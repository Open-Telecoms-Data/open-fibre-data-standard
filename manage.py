#!/usr/bin/env python3
from copy import deepcopy
import click
import csv
import json
import jsonref
import logging
import os
import re
import requests
import shutil
import subprocess
import sys

from contextlib import contextmanager
from flattentool import create_template, flatten
from io import StringIO
from lxml import etree
from ocdskit.mapping_sheet import mapping_sheet
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'schema', 'data_formats', 'geopackage'))
import buildofdsgeopackage

basedir = Path(__file__).resolve().parent
codelistdir = basedir / 'schema' / 'codelists'
examplesdir = basedir / 'examples'
referencedir = basedir / 'docs' / 'reference'
schemadir = basedir / 'schema'


def read_lines(filename):
    """Read a file and return a list of lines."""

    with open(filename, 'r') as f:
        return f.readlines()


def write_lines(filename, lines):
    """Write a list of lines to a file."""

    with open(filename, 'w') as f:
        f.writelines(lines)


def csv_load(url, delimiter=','):
    """
    Loads CSV data into a ``csv.DictReader`` from the given URL.
    """
    reader = csv.DictReader(StringIO(get(url).text), delimiter=delimiter)
    return reader


@contextmanager
def csv_dump(path, fieldnames):
    """
    Writes CSV headers to the given path, and yields a ``csv.writer``.
    """
    f = (Path(path)).open('w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fieldnames)
    try:
        yield writer
    finally:
        f.close()


def get(url):
    """
    GETs a URL and returns the response. Raises an exception if the status code is not successful.
    """
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response


def json_dump(filename, data):
    """
    Writes JSON data to the given filename.
    """
    with (schemadir / filename).open('w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def delete_directory_contents(directory_path):
  """
  Deletes the contents of a directory on disk.
  """
  for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


def json_load(filename, library=json):
    """
    Loads JSON data from the given filename.
    """
    with (schemadir / filename).open() as f:
        return library.load(f)


def get_dereferenced_schema(schema, output=None):
    """
    Returns the dereferenced schema.
    """
    # Without a deepcopy, changes to referenced objects are copied across referring objects. However, the deepcopy does
    # not retain the `__reference__` property.
    if not output:
        output = deepcopy(schema)

    if isinstance(schema, list):
        for index, item in enumerate(schema):
            get_dereferenced_schema(item, output[index])
    elif isinstance(schema, dict):
        for key, value in schema.items():
            get_dereferenced_schema(value, output[key])
        if hasattr(schema, '__reference__'):
            for prop in schema.__reference__:
                if prop != '$ref':
                    output[prop] = schema.__reference__[prop]

    return output


def update_csv_docs(jsonref_schema):
  """Update docs/reference/data_formats/csv.md"""

  # Load csv reference
  csv_reference = read_lines(referencedir / 'data_formats' / 'csv.md')

  # Preserve introductory content up to the ## networks heading
  csv_reference = csv_reference[:csv_reference.index("### networks\n") - 1]

  # Generate CSV reference
  dereferenced_schema = get_dereferenced_schema(jsonref_schema)
  markdown = generate_csv_reference_markdown('networks', dereferenced_schema)
 
  for key, value in markdown.items():
    csv_reference.append(f"\n{'#'*(value['depth']+1)} {key}\n\n")
    csv_reference.extend(value['content'])

  write_lines(referencedir / 'data_formats' / 'csv.md', csv_reference)

def generate_csv_reference_markdown(table, schema, parents=None, depth=2):
  """
  Recursively generate reference documentation for each table in the CSV publication format.
  
  :param table: the name of the table
  :param schema: the schema for the object represented by the table
  :param parents: a list of the parents of the object represented by the table
  :param depth: the depth in the JSON schema hierarchy of the object represented by the table
  """

  markdown = {}
  if parents:
    table = '_'.join(parents[1:] + [table])
  markdown[table] = {'depth': depth, 'content': []}
  
  include_pointers = []

  if parents is None:
    parents = []

  if schema['type'] == 'object':
    properties = schema['properties']
  elif schema['type'] == 'array':
    properties = schema['items']['properties']
  
  markdown[table]['content'] = ["This table is related to the following tables:\n\n"]

  # Generate JSON pointer to parent and link to parent table
  parent_ref= ''
  if parents:
    if len(parents) > 1:
      parent_ref = f"{'/0/'.join([parent for parent in parents[1:]])}"
 
    markdown[table]['content'].append(
      f"- [{parents[-1]}](#{parents[-1].lower()}): many-to-one by `{parent_ref + '/0/' if len(parent_ref) > 0 else ''}id`\n"
    )

  # Add references to parent object ids to list of pointers for jsonschema directive
  if len(parents) == 1:
    include_pointers.extend(['id'])
  elif len(parents) > 0:
    include_pointers.extend(['id', f"{parent_ref}/0/id"])

  # Generate list of links to child tables and populate list of pointers for jsonschema directive
  for key,value in properties.items():
    if value['type'] == 'array' and value['items']['type'] == 'object':     
      markdown[table]['content'].append(
        f"- [{key if table == 'networks' else f'{table}_{key}'}](#{key if table == 'networks' else f'{table}_{key}'.lower()}): one-to-many by `{'id' if table == 'networks' else '/0/'.join(parents[1:] + [table, 'id'])}`\n"
      )
      markdown.update(generate_csv_reference_markdown(key, value, parents + [table], depth + 1))
    else:
      include_pointers.append(f"{parent_ref}{'/0/' if len(parent_ref) > 0 else ''}{table.split('_')[-1]+'/0/' if len(parents)>0 else ''}{key}")

  # Generate links to examples and templates
  markdown[table]['content'].append(f"\nThe columns in this table are listed below. You can also download an [example CSV file](../../../examples/csv/{table}.csv) or a [blank template](../../../examples/csv/template/{table}.csv) for this table.\n\n")

  # Generate jsonschema directive
  markdown[table]['content'].extend([
    "```{jsonschema} ../../../_readthedocs/html/network-schema.json\n"
    f":include: {','.join(include_pointers)}\n"
  ])

  # Collapse node locations and span routes, which are represented using well-known text in the CSV format
  if table == 'nodes':
    markdown[table]['content'].extend([
      ":collapse: nodes/0/location\n"
    ])
  elif table == 'spans':
    markdown[table]['content'].extend([
      ":collapse: spans/0/route\n"
    ])

  markdown[table]['content'].extend([
    ":nocrossref:\n"
    "```\n"
  ])

  return markdown


def get_definition_references(schema, defn, parents=None, network_schema=None):
  """
  Recursively generate a list of JSON pointers that reference a definition in JSON schema.

  :param schema: The JSON schema
  :defn: The name of the definition
  :parents: A list of the parents of schema
  :network_schema: The full network schema
  """

  references = []

  if parents is None:
    parents = []

  if network_schema is None:
    network_schema = schema

  if 'properties' in schema:
    for key, value in schema['properties'].items():
      if value.get('type') == 'array' and '$ref' in value['items']:
        if value['items']['$ref'] == f"#/$defs/{defn}":
          references.append(parents + [key, '0'])
        else:
          references.extend(get_definition_references(network_schema['$defs'][value['items']['$ref'].split('/')[-1]], defn, parents + [key, '0'], network_schema))
      elif '$ref' in value:
        if value['$ref'] == f"#/$defs/{defn}":
          references.append(parents + [key])
        else:
          references.extend(get_definition_references(network_schema['$defs'][value['$ref'].split('/')[-1]], defn, parents + [key], network_schema))
      elif 'properties' in value:
          references.extend(get_definition_references(value, defn, parents + [key], network_schema))

  if '$defs' in schema:
    for key, value in schema['$defs'].items():
      references.extend(get_definition_references(value, defn, [key], network_schema))
  
  return references


# Extract the logical data model from network-schema.json.
#
# The schema uses custom keywords to control extraction:
#   x-logical-type: entity    - $defs entry is a first-class entity (Node, Span, etc.)
#   x-logical-type: attribute - $defs entry is a leaf attribute (e.g. a GeoJSON geometry);
#                               don't recurse, record as a single attribute
#   x-logical-type: exclude   - property is omitted from the data model
#   x-references              - property or $defs entry is a foreign-key reference to an entity
#   x-relationship-label       - human-friendly label for relationships, used in Mermaid diagram

# Populated once by update_data_model_docs; treated as read-only by the functions below.
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


def update_data_model_docs(schema):
    """Generate schema/data_model/ files: entities.csv, data_model.mmd, and per-entity
    attributes.csv, relationships.csv and directive.txt."""
    global SCHEMA
    SCHEMA = schema

    entities = {}
    entities["Network"] = extract_model(SCHEMA)
    for defn_name, defn in SCHEMA.get("$defs", {}).items():
        if is_entity(defn):
            entities[defn["title"]] = extract_model(defn)

    output_dir = schemadir / 'data_model'
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "entities.csv").open("w", newline="") as f:
        csv_writer = csv.writer(f, lineterminator="\n")
        csv_writer.writerow(["name"])
        for entity in entities:
            csv_writer.writerow([entity])

    with (output_dir / "data_model.mmd").open("w") as mermaid_file:
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
            entity_dir = output_dir / entity.lower()
            entity_dir.mkdir(parents=True, exist_ok=True)

            with (entity_dir / "relationships.csv").open("w", newline="") as f:
                csv_writer = csv.writer(f, lineterminator="\n")
                csv_writer.writerow(["entity", "cardinality", "description"])
                for relationship in definition["relationships"]:
                    csv_writer.writerow([relationship["entity"], relationship["cardinality"], relationship["description"]])

            with (entity_dir / "attributes.csv").open("w", newline="") as f:
                csv_writer = csv.writer(f, lineterminator="\n")
                csv_writer.writerow(["path", "title", "description", "type", "codelist"])
                for attribute in definition["attributes"]:
                    csv_writer.writerow([attribute["path"], attribute["title"], attribute["description"], attribute["type"], attribute.get("codelist", "")])

            # directive.txt contains a MyST jsonschema directive that renders the entity's attributes
            with (entity_dir / "directive.txt").open("w") as f:
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


@click.group()
def cli():
    pass


@cli.command()
def pre_commit():
    """Update derivative schema files, examples and reference documentation:
      - network-schema.csv
      - schema/data_model
      - examples/csv/template
      - examples/csv
      - reference/data_formats/csv.md
      - examples/geojson/nodes.geojson
      - examples/geojson/spans.geojson
      Also run:
      - mdformat
    """

    # Load schema
    schema = json_load('data_formats/json/network-schema.json')
    jsonref_schema = json_load('data_formats/json/network-schema.json', jsonref)
     
    # Generate network-schema.csv
    schema_table = mapping_sheet(schema, include_codelist=True, include_definitions=False)

    with (schemadir / 'data_formats' / 'json' / 'network-schema.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=schema_table[0], lineterminator='\n')
        
        writer.writeheader()
        for row in schema_table[1]:
            writer.writerow(row)

    # Generate schema/data_model files
    update_data_model_docs(schema)

    # Generate GeoPackage
    builder = buildofdsgeopackage.Builder(
        root_directory=os.path.realpath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)))
        ),
    )
    builder.go()

    # Generate diagram from GeoPackage
    subprocess.run(["mermerd", "--runConfig", "docs/reference/data_formats/geopackage/geopackage.yaml"])

    # Add style config to diagram and remove non-key attributes
    with open("docs/reference/data_formats/geopackage/geopackage.mmd", 'r') as f:
        lines = f.readlines()

    # 1. Prepare Header
    header = "---\nconfig:\n  layout: elk\n---\n"
    
    # 2. Prepare Footer
    footer = (
        "\n    classDef feature fill:#f3ffa6ff,stroke:#bbd034\n"
        "    classDef attribute fill:#cec7ffff,stroke:#110e27\n"
        "    classDef mapping fill:#efefefff,stroke:#434343ff\n\n"
        "    class nodes,spans feature\n"
        "    class networks,organisations,phases,contracts,wayleaves attribute\n"
        "    class relation_contracts_relatedPhases,relation_spans_networkProviders,relation_spans_wayleaves,relation_nodes_networkProviders mapping\n"
        "    direction BT\n"
    )

    processed_content = []
    
    # Regex to identify lines inside table definitions that are NOT PK or FK
    # It looks for lines that contain 'PK' or 'FK'
    is_inside_table = False
    
    for line in lines:
        stripped = line.strip()
        
        # Detect start/end of table blocks
        if '{' in line:
            is_inside_table = True
            processed_content.append(line)
            continue
        if '}' in line:
            is_inside_table = False
            processed_content.append(line)
            continue
            
        if is_inside_table:
            # 3. Remove attributes that aren't PK or FK
            # We keep the line if it contains PK or FK (case insensitive)
            if re.search(r'\bPK\b|\bFK\b', stripped) and not re.search('identifier__scheme', stripped) and not re.search('type', stripped) and not re.search('language', stripped):
                processed_content.append(line)
            else:
                # Skip normal attributes
                continue
        else:
            # Keep lines outside of tables (like relationship definitions)
            processed_content.append(line)

    # Combine everything
    final_output = header + "".join(processed_content) + footer

    with open("docs/reference/data_formats/geopackage/geopackage.mmd", 'w') as f:
        f.write(final_output)

    # Update examples/csv
    delete_directory_contents('examples/csv')
    flatten(
      input_name='examples/json/network-package.json',
      schema='schema/data_formats/json/network-schema.json',
      output_name='examples/csv',
      output_format='csv',
      main_sheet_name="networks",
      truncation_length=9,
      root_list_path='networks',
      line_terminator='LF',
      convert_wkt=True
    )

    # Update examples/csv/template
    create_template(
      schema='schema/data_formats/json/network-schema.json',
      output_name='examples/csv/template',
      output_format="csv",
      main_sheet_name="networks",
      truncation_length=9,
      no_deprecated_fields=True,
      line_terminator='LF',
      convert_wkt=True
    )

    # Update docs/reference/data_formats/csv.md
    update_csv_docs(jsonref_schema)

    # Update examples/geojson/nodes.geojson and examples/geojson/spans.geojson
    subprocess.run(['libcoveofds', 'jsontogeojson', 'examples/json/network-package.json', 'examples/geojson/nodes.geojson', 'examples/geojson/spans.geojson'])

    # Run mdformat
    subprocess.run(['mdformat', 'docs'])


