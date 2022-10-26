#!/usr/bin/env python3
from copy import deepcopy
import click
import csv
import glob
import json
import jsonref
import os
import shutil

from flattentool import create_template, flatten
from github import Github
from ocdskit.mapping_sheet import mapping_sheet
from pathlib import Path
from pyairtable import Table
from pyairtable.formulas import match

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_ID = 'apprMa4GXD05csfkW'
GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
EXTERNAL_CODELISTS = ['country.csv', 'currency.csv', 'language.csv', 'mediaType.csv']

basedir = Path(__file__).resolve().parent
codelistdir = basedir / 'codelists'
examplesdir = basedir / 'examples'
referencedir = basedir / 'docs' / 'reference'
schemadir = basedir / 'schema'

def set_value(source_obj, target_obj, source_field, target_field):
    """Update the value of the target object's field if the equivalent field exists in the source object."""
    
    if source_obj.get(source_field):
        target_obj[target_field] = source_obj[source_field]


def read_lines(filename):
    """Read a file and return a list of lines."""

    with open(filename, 'r') as f:
        return f.readlines()


def write_lines(filename, lines):
    """Write a list of lines to a file."""

    with open(filename, 'w') as f:
        f.writelines(lines)


def dereference_object(ref, list):
    """
    Return from list the object referenced by ref. Otherwise, return ref.
    """

    if "id" in ref: # Can remove, `id` is required
        for item in list:
            if item.get("id") == ref["id"]: # Can simplify, `id` is required
                return item

    return ref


def convert_to_feature(object, organisation_references, network, organisations, phases, nodes):
    """
    Convert a node or span to a GeoJSON feature.
    """
    feature = {"type": "Feature"}

    # Set `.geometry`
    # TO-DO: Handle case when publishers add an additional `location` or `route` field to spans and nodes, respectively.
    if "location" in object:
        feature["geometry"] = object.pop("location")
    elif "route" in object:
        feature["geometry"] = object.pop("route")
    else:
        feature["geometry"] = None
    
    properties = feature["properties"] = object
    
    # Dereference organisation references
    for organisationReference in organisation_references:
        if organisationReference in properties:
            properties[organisationReference] == dereference_object(properties[organisationReference], organisations)
    
    # Dereference phase references
    if "phase" in properties:
        properties["phase"] == dereference_object(properties["phase"], phases)

    # Dereference endpoints
    for endpoint in ["start", "end"]:
        if endpoint in properties:
            for node in nodes:
                if "id" in node and node["id"] == properties[endpoint]: # Can simplify, `.id` is required
                    properties[endpoint] = node

    # Embed network-level data
    # TO-DO: Handle case when publishers add an additional `network` field to `Node` or `Span`.
    feature["properties"]["network"] = network

    return feature


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

@click.group()
def cli():
    pass


