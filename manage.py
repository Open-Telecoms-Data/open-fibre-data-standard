#!/usr/bin/env python3
from copy import deepcopy
import click
import csv
import glob
import json
import os

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

@cli.command()
def pre_commit():
    """Update the following files based on the network-schema.json and codelist CSVs:
      - network-schema.csv
      - docs/reference/schema.md
      - docs/reference/codelists.md
    """

    # Load schema
    with (schemadir / 'network-schema.json').open() as f:
        schema = json.load(f)
     
    # Generate network-schema.csv
    schema_table = mapping_sheet(schema, include_codelist=True, include_definitions=True)

    with (schemadir / 'network-schema.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=schema_table[0])
        
        writer.writeheader()
        for row in schema_table[1]:
            writer.writerow(row)

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
            definition["content"].append("```\n")

        # Add definition and schema table
        definition["content"].extend([
            f"`{defn}` is defined as:\n",
            "```{jsoninclude-quote} ../_build/dirhtml/_schema/network-schema.json\n",
            f":jsonpointer: /definitions/{defn}/description\n",
            "```\n",
            f"Each `{defn}` has the following fields:\n", 
            "```{jsonschema} ../_build/dirhtml/_schema/network-schema.json\n",
            f":pointer: /definitions/{defn}\n",
            f":collapse: {','.join(definition['properties'].keys())}\n"
            "```\n",
            "\n"
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