@cli.command()
def update_media_type():
    """
    Update mediaType.csv from IANA.

    Ignores deprecated and obsolete media types.
    """
    # https://www.iana.org/assignments/media-types/media-types.xhtml

    # See "Registries included below".
    registries = [
        'application',
        'audio',
        'font',
        'image',
        'message',
        'model',
        'multipart',
        'text',
        'video',
    ]

    with csv_dump('schema/codelists/open/mediaType.csv', ['Code', 'Title']) as writer:
        for registry in registries:
            # See "Available Formats" under each heading.
            reader = csv_load(f'https://www.iana.org/assignments/media-types/{registry}.csv')
            for row in reader:
                if ' ' in row['Name']:
                    name, message = row['Name'].split(' ', 1)
                else:
                    name, message = row['Name'], None
                code = f"{registry}/{name}"
                template = row['Template']
                # All messages are expected to be about deprecation and obsoletion.
                if message:
                    logging.warning('%s: %s', message, code)
                # "x-emf" has "image/emf" in its "Template" value (but it is deprecated).
                elif template and template != code:
                    raise Exception(f"expected {code}, got {template}")
                else:
                    writer.writerow([code, name])

        writer.writerow(['offline/print', 'print'])


@cli.command()
def update_language():
    """
    Update language.csv from ISO 639-1.
    """
    # https://www.iso.org/iso-639-language-codes.html
    # https://id.loc.gov/vocabulary/iso639-1.html

    with csv_dump('schema/codelists/open/language.csv', ['Code', 'Title']) as writer:
        reader = csv_load('https://id.loc.gov/vocabulary/iso639-1.tsv', delimiter='\t')
        for row in reader:
            # Remove parentheses, like "Greek, Modern (1453-)", and split alternatives.
            titles = re.split(r' *\| *', re.sub(r' \(.+\)', '', row['Label (English)']))
            # Remove duplication like "Ndebele, North |  North Ndebele" and join alternatives using a comma instead of
            # a pipe. To preserve order, a dict without values is used instead of a set.
            titles = ', '.join({' '.join(reversed(title.split(', '))): None for title in titles})
            writer.writerow([row['code'], titles])