@cli.command()
def update_from_airtable():
    """Update schema and codelists from Airtable.
    
    * Add new definitions and properties
    * Update existing definitions and properties
    * Delete definitions and properties that do not exist in Airtable or are marked as 'Omit' 
    """

    top_object = 'Network'
    
    with (schemadir / 'network-schema.json').open() as f:
        schema = json.load(f)
    
    # Get data from Airtable
    definitions_table = Table(AIRTABLE_API_KEY, BASE_ID, 'Classes')
    properties_table = Table(AIRTABLE_API_KEY, BASE_ID, 'Properties')
    codelists_table = Table(AIRTABLE_API_KEY, BASE_ID, 'Codelists')
    codes_table = Table(AIRTABLE_API_KEY, BASE_ID, 'Codes')  

    # Update schema
    definitions = {record['id']: record for record in definitions_table.all()}
    for definition_record in definitions.values():
        definition_fields = definition_record['fields']
        
        if definition_fields['Status'] != 'Omit':
            if definition_fields['Name'] == top_object:
                target = schema
            else:
                if definition_fields['Name'] not in schema['definitions']:
                    target = schema['definitions'][definition_fields['Name']] = {}
                else:
                    target = schema['definitions'][definition_fields['Name']]

            set_value(definition_fields, target, "Title", "title")
            set_value(definition_fields, target, "Description", "description")
            set_value(definition_fields, target, "Status", "$comment")
            if "additionalFields" in definition_fields:
                target["additionalFields"] = bool(definition_fields["additionalFields"])
            
            target["type"] = "object"
            
            # Add links to related Github issues
            target['$comment'] = ",".join(definition_fields.get("Github issues",""))

            # Update properties
            if not target.get("properties"):
                target["properties"] = {}
            
            # Clear required fields
            if target.get("required"):
                target["required"] = []

            if definition_fields.get('Properties'):
                for property_id in definition_fields['Properties']:
                    property_record = properties_table.get(property_id)
                    property_fields = property_record['fields']
                    
                    if property_fields['Status'] != 'Omit':
                        
                        # Add new properties or update existing properties
                        if property_fields['Property'] not in target["properties"]:
                            property = target["properties"][property_fields['Property']] = {}
                        else:
                            property = target["properties"][property_fields['Property']]
        
                        # Set values
                        set_value(property_fields, property, "Title", "title")
                        set_value(property_fields, property, "Description", "description")
                        set_value(property_fields, property, "Github issues", "$comment")
                        set_value(property_fields, property, "Format", "format")
                        set_value(property_fields, property, "Type", "type")
                        set_value(property_fields, property, "Constant value", "const")

                        # Add links to related Github issues
                        property['$comment'] = ",".join(property_fields.get("Github issues",""))

                        # Set $ref for objects and arrays of objects
                        if 'instanceOf' in property_fields:
                            ref = definitions[property_fields['instanceOf'][0]]['fields']['Name']

                        if property_fields.get('Type') == 'object':
                            property.pop("type")
                            property['$ref'] = f'#/definitions/{ref}'
                        elif property_fields.get('Type') == 'array':
                            if property_fields.get("Items"):
                                property["items"] = {"type": property_fields["Items"]}
                                if property_fields.get("instanceOf"):
                                    property["items"] = {"$ref": f'#/definitions/{ref}'}
                        
                        # Set codelist, enum and openCodelist
                        if property_fields.get("Codelist"):
                            codelist_record = codelists_table.get(property_fields["Codelist"][0])
                            codelist_fields = codelist_record["fields"]
                            property["codelist"] = f"{codelist_fields['Name']}.csv"
                            
                            if codelist_fields.get("Codelist type") == "Closed":
                                property["openCodelist"] = False
                                property["enum"] = []
                                
                                if codelist_fields.get("Codes"):
                                    for code_id in codelist_fields["Codes"]:
                                        code_record = codes_table.get(code_id)
                                        property["enum"].append(code_record["fields"]["Code"])
                            
                            elif codelist_fields.get("Codelist type") == "Open":
                                property["openCodelist"] = True

                        # Set required properties
                        if property_fields.get("Required") == True:
                            if target.get("required"):
                                if property_fields["Property"] not in target["required"]:
                                    target["required"].append(property_fields["Property"])
                            else:
                                target["required"] = [property_fields["Property"]]

                        target["properties"][property_fields['Property']] = property
            
            # Delete properties not in Airtable
            for property in list(target["properties"]):
                formula = match({"Property": property, "propertyOf": definition_fields["Name"]})
                result = properties_table.first(formula=formula)

                if not result or result["fields"]["Status"] == "Omit":
                    target["properties"].pop(property)

    # Delete definitions not in Airtable
    for definition in list(schema["definitions"]):
        formula = match({"Name": definition})
        result = definitions_table.first(formula=formula)

        if not result or result["fields"]["Status"] == "Omit":
            schema["definitions"].pop(definition)

    with (schemadir / 'network-schema.json').open('w') as f:
        json.dump(schema, f, indent=2)
        f.write('\n')
    
    # Update codelists
    files = glob.glob(f"{codelistdir}/*/*.csv")
    for file in files:
      
      # Don't delete codelists that are managed outside of Airtable
      if file.split("/")[-1] not in EXTERNAL_CODELISTS:
        os.remove(file)
    
    for codelist in codelists_table.all():
        codelist_fields = codelist["fields"]
        
        if codelist_fields["Status"] != "Omit" and codelist_fields.get("Codes"):
            filename = f"{codelist_fields['Name']}.csv"
            
            if codelist_fields.get("Codelist type") == "Closed":
                subdir = "closed"
            else:
                subdir = "open"

            with open(codelistdir / subdir / filename, 'w', newline='') as f:
                fieldnames = ['code', 'title', 'description']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for code_id in codelist_fields['Codes']:
                    code_record = codes_table.get(code_id)
                    code_fields = code_record['fields']

                    if code_fields["Status"] not in ["Omit","Further clarification needed"]:

                        writer.writerow({
                            'code': code_fields.get("Code", ""),
                            'title': code_fields.get("Title", ""),
                            'description': code_fields.get("Description", "")
                        })

