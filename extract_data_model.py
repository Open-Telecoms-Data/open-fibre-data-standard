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


def get_attribute(path, prop_schema, parent_titles=None, parent_descriptions=None):
    """Return a dict describing an attribute at path, sourced from prop_schema.

    parent_titles is a list of ancestor property titles accumulated while flattening
    non-entity $defs. When present, they are prepended to form a qualified title
    (e.g. ['Address'] + 'Street address' → 'Address street address').

    parent_descriptions is the corresponding list of ancestor property descriptions.
    When present, they are prepended as separate paragraphs (joined with '\\n\\n')."""
    if parent_titles:
        title = " ".join([parent_titles[0]] + [t.lower() for t in parent_titles[1:]] + [prop_schema["title"].lower()])
    else:
        title = prop_schema["title"]
    if parent_descriptions:
        description = " | ".join(parent_descriptions + [prop_schema["description"]])
    else:
        description = prop_schema["description"]
    return {
        "path": '/'.join(path),
        "title": title,
        "description": description,
        "type": prop_schema.get("type") + f" ({prop_schema.get('items', {}).get('type')})" if prop_schema.get("type") == "array" else prop_schema.get("type"),
        "codelist": prop_schema.get("codelist")
    }


def extract_model(schema, path=None, cardinality="1:1", result=None, parent_prop_schema=None, parent_titles=None, parent_descriptions=None):
    """
    Recursively walk schema, collecting attributes and relationships into result.

    result is a shared dict passed through all recursive calls so that attributes
    and relationships for an entity accumulate into the same lists.

    parent_prop_schema is the property schema that triggered the current recursive call,
    needed in the x-logical-type: attribute and x-references branches where we want the
    originating property's title/description rather than the def's.

    parent_titles and parent_descriptions are lists of ancestor property titles/descriptions
    accumulated while flattening non-entity $defs. Each grows by one entry each time we
    recurse into a $ref to a non-entity def, and are used to build qualified attribute
    titles and multi-paragraph descriptions.
    """
    if path is None:
        path = []
    if parent_titles is None:
        parent_titles = []
    if parent_descriptions is None:
        parent_descriptions = []
    if result is None:
        result = {"relationships": [], "attributes": [], "collapse": []}

    # x-logical-type: attribute → leaf node (e.g. a geometry), record and stop
    # parent_prop_schema is already the last entry in parent_titles/parent_descriptions,
    # so strip it before passing to avoid doubling the title and description.
    if schema.get("x-logical-type") == "attribute":
        result["attributes"].append(get_attribute(path, parent_prop_schema, parent_titles[:-1], parent_descriptions[:-1]))
        result["collapse"].append("/".join(path))

    # x-references at def level → the whole def is a foreign-key reference (e.g. OrganisationReference)
    elif "x-references" in schema:
        definition = resolve_ref(schema["x-references"]["definition"])
        if is_entity(definition):
            result["relationships"].append(get_relationship(definition, parent_prop_schema, cardinality))

    else:
        for child_prop_name, child_prop_schema in schema.get("properties", {}).items():
            if child_prop_schema.get("x-logical-type") == "exclude":
                continue

            definition = resolve_definition(child_prop_schema)
            if definition is not None:
                if is_entity(definition):
                    # $ref to an entity → relationship
                    result["relationships"].append(get_relationship(definition, child_prop_schema, cardinality))
                else:
                    # $ref to a non-entity def (e.g. Address) → flatten, accumulating title and description
                    child_title = child_prop_schema.get("title")
                    child_desc = child_prop_schema.get("description")
                    new_titles = parent_titles + ([child_title] if child_title else [])
                    new_descriptions = parent_descriptions + ([child_desc] if child_desc else [])
                    extract_model(definition, path=path + [child_prop_name], cardinality=cardinality, result=result, parent_prop_schema=child_prop_schema, parent_titles=new_titles, parent_descriptions=new_descriptions)

            elif child_prop_schema.get("type") == "object":
                extract_model(child_prop_schema, path=path + [child_prop_name], cardinality=cardinality, result=result, parent_titles=parent_titles, parent_descriptions=parent_descriptions)

            elif child_prop_schema.get("type") == "array":
                items = child_prop_schema.get("items", {})
                items_definition = resolve_definition(items)
                if items_definition is not None:
                    if is_entity(items_definition):
                        result["relationships"].append(get_relationship(items_definition, child_prop_schema, "1:N"))
                    else:
                        child_title = child_prop_schema.get("title")
                        child_desc = child_prop_schema.get("description")
                        new_titles = parent_titles + ([child_title] if child_title else [])
                        new_descriptions = parent_descriptions + ([child_desc] if child_desc else [])
                        extract_model(items_definition, path=path + [child_prop_name, "0"], cardinality="1:N", result=result, parent_prop_schema=child_prop_schema, parent_titles=new_titles, parent_descriptions=new_descriptions)
                elif items.get("type") == "object":
                    child_title = child_prop_schema.get("title")
                    child_desc = child_prop_schema.get("description")
                    new_titles = parent_titles + ([child_title] if child_title else [])
                    new_descriptions = parent_descriptions + ([child_desc] if child_desc else [])
                    extract_model(items, path=path + [child_prop_name, "0"], cardinality="1:N", result=result, parent_prop_schema=child_prop_schema, parent_titles=new_titles, parent_descriptions=new_descriptions)
                else:
                    # Array of primitives → record as attribute
                    result["attributes"].append(get_attribute(path + [child_prop_name], child_prop_schema, parent_titles, parent_descriptions))

            else:
                # Leaf property
                result["attributes"].append(get_attribute(path + [child_prop_name], child_prop_schema, parent_titles, parent_descriptions))

    return result


if __name__ == "__main__":
    with open("schema/network-schema.json") as f:
        SCHEMA = json.load(f)

    entities = {}

    entities["Network"] = extract_model(SCHEMA)

    for name, schema in SCHEMA.get("$defs", {}).items():
        if is_entity(schema):
            entities[schema["title"]] = extract_model(schema)
    
    with open("docs/reference/data_model/entities.csv", "w", newline="") as f:
        csv_writer = csv.writer(f, lineterminator="\n")
        csv_writer.writerow(["name"])
        for entity, definition in entities.items():
            csv_writer.writerow([entity])

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

            with open(f"docs/reference/data_model/{entity.lower()}/relationships.csv", "w", newline="") as f:
                csv_writer = csv.writer(f, lineterminator="\n")
                csv_writer.writerow(["entity", "cardinality", "description"])
                for relationship in definition["relationships"]:
                    csv_writer.writerow([relationship["entity"], relationship["cardinality"], relationship["description"]])

            with open(f"docs/reference/data_model/{entity.lower()}/attributes.csv", "w", newline="") as f:
                csv_writer = csv.writer(f, lineterminator="\n")
                csv_writer.writerow(["path", "title", "description", "type", "codelist"])
                for attribute in definition["attributes"]:
                    csv_writer.writerow([attribute["path"], attribute["title"], attribute["description"], attribute["type"], attribute.get("codelist", "")])

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
