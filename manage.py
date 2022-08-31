#!/usr/bin/env python3
import click
import csv
import glob
import json
import os

from ocdskit.mapping_sheet import mapping_sheet
from pathlib import Path
from pyairtable import Table

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_ID = 'apprMa4GXD05csfkW'

basedir = Path(__file__).resolve().parent
schemadir = basedir / 'schema'
referencedir = basedir / 'docs' / 'reference'
codelistdir = basedir / 'codelists'

def set_value(source_obj, target_obj, source_field, target_field):
    """Update the value of the target object's field if the equivalent field exists in the source object."""
    if source_obj.get(source_field):
        target_obj[target_field] = source_obj[source_field]


def read_markdown(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def write_markdown(filename, lines):
    with open(filename, 'w') as f:
        f.writelines(lines)


@click.group()
def cli():
    pass


@cli.command()
def update_from_airtable():
    """Update schema and codelists from Airtable."""
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
            target["type"] = "object"
            
            # Update properties
            if not target.get("properties"):
                target["properties"] = {}

            if definition_fields.get('Properties'):
                for property_id in definition_fields['Properties']:
                    property_record = properties_table.get(property_id)
                    property_fields = property_record['fields']
                    
                    if property_fields['Status'] != 'Omit':
                        if property_fields['Property'] not in target["properties"]:
                            property = target["properties"][property_fields['Property']] = {}
                        else:
                            property = target["properties"][property_fields['Property']]
        
                        set_value(property_fields, property, "Title", "title")
                        set_value(property_fields, property, "Description", "description")
                        set_value(property_fields, property, "Status", "$comment")
                        set_value(property_fields, property, "Format", "format")

                        if 'instanceOf' in property_fields:
                            ref = definitions[property_fields['instanceOf'][0]]['fields']['Name']

                        if property_fields.get('Type') == 'object':
                            property["type"] = "object",
                            property['$ref'] = f'#/definitions/{ref}'
                        elif property_fields.get('Type') == 'array (string)':
                            property["type"] = "array"
                            property["items"] = {"type": "string"}
                        elif property_fields.get('Type') == 'array (object)':
                            property["type"] = "array"
                            property["items"] = {"$ref": f'#/definitions/{ref}'}
                        
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

                        target["properties"][property_fields['Property']] = property

                # Delete keys not in Airtable
                for key in list(property):
                    if key not in property_fields:
                        del(property[key])
        
    with (schemadir / 'network-schema.json').open('w') as f:
        json.dump(schema, f, indent=2)
        f.write('\n')
    
    # Update codelists
    for codelist in codelists_table.all():
        codelist_fields = codelist["fields"]
        
        if codelist_fields["Status"] != "Omit" and codelist_fields.get("Codes"):
            filename = f"{codelist_fields['Name']}.csv"
            
            with open(codelistdir / filename, 'w', newline='') as f:
                fieldnames = ['code', 'title', 'description']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for code_id in codelist_fields['Codes']:
                    code_record = codes_table.get(code_id)
                    code_fields = code_record['fields']

                    if code_fields["Status"] != "Omit":

                        writer.writerow({
                            'code': code_fields.get("Code", ""),
                            'title': code_fields.get("Title", ""),
                            'description': code_fields.get("Description", "")
                        })


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
        writer = csv.writer(f)
        for row in schema_table:
            writer.writerow(row)

    # Update schema reference
    schema_reference = read_markdown(referencedir / 'schema.md')

    for key, value in schema["definitions"].items():
        heading = f"#### {key}\n"
        
        if heading not in schema_reference:
            schema_reference.extend([
                heading,
                "\n", 
                "```{jsonschema} ../../schema/network-schema.json\n",
                f":pointer: /definitions/{key}\n",
                f":collapse: {','.join(value['properties'].keys())}\n"
                "```\n",
                "\n"
            ])

    write_markdown(referencedir / 'schema.md', schema_reference)

    # Update codelist reference
    codelist_reference = read_markdown(referencedir / 'codelists.md')

    for path in glob.glob(f"{codelistdir}/*"):
        codelist = path.split("/")[-1].split(".")[0]
        heading = f"### {codelist}\n"

        if heading not in codelist_reference:
            codelist_reference.extend([
                heading,
                "\n",
                "```{csv-table-no-translate}\n",
                ":header-rows: 1\n",
                ":widths: auto\n",
                f":file: ../../codelists/{codelist}.csv\n",
                "```\n",
                "\n"
            ])

    write_markdown(referencedir / 'codelists.md', codelist_reference)

if __name__ == '__main__':
    cli()