def get_issues(issue_urls):
    """
    Accepts a comma-separated list of issue urls and returns issues from the Github API.
    """
    github = Github(GITHUB_ACCESS_TOKEN)
    repo = github.get_repo("Open-Telecoms-Data/open-fibre-data-standard")
    issues = []

    for issue_url in set(issue_urls.split(",")):
        issues.append(repo.get_issue(number=int(issue_url.split("/")[-1])))
    
    return issues 


def update_csv_docs():
  """Update docs/reference/publication_formats/csv.md"""

  jsonref_schema = json_load('network-schema.json', jsonref)
  dereferenced_schema = get_dereferenced_schema(jsonref_schema)

  markdown = generate_csv_reference_markdown('networks', dereferenced_schema)

  static_content = []

  with open(referencedir / 'publication_formats' / 'csv.md', 'r') as f:
    for line in f:
      if line == '## Networks\n':
        break
      else:
        static_content.append(line)

  with open(referencedir / 'publication_formats' / 'csv.md', 'w') as f:
    f.writelines(static_content)

    for key, value in markdown.items():
      f.write(f"\n{'#'*value['depth']} {key}\n\n")
      f.writelines(value['content'])


def generate_csv_reference_markdown(table, schema, parents=None, depth=2):
  """
  Recursively generate reference documentation for each table in the CSV publication format.
  
  :param table: the name of the table
  :param schema: the schema for the object represented by the table
  :param parents: a list of the parents of the object represented by the table
  :param depth: the depth in the JSON schema hierarchy of the object represented by the table
  """

  markdown = {}
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
      f" * [{parents[-1]}](#{parents[-1].lower()}): many-to-one by `{parent_ref + '/0/' if len(parent_ref) > 0 else ''}id`\n"
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
        f" * [{key}](#{key.lower()}): one-to-many by `{'id' if table == 'networks' else '/0/'.join(parents[1:] + [table, 'id'])}`\n"
      )
      markdown.update(generate_csv_reference_markdown(key, value, parents + [table], depth + 1))
    else:
      include_pointers.append(f"{parent_ref}{'/0/' if len(parent_ref) > 0 else ''}{table+'/0/' if len(parents)>0 else ''}{key}")

  # Generate links to examples and templates
  table_name = '_'.join(parents[1:] + [table])
  markdown[table]['content'].append(f"\nThe fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/{table_name}.csv) or a [blank template](../../../examples/csv/template/{table_name}.csv) for this table.\n\n")

  # Generate jsonschema directive
  markdown[table]['content'].extend([
    "```{jsonschema} ../../../schema/network-schema.json\n"
    f":include: {','.join(include_pointers)}\n"
    "```\n"
  ])

  return markdown


