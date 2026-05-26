import csv
import json
import re
from pathlib import Path

ENTITIES = ["Network", "Phase", "Node", "Span", "Organisation", "Contract", "Wayleave", "Document"]

REFERENCE_DEFS = {"OrganisationReference": "Organisation", "PhaseReference": "Phase"}

SCHEMA_PATH = Path("schema/network-schema.json")
DOC_PATH = Path("docs/reference/data_model.md")

EXCLUDE_PATHS = {"publisher/name", "publisher/identifier", "crs/name", "crs/uri", "links"}


def resolve_ref(ref_name, prop):
    """Resolve a $ref name to a known entity name, or None if unrecognised."""
    if ref_name in ENTITIES:
        return ref_name
    if ref_name in REFERENCE_DEFS:
        return REFERENCE_DEFS[ref_name]
    if ref_name in ENTITIES and "x-references" in prop:
        return prop["x-references"]["definition"].split("/")[-1]
    return None


def _ref_entity(prop):
    """Return (entity_name, cardinality) if prop is a relationship, else (None, None)."""
    if prop.get("type") == "array":
        items = prop.get("items", {})
        if "$ref" in items:
            ref_name = items["$ref"].split("/")[-1]
        elif "x-references" in items:
            ref_name = items["x-references"]["definition"].split("/")[-1]
        else:
            return None, None
        cardinality = "1:N"
    elif "$ref" in prop:
        ref_name = prop["$ref"].split("/")[-1]
        cardinality = "1:1"
    elif "x-references" in prop:
        ref_name = prop["x-references"]["definition"].split("/")[-1]
        cardinality = "1:1"
    else:
        return None, None
    return resolve_ref(ref_name, prop), cardinality


def _is_geojson_def(defn):
    """Return True if this $def is a GeoJSON geometry type (treat as a leaf, not recursed)."""
    props = defn.get("properties", {})
    return "coordinates" in props or "geometries" in props


def get_relationships(schema, all_defs, prefix=""):
    """Recursively return a list of relationships from schema properties."""
    relationships = []
    for name, prop in schema.get("properties", {}).items():
        path = f"{prefix}/{name}" if prefix else name
        entity, cardinality = _ref_entity(prop)
        if entity:
            relationships.append({
                "entity": entity,
                "title": prop.get("title", ""),
                "description": prop.get("description", ""),
                "cardinality": cardinality,
            })
        else:
            # Resolve $ref to a non-entity definition and recurse into sub-properties
            resolved = prop
            if "$ref" in prop:
                ref_name = prop["$ref"].split("/")[-1]
                if ref_name not in ENTITIES and ref_name not in REFERENCE_DEFS:
                    resolved = all_defs.get(ref_name, prop)
            if "properties" in resolved and not _is_geojson_def(resolved):
                relationships.extend(get_relationships(resolved, all_defs, prefix=path))
    return relationships


def write_relationships_csv(entity, relationships, output_dir=Path(".")):
    """Write a CSV of relationships for an entity to output_dir/<entity>-relationships.csv."""
    path = output_dir / f"{entity.lower()}-relationships.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Entity", "Cardinality", "Description"])
        for rel in relationships:
            writer.writerow([
                f"[{rel['entity']}](#{rel['entity'].lower()})",
                rel["cardinality"],
                f"{rel['title']}: {rel['description']}",
            ])
    return path


def get_property_paths(schema, all_defs, prefix=""):
    """Recursively return JSON pointer paths for all non-relationship properties."""
    paths = []
    for name, prop in schema.get("properties", {}).items():
        path = f"{prefix}/{name}" if prefix else name

        # Skip properties that are relationships to known entities
        if _ref_entity(prop)[0]:
            continue

        # Resolve a $ref to a non-entity definition
        resolved = prop
        if "$ref" in prop:
            ref_name = prop["$ref"].split("/")[-1]
            if ref_name not in ENTITIES and ref_name not in REFERENCE_DEFS:
                resolved = all_defs.get(ref_name, prop)

        # Recurse into objects with sub-properties, except GeoJSON geometry types
        if "properties" in resolved and not _is_geojson_def(resolved):
            paths.extend(get_property_paths(resolved, all_defs, prefix=path))
        else:
            paths.append(path)

    return paths


def update_doc_includes(doc_path, entity_includes):
    """Update or insert :include: options in {jsonschema} directives in doc_path."""
    with open(doc_path) as f:
        content = f.read()

    # Match complete {jsonschema} directive blocks (opening line + options + closing ```)
    block_re = re.compile(
        r'(```\{jsonschema\}[^\n]*\n)(.*?)(^```[ \t]*\n)',
        re.MULTILINE | re.DOTALL,
    )

    def replace_block(m):
        opening, body, closing = m.group(1), m.group(2), m.group(3)

        pointer_match = re.search(r':pointer:\s*/\$defs/(\w+)', body)
        entity = pointer_match.group(1) if pointer_match else "Network"

        if entity not in entity_includes:
            return m.group(0)

        include_line = f":include: {entity_includes[entity]}\n"

        if ':include:' in body:
            body = re.sub(r':include:[^\n]*\n', include_line, body)
        elif pointer_match:
            # No existing :include: — insert it after the :pointer: line
            body = re.sub(r'(:pointer:[^\n]*\n)', r'\1' + include_line, body)
        else:
            # Network has no :pointer:; insert at the top of the options block
            body = include_line + body

        return opening + body + closing

    new_content = block_re.sub(replace_block, content)

    with open(doc_path, "w") as f:
        f.write(new_content)


def main():
    with open(SCHEMA_PATH) as f:
        network_schema = json.load(f)

    all_defs = network_schema.get("$defs", {})
    entity_includes = {}

    for entity in ENTITIES:
        schema = network_schema if entity == "Network" else network_schema["$defs"][entity]

        relationships = get_relationships(schema, all_defs)
        paths = [p for p in get_property_paths(schema, all_defs) if p not in EXCLUDE_PATHS]
        entity_includes[entity] = ",".join(paths)

        print(f"\nEntity: {entity}")
        print(f"Description: {schema['description']}")
        print("Properties:")
        for path in paths:
            print(f"  {path}")

        if relationships:
            csv_path = write_relationships_csv(entity, relationships)
            print(f"Relationships written to {csv_path}")

    update_doc_includes(DOC_PATH, entity_includes)
    print(f"\nUpdated :include: options in {DOC_PATH}")


if __name__ == "__main__":
    main()
