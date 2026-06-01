"""
Extract the logical data model from network-schema.json.

The schema uses custom keywords to control extraction:
  x-logical-type: entity    - $defs entry is a first-class entity (Node, Span, etc.)
  x-logical-type: attribute - $defs entry is a leaf attribute (e.g. a GeoJSON geometry);
                              don't recurse, record as a single attribute
  x-logical-type: exclude   - property is omitted from the data model
  x-references              - property or $defs entry is a foreign-key reference to an entity
  x-relationship-label       - human-friendly label for relationships, used in Mermaid diagram
"""

import csv
import json

# Populated once in __main__; treated as read-only by all functions.
SCHEMA: dict = {}


def is_entity(schema):
    """Return True if schema is a first-class entity (x-logical-type: entity)."""
    return schema.get("x-logical-type") == "entity"


def resolve_ref(pointer):
    """Return the $defs entry for a JSON pointer, or None if unresolvable.
    Only supports top-level $defs pointers (e.g. '#/$defs/Node'), not pointers to nested schemas."""
    return SCHEMA["$defs"].get(pointer.split("/")[-1])


def resolve_definition(prop):
    """Return the resolved $defs entry for a property with $ref or x-references, else None."""
    pointer = prop.get("$ref") or prop.get("x-references", {}).get("definition")
    return resolve_ref(pointer) if pointer else None


def get_relationship(entity, prop_schema, cardinality):
    """Return a dict describing a relationship to entity, sourced from prop_schema."""
    return {
        "entity": f"[{entity['title']}](#{entity['title'].lower()})",
        "cardinality": cardinality,
        "description": f"{prop_schema['title']}: {prop_schema['description']}",
        "label": prop_schema.get("x-relationship-label", "")
    }


def get_attribute(path, prop_schema):
    """Return a dict describing an attribute at path, sourced from prop_schema."""
    return {
        "path": '/'.join(path),
        "title": prop_schema["title"],
        "description": prop_schema["description"],
        "type": prop_schema.get("type") + f" ({prop_schema.get("items", {}).get('type')})" if prop_schema.get("type") == "array" else prop_schema.get("type"),
    }


def extract_model(schema, path=None, cardinality="1:1", result=None, prop_schema=None):
    """
    Recursively walk schema, collecting attributes and relationships into result.

    result is a shared dict passed through all recursive calls so that attributes
    and relationships for an entity accumulate into the same lists.

    prop_schema is the property schema that triggered the current recursive call. It is
    needed when we recurse into a $def (e.g. PointGeometry or OrganisationReference),
    where we want the originating property's title/description rather than the def's.
    """
    if path is None:
        path = []
    if result is None:
        result = {"relationships": [], "attributes": [], "collapse": []}

    # x-logical-type: attribute → leaf node (e.g. a geometry), record and stop
    if schema.get("x-logical-type") == "attribute":
        result["attributes"].append(get_attribute(path, prop_schema))
        result["collapse"].append("/".join(path))

    # x-references at def level → the whole def is a foreign-key reference (e.g. OrganisationReference)
    elif "x-references" in schema:
        definition = resolve_ref(schema["x-references"]["definition"])
        if is_entity(definition):
            result["relationships"].append(get_relationship(definition, prop_schema, cardinality))

    else:
        for prop, prop_schema in schema.get("properties", {}).items():
            if prop_schema.get("x-logical-type") == "exclude":
                continue

            definition = resolve_definition(prop_schema)
            if definition is not None:
                if is_entity(definition):
                    # $ref to an entity → relationship
                    result["relationships"].append(get_relationship(definition, prop_schema, cardinality))
                else:
                    # $ref to a non-entity def (e.g. Address) → flatten into this entity
                    extract_model(definition, path=path + [prop], cardinality=cardinality, result=result, prop_schema=prop_schema)

            elif prop_schema.get("type") == "object":
                extract_model(prop_schema, path=path + [prop], cardinality=cardinality, result=result, prop_schema=prop_schema)

            elif prop_schema.get("type") == "array":
                items = prop_schema.get("items", {})
                items_definition = resolve_definition(items)
                if items_definition is not None:
                    if is_entity(items_definition):
                        result["relationships"].append(get_relationship(items_definition, prop_schema, "1:N"))
                    else:
                        extract_model(items_definition, path=path + [prop, "0"], cardinality="1:N", result=result, prop_schema=prop_schema)
                elif items.get("type") == "object":
                    extract_model(items, path=path + [prop, "0"], cardinality="1:N", result=result, prop_schema=prop_schema)
                else:
                    # Array of primitives → record as attribute
                    result["attributes"].append(get_attribute(path + [prop], prop_schema))

            else:
                # Leaf property
                result["attributes"].append(get_attribute(path + [prop], prop_schema))

    return result


if __name__ == "__main__":
    with open("schema/network-schema.json") as f:
        SCHEMA = json.load(f)

    entities = {}

    entities["Network"] = extract_model(SCHEMA)

    for name, schema in SCHEMA.get("$defs", {}).items():
        if is_entity(schema):
            entities[schema["title"]] = extract_model(schema)
    
    with open("docs/reference/data_model/data_model.mmd", "w") as mermaid_file:
        # Write Mermaid diagram frontmatter and header
        mermaid_file.write("\n".join([
            "---",
            "config:",
            "  layout: elk",
            "---",
            "erDiagram"
        ]))

        # Write relationships.csv, attributes.csv and directive.md for each entity
        for entity, definition in entities.items():

            with open(f"docs/reference/data_model/{entity.lower()}/relationships.csv", "w") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["entity", "cardinality", "description"])
                for relationship in definition["relationships"]:
                    csv_writer.writerow([relationship["entity"], relationship["cardinality"], relationship["description"]])

            with open(f"docs/reference/data_model/{entity.lower()}/attributes.csv", "w") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["path", "title", "description", "type"])
                for attribute in definition["attributes"]:
                    csv_writer.writerow([attribute["path"], attribute["title"], attribute["description"], attribute["type"]])

            # directive.txt contains a MyST jsonschema directive that renders the entity's attributes
            with open(f"docs/reference/data_model/{entity.lower()}/directive.txt", "w") as f:
                include = ','.join(attr['path'] for attr in definition['attributes'])
                collapse = ','.join(definition['collapse'])
                f.write("\n".join(list(filter(None, [
                    "```{jsonschema} ../../../_readthedocs/html/network-schema.json",
                    f":pointer: /$defs/{entity}" if entity != "Network" else "",
                    f":include: {include}",
                    f":collapse: {collapse}" if len(collapse) > 0 else "",
                    ":nocrossref:",
                    ":addtargets:",
                    ":prefix: data_model",
                    "```",
                ]))))
            
            # Write relationships to Mermaid diagram
            for relationship in definition["relationships"]:
                target_entity = relationship["entity"].split("]")[0][1:]
                cardinality = relationship["cardinality"]
                if cardinality == "1:1":
                    mermaid_file.write(f"\n{entity} ||--|| {target_entity}: \"{relationship['label']}\"")
                elif cardinality == "1:N":
                    mermaid_file.write(f"\n{entity} ||--o{{ {target_entity}: \"{relationship['label']}\"")
        
        mermaid_file.write("\n".join([
            "classDef spatial fill:#f3ffa6ff,stroke:#bbd034",
            "classDef non-spatial fill:#cec7ffff,stroke:#110e27",
            "class Node,Span spatial",
            "class Network,Organisation,Phase,Contract,Wayleave,Document non-spatial",
            "direction LR"
        ]))