@cli.command()
def pre_commit():
    """Update derivative schema files, examples and reference documentation:
      - network-schema.csv
      - examples/csv/template
      - examples/csv
      - reference/publication_formats/csv.md
    """

    # Load schema
    schema = json_load('network-schema.json')
     
    # Generate network-schema.csv
    schema_table = mapping_sheet(schema, include_codelist=True, include_definitions=True)

    with (schemadir / 'network-schema.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=schema_table[0])
        
        writer.writeheader()
        for row in schema_table[1]:
            writer.writerow(row)
    
    # Update examples/csv
    delete_directory_contents('examples/csv')
    flatten(
      input_name='examples/json/network-package.json',
      schema='schema/network-schema.json',
      output_name='examples/csv',
      output_format='csv',
      main_sheet_name="networks",
      truncation_length=9,
      root_list_path='networks'
    )

    # Update examples/csv/template
    create_template(
      schema='schema/network-schema.json',
      output_name='examples/csv/template',
      output_format="csv",
      main_sheet_name="networks",
      truncation_length=9,
      no_deprecated_fields=True
    )

    # Update docs/reference/publication_formats/csv.md
    update_csv_docs()


def get_references(schema, defn, parents=None, network_schema=None):
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
        if value['items']['$ref'] == f"#/definitions/{defn}":
          references.append(parents + [key, '0'])
        else:
          references.extend(get_references(network_schema['definitions'][value['items']['$ref'].split('/')[-1]], defn, parents + [key, '0'], network_schema))
      elif '$ref' in value:
        if value['$ref'] == f"#/definitions/{defn}":
          references.append(parents + [key])
        else:
          references.extend(get_references(network_schema['definitions'][value['$ref'].split('/')[-1]], defn, parents + [key], network_schema))
      elif 'properties' in value:
          references.extend(get_references(value, defn, parents + [key], network_schema))

  if 'definitions' in schema:
    for key, value in schema['definitions'].items():
      references.extend(get_references(value, defn, [key], network_schema))
  
  return references


@cli.command()
def update_reference_docs():
    """Update reference documentation:
      - docs/reference/schema.md
      - docs/reference/codelists.md
    """    
    
    # Load schema
    schema = json_load('network-schema.json')

    # Get list of references 
    references = {}
    for defn in schema['definitions']:
      references[defn] = get_references(schema, defn)

    # Load schema reference
    schema_reference = read_lines(referencedir / 'schema.md')

    # Get content from components section of schema reference
    components_index = schema_reference.index("### Components\n") + 3

    for i in range(components_index, len(schema_reference)):
        if schema_reference[i][:5] == "#### ":
            defn = schema_reference[i][5:-1]
            
            if defn in schema["definitions"]:
                schema["definitions"][defn]["content"] = []
                j = i+1

                # Drop auto-generated reference content
                while j < len(schema_reference) and not schema_reference[j].startswith("```{admonition}") and not schema_reference[j].startswith(f"`{defn}"):
                    schema["definitions"][defn]["content"].append(schema_reference[j])
                    j = j+1

    # Generate standard reference content for each definition
    for defn, definition in schema["definitions"].items():
        definition["content"] = definition.get("content", [])
        
        # Add heading
        definition["content"].insert(0, f"#### {defn}\n")
        
        # Get Github issues and list related definitions and properties
        definition["issues"] = {}
        if definition.get("$comment"):
            for issue in get_issues(definition["$comment"]):
                definition["issues"][issue.url] = {"issue": issue, "relatedTo": [defn]}
        
        for prop, property in definition["properties"].items():
            if property.get("$comment"):
                for issue in get_issues(property["$comment"]):
                    if issue.url in definition["issues"]:
                        definition["issues"][issue.url]["relatedTo"].append(f".{prop}")
                    else:
                        definition["issues"][issue.url] = {"issue": issue, "relatedTo": [f".{prop}"]}
          
        # Add admonition with list of related Github issues
        if len(definition["issues"]) > 0:
            definition["content"].extend([
                "```{admonition} Alpha consultation\n",
                "The following issues relate to this component or its fields:\n"
            ])
            for issue in definition["issues"].values():
                definition["content"].extend([
                    f"* `{'`, `'.join(issue['relatedTo'])}`: [#{issue['issue'].number} {issue['issue'].title}]({issue['issue'].html_url})\n"
                ])
            definition["content"].append("```\n\n")

        # Add a list of references.
        definition["content"].append("This component is referenced by the following properties:\n")

        for ref in references[defn]:
            # Remove array indices because they do not appear in the HTML anchors generated by the json schema directive
            ref = [part for part in ref if part != '0']
            # Ideally, these would be relative links - see https://github.com/OpenDataServices/sphinxcontrib-opendataservices/issues/43
            definition["content"].append(f"* [`{'/'.join(ref)}`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,{'/definitions/' if len(ref) > 1 else ','}{','.join(ref)})\n")
                
        # Add definition and schema table
        definition["content"].extend([
            f"\n\n`{defn}` is defined as:\n\n",
            "```{jsoninclude-quote} ../../schema/network-schema.json\n",
            f":jsonpointer: /definitions/{defn}/description\n",
            "```\n\n",
            f"Each `{defn}` has the following fields:\n\n", 
            "::::{tab-set}\n\n",
            ":::{tab-item} Schema\n\n",
            "```{jsonschema} ../../schema/network-schema.json\n",
            f":pointer: /definitions/{defn}\n",
            f":collapse: {','.join(definition['properties'].keys())}\n"
            "```\n\n",
            ":::\n\n",
            ":::{tab-item} Examples\n\n"
        ])

        # Add examples
        for ref in references[defn]:
          if ref[0] not in schema['definitions']:
            if ref[-1] == '0':
              ref.pop(-1)
            
            definition["content"].extend([
              "```{eval-rst}\n",
              ".. jsoninclude:: ../../examples/json/network-package.json\n",
              f" :jsonpointer: /networks/0/{'/'.join(ref)}\n",
              f" :title: {'/'.join(ref)}\n",
              "```\n\n"
            ])

        definition["content"].extend([          
            ":::\n\n",
            "::::\n\n"
        ])
      
    # Update schema reference
    schema_reference = schema_reference[:components_index+1]
    schema_reference.append("\n")
    
    for definition in schema["definitions"].values():
        schema_reference.extend(definition["content"])

    write_lines(referencedir / 'schema.md', schema_reference)

    # Load codelist reference
    codelist_reference = read_lines(referencedir / 'codelists.md')

    # Get codelists from the codelist directory
    codelists = {}
    for path in glob.glob(f"{codelistdir}/*/*.csv"):
        codelists[(path.split("/")[-1].split(".")[0])] = {"type": path.split("/")[-2], "reference": []}

    # Get codelists from codelist reference, drop any missing from the codelist directory
    codelists_index = codelist_reference.index("## Open codelists\n")
    for i in range(0, len(codelist_reference)):
        line = codelist_reference[i]       
        
        if line[:4] == "### ":
            codelist = line[4:-1]
            
            if codelist in codelists:
                j = i+1
                
                while j < len(codelist_reference) and codelist_reference[j][:2] != "##":
                    codelists[codelist]["reference"].append(codelist_reference[j])
                    j += 1

    # Add new codelists and update codelist reference
    codelist_reference = codelist_reference[:codelists_index-1]
    codelist_reference.append("\n")
    open_reference = ["## Open codelists\n", "\n"]
    closed_reference = ["## Closed codelists\n", "\n"]
    
    for key, value in codelists.items():
        if value["type"] == "closed":
            target = closed_reference
        else:
            target = open_reference
        if value["reference"] == []:
            value["reference"].extend([
                "\n",
                "```{csv-table-no-translate}\n",
                ":header-rows: 1\n",
                ":widths: auto\n",
                f":file: ../../codelists/{value['type']}/{key}.csv\n",
                "```\n",
                "\n"       
            ])
        target.append(f"### {key}\n")
        target.extend(value["reference"])
    
    codelist_reference.extend(open_reference)
    codelist_reference.extend(closed_reference)

    write_lines(referencedir / 'codelists.md', codelist_reference)

@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def convert_to_geojson(filename):
    """
    Convert a network package to two GeoJSON files: nodes.geojson and spans.geojson.
    """

    # Load data
    with open(filename, 'r') as f:
        package = json.load(f)

    nodeFeatures = []
    spanFeatures = []
    
    for network in package["networks"]:
      nodes = network.pop("nodes", [])
      spans = network.pop("spans", [])
      # TO-DO: Consider how to handle unreferenced phases and organisations. Currently, they are dropped from the geoJSON output
      phases = network.pop("phases", [])
      organisations = network.pop("organisations", [])

      # Dereference `contracts.relatedPhases`
      if "contracts" in network:
          for contract in network["contracts"]:
              if "relatedPhases" in contract:
                  for phase in contract["relatedPhases"]:
                      phase = dereference_object(phase, phases)

      # Convert nodes to features
      for node in nodes:
          nodeFeatures.append(convert_to_feature(node, ['physicalInfrastructureProvider', 'networkProvider'], network, organisations, phases, nodes))

      # Convert spans to features
      for span in spans:
          spanFeatures.append(convert_to_feature(span, ['physicalInfrastructureProvider', 'networkProvider'], network, organisations, phases, nodes))

    with open('nodes.geojson', 'w') as f:
        featureCollection = {
            "type": "FeatureCollection",
            "features": nodeFeatures
        }
        json.dump(featureCollection, f, indent=2)

    with open('spans.geojson', 'w') as f:
        featureCollection = {
            "type": "FeatureCollection",
            "features": spanFeatures
        }
        json.dump(featureCollection, f, indent=2)

if __name__ == '__main__':
    cli()