@cli.command()
@click.argument('file', type=click.File())
def update_country(file):
    """
    Update country.csv from ISO 3166-1 using FILE.

    To retrieve the file:

    \b
    1. Open https://www.iso.org/obp/ui/#search/code/
    2. Open the "Network" tab of the "Web Inspector" utility (Option-Cmd-I in Safari)
    3. Set "Results per page:" to 300
    4. Click the last "UIDL" entry in the "Network" tab
    5. Copy its contents, excluding the for-loop, into a file
    """
    # https://www.iso.org/iso-3166-country-codes.html
    # https://www.iso.org/obp/ui/#search

    codes = {
        # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#User-assigned_code_elements
        'XK': 'Kosovo',
    }

    rpc = json.load(file)[0]['rpc'][0]
    offset = int(rpc[0])
    for entry in rpc[3][1]:
        d = entry['d']
        # Clean "Western Sahara*", "United Arab Emirates (the)", etc.
        codes[d[str(offset + 9)]] = re.sub(r' \(the\)|\*', '', d[str(offset + 13)])
        # The country code appears at offsets 9 and 15. Check that they are always the same.
        assert d[str(offset + 9)] == d[str(offset + 15)]

    with open('schema/codelists/closed/country.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['Code', 'Title'])
        for code in sorted(codes):
            writer.writerow([code, codes[code]])


@cli.command()
def update_currency():
    """
    Update currency.csv from ISO 4217.
    """
    # https://www.iso.org/iso-4217-currency-codes.html
    # https://www.six-group.com/en/products-services/financial-information/data-standards.html#scrollTo=currency-codes

    # "List One: Current Currency & Funds"
    current_codes = {}
    url = 'https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml'  # noqa: E501
    tree = etree.fromstring(get(url).content)
    for node in tree.xpath('//CcyNtry'):
        match = node.xpath('./Ccy')
        # Entries like Antarctica have no universal currency.
        if match:
            code = node.xpath('./Ccy')[0].text
            title = node.xpath('./CcyNm')[0].text.strip()
            if code not in current_codes:
                current_codes[code] = title
            # We should expect currency titles to be consistent across countries.
            elif current_codes[code] != title:
                raise Exception(f'expected {current_codes[code]}, got {title}')

    # "List Three: Historic Denominations (Currencies & Funds)"
    historic_codes = {}
    url = 'https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-three.xml'  # noqa: E501
    tree = etree.fromstring(get(url).content)
    for node in tree.xpath('//HstrcCcyNtry'):
        code = node.xpath('./Ccy')[0].text
        title = node.xpath('./CcyNm')[0].text.strip()
        valid_until = node.xpath('./WthdrwlDt')[0].text
        # Use ISO8601 interval notation.
        valid_until = re.sub(r'^(\d{4})-(\d{4})$', r'\1/\2', valid_until.replace(' to ', '/'))
        if code not in current_codes:
            if code not in historic_codes:
                historic_codes[code] = {'Title': title, 'Valid Until': valid_until}
            # If the code is historical, use the most recent title and valid date.
            elif valid_until > historic_codes[code]['Valid Until']:
                historic_codes[code] = {'Title': title, 'Valid Until': valid_until}

    with csv_dump('schema/codelists/closed/currency.csv', ['Code', 'Title', 'Valid Until']) as writer:
        for code in sorted(current_codes):
            writer.writerow([code, current_codes[code], None])
        for code in sorted(historic_codes):
            writer.writerow([code, historic_codes[code]['Title'], historic_codes[code]['Valid Until']])

    network_schema = json_load('data_formats/json/network-schema.json')
    codes = sorted(list(current_codes) + list(historic_codes))
    network_schema['$defs']['Value']['properties']['currency']['enum'] = codes

    json_dump('data_formats/json/network-schema.json', network_schema)

@cli.command()
def update_organisation_identifier_scheme():
  """
  Update organisationIdentifierScheme.csv from org-id.guide.
  """   
   
  reader = csv_load('http://org-id.guide/download.csv')

  with open('schema/codelists/open/organisationIdentifierScheme.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, lineterminator='\n')

    writer.writerow(['Code', 'Title'])
    for code in reader:
      writer.writerow([code['code'], code['name/en'].strip()])


@cli.command()
@click.pass_context
def update_codelists(ctx):
    """
    Update codelists except country.csv.
    """
    ctx.invoke(update_currency)
    ctx.invoke(update_language)
    ctx.invoke(update_media_type)
    ctx.invoke(update_organisation_identifier_scheme)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def format_csv(filename):
    """
    Format a CSV file to conform to the requirements of the tests.
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)


if __name__ == '__main__':
    cli()
