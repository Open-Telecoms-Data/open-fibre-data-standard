#!/usr/bin/env python3
import click
import json
import os

from pathlib import Path
from pyairtable import Table

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_ID = 'apprMa4GXD05csfkW'

basedir = Path(__file__).resolve().parent
schemadir = basedir / 'schema'

def set_value(source_obj, target_obj, source_field, target_field):
    """Update the value of the target object's field if the equivalent field exists in the source object."""
    if source_obj.get(source_field):
        target_obj[target_field] = source_obj[source_field]


@click.group()
def cli():
    pass


@cli.command()
def update_schema():
    """Update network-schema.json from Airtable."""
    top_object = 'Network'
    
    with (schemadir / 'network-schema.json').open() as f:
        schema = json.load(f)

    # Get definitions from Airtable
    definitions_table = Table(AIRTABLE_API_KEY, BASE_ID, 'Classes')
    definitions = {record['id']: record for record in definitions_table.all()}

    # Update top-object and definitions
    for record in definitions.values():
        source = record['fields']
        
        if source['Status'] != 'Omit':
            if source['Name'] == top_object:
                target = schema
            else:
                if source['Name'] not in schema['definitions']:
                    target = schema['definitions'][source['Name']] = {}
                else:
                    target = schema['definitions'][source['Name']]

                set_value(source, target, "Title", "title")
                set_value(source, target, "Description", "description")
                set_value(source, target, "Status", "$comment")
                target["type"] = "object"
                target["properties"] = {}

    # Get properties from Airtable
    properties_table = Table(AIRTABLE_API_KEY, BASE_ID, 'Properties')
    properties = {record['id']: record for record in properties_table.all()}

    # Update properties
    for record in properties.values():
        source = record['fields']
        definition = definitions[source['propertyOf'][0]]['fields']['Name']

        if source['Status'] != 'Omit':
            if definition == top_object:
                target_list = schema['properties']
            else:
                target_list = schema['definitions'][definition]['properties']

            if source['Property'] not in target_list:
                target = target_list[source['Property']] = {}
            else:
                target = target_list[source['Property']]

            # Delete keys not in Airtable
            for key in list(target):
                if key not in source:
                    del(target[key])
        
            set_value(source, target, "Title", "title")
            set_value(source, target, "Description", "description")
            set_value(source, target, "Status", "$comment")
            set_value(source, target, "Format", "format")

            if 'instanceOf' in source:
                ref = definitions[source['instanceOf'][0]]['fields']['Name']

            if source.get('Type') == 'object':
                target["type"] = "object",
                target['$ref'] = f'#/definitions/{ref}'
            elif source.get('Type') == 'array (string)':
                target["type"] = "array"
                target["items"] = {"type": "string"}
            elif source.get('Type') == 'array (object)':
                target["type"] = "array"
                target["items"] = {"$ref": f'#/definitions/{ref}'}

            target_list[source['Property']] = target

    with (schemadir / 'network-schema.json').open('w') as f:
        json.dump(schema, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    cli()
