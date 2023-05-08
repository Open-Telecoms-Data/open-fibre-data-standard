#!/usr/bin/env python3
from copy import deepcopy
import click
import csv
import glob
import json
import jsonref
import logging
import os
import re
import requests
import shutil
import subprocess

from collections import OrderedDict
from contextlib import contextmanager
from flattentool import create_template, flatten
from io import StringIO
from lxml import etree
from ocdskit.mapping_sheet import mapping_sheet
from pathlib import Path

basedir = Path(__file__).resolve().parent
codelistdir = basedir / 'codelists'
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
  """Update docs/reference/publication_formats/csv.md"""

  # Load csv reference
  csv_reference = read_lines(referencedir / 'publication_formats' / 'csv.md')

  # Preserve introductory content up to the ## networks heading
  csv_reference = csv_reference[:csv_reference.index("## networks\n") - 1]

  # Generate CSV reference
  dereferenced_schema = get_dereferenced_schema(jsonref_schema)
  markdown = generate_csv_reference_markdown('networks', dereferenced_schema)
 
  for key, value in markdown.items():
    csv_reference.append(f"\n{'#'*value['depth']} {key}\n\n")
    csv_reference.extend(value['content'])

  write_lines(referencedir / 'publication_formats' / 'csv.md', csv_reference)

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
        f" * [{key if table == 'networks' else f'{table}_{key}'}](#{key if table == 'networks' else f'{table}_{key}'.lower()}): one-to-many by `{'id' if table == 'networks' else '/0/'.join(parents[1:] + [table, 'id'])}`\n"
      )
      markdown.update(generate_csv_reference_markdown(key, value, parents + [table], depth + 1))
    else:
      include_pointers.append(f"{parent_ref}{'/0/' if len(parent_ref) > 0 else ''}{table.split('_')[-1]+'/0/' if len(parents)>0 else ''}{key}")

  # Generate links to examples and templates
  markdown[table]['content'].append(f"\nThe fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/{table}.csv) or a [blank template](../../../examples/csv/template/{table}.csv) for this table.\n\n")

  # Generate jsonschema directive
  markdown[table]['content'].extend([
    "```{jsonschema} ../../../schema/network-schema.json\n"
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
        if value['items']['$ref'] == f"#/definitions/{defn}":
          references.append(parents + [key, '0'])
        else:
          references.extend(get_definition_references(network_schema['definitions'][value['items']['$ref'].split('/')[-1]], defn, parents + [key, '0'], network_schema))
      elif '$ref' in value:
        if value['$ref'] == f"#/definitions/{defn}":
          references.append(parents + [key])
        else:
          references.extend(get_definition_references(network_schema['definitions'][value['$ref'].split('/')[-1]], defn, parents + [key], network_schema))
      elif 'properties' in value:
          references.extend(get_definition_references(value, defn, parents + [key], network_schema))

  if 'definitions' in schema:
    for key, value in schema['definitions'].items():
      references.extend(get_definition_references(value, defn, [key], network_schema))
  
  return references


def get_codelist_references(schema, codelist, parents=None, network_schema=None):
  """
  Recursively generate a list of JSON pointers that reference a codelist in JSON schema.

  :param schema: The JSON schema
  :codelist: The name of the definition
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
      if value.get('codelist') == f"{codelist}.csv":
        references.append(parents + [key])
      elif value.get('type') == 'array' and '$ref' in value['items']:
        references.extend(get_codelist_references(network_schema['definitions'][value['items']['$ref'].split('/')[-1]], codelist, parents + [key, '0'], network_schema))
      elif '$ref' in value:
        references.extend(get_codelist_references(network_schema['definitions'][value['$ref'].split('/')[-1]], codelist, parents + [key], network_schema))
      elif 'properties' in value:
          references.extend(get_codelist_references(value, codelist, parents + [key], network_schema))

  if 'definitions' in schema:
    for key, value in schema['definitions'].items():
      references.extend(get_codelist_references(value, codelist, [key], network_schema))
  
  return references


def generate_codelist_markdown(codelist, type, references, definitions):
  """Generate reference markdown for codelist"""

  markdown = ["This codelist is referenced by the following properties:\n\n"]

  for ref in references:   
    # Remove array indices because they do not appear in the HTML anchors generated by the json schema directive
    ref = [part for part in ref if part != '0']
    
    # Ideally, these would be relative links - see https://github.com/OpenDataServices/sphinxcontrib-opendataservices/issues/43
    url = 'https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,'
    
    # Omit nested references
    if ref[0] in definitions and len(ref) == 2:
      url += '/definitions/'
    elif len(ref) == 1:
      url += ','
    else:
      continue
    
    url += ','.join(ref)
    markdown.append(f"- [`{'/'.join(ref)}`]({url})\n")

  markdown.extend([
    "\nThis codelist has the following codes:\n\n"
    "```{csv-table-no-translate}\n",
    ":header-rows: 1\n",
    ":widths: auto\n",
    f":file: ../../codelists/{type}/{codelist}.csv\n",
    "```\n\n"
  ])

  return markdown


def update_codelist_docs(schema):
  """Update docs/reference/codelists.md"""

  # Load codelist reference
  codelist_reference = read_lines(referencedir / 'codelists.md')

  # Get codelist names and types (open or closed) from the codelist directory and get a list of references for each codelist
  codelists = {}
  for path in glob.glob(f"{codelistdir}/*/*.csv"):
      codelist = path.split("/")[-1].split(".")[0]
      codelists[codelist] = {
        "type": path.split("/")[-2],
        "content": [f"### {codelist}\n",],
        "references": get_codelist_references(schema, codelist)
        }
  
  # Sort codelists alphabetically
  codelists = OrderedDict(sorted(codelists.items()))

  # Preserve content that appears before the generated reference content for each codelist 
  for i in range(0, len(codelist_reference)):
      line = codelist_reference[i]       
      
      if line[:4] == "### ":
          codelist = line[4:-1]
          
          # Drop codelists that don't appear in the codelists directory 
          if codelist in codelists:
              j = i+1
              
              while j < len(codelist_reference) and codelist_reference[j] != "This codelist is referenced by the following properties:\n":
                  codelists[codelist]["content"].append(codelist_reference[j])
                  j += 1

  # Preserve introductory content up to an including the ## Open codelists heading
  codelist_reference = codelist_reference[:codelist_reference.index("## Open codelists\n") + 1]
  codelist_reference.append("\n")

  # Update reference for open and closed codelists
  closed_codelist_reference = ["## Closed codelists\n\n"]
  
  for key, value in codelists.items():
    value['content'].extend(generate_codelist_markdown(key, value['type'], value['references'], schema['definitions']))
    if value["type"] == "open":
        codelist_reference.extend(value['content'])
    else:
        closed_codelist_reference.extend(value['content'])
    
  codelist_reference.extend(closed_codelist_reference)

  write_lines(referencedir / 'codelists.md', codelist_reference)


def update_schema_docs(schema):
  """Update docs/reference/schema.md"""    

  # Load schema reference
  schema_reference = read_lines(referencedir / 'schema.md')

  # Preserve content that appears before the generated reference content for each component
  components_index = schema_reference.index("### Components\n") + 3

  for i in range(components_index, len(schema_reference)):
      if schema_reference[i][:5] == "#### ":
          defn = schema_reference[i][5:-1]
          
          # Drop definitions that don't appear in the schema
          if defn in schema["definitions"]:
              schema["definitions"][defn]["content"] = []
              j = i+1

              # while j < len(schema_reference) and not schema_reference[j].startswith("```{admonition}") and schema_reference[j] != 'This component is referenced by the following properties:\n':
              while j < len(schema_reference) and not schema_reference[j].startswith("```{admonition}") and schema_reference[j] != f"`{defn}` is defined as:\n":
                schema["definitions"][defn]["content"].append(schema_reference[j])
                j = j+1

  # Preserve introductory content up to and including the sentence below the ### Components heading
  schema_reference = schema_reference[:components_index]
  schema_reference.append("\n")
    
  # Generate standard reference content for each definition
  for defn, definition in schema["definitions"].items():
      definition["content"] = definition.get("content", [])
      
      # Add heading
      definition["content"].insert(0, f"#### {defn}\n")
                         
      # Add description
      definition["content"].extend([
          f"`{defn}` is defined as:\n\n",
          "```{jsoninclude-quote} ../../schema/network-schema.json\n",
          f":jsonpointer: /definitions/{defn}/description\n",
          "```\n\n"
      ])

      # Add a list of properties that reference this definition
      definition["references"] = get_definition_references(schema, defn)
      definition["content"].append("This component is referenced by the following properties:\n\n")

      for ref in definition["references"]:
          # Remove array indices because they do not appear in the HTML anchors generated by the json schema directive
          ref = [part for part in ref if part != '0']

          # Ideally, these would be relative links - see https://github.com/OpenDataServices/sphinxcontrib-opendataservices/issues/43
          url = 'https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,'
          
          # Omit nested references
          if ref[0] in schema['definitions'] and len(ref) == 2:
            url += '/definitions/'
          elif len(ref) == 1:
            url += ','
          else:
            continue
    
          url += ','.join(ref)
          definition["content"].append(f"- [`{'/'.join(ref)}`]({url})\n")

      # Add schema table
      definition["content"].extend([
          f"\nEach `{defn}` has the following fields:\n\n", 
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
      for ref in definition["references"]:
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

      schema_reference.extend(definition["content"])     

  write_lines(referencedir / 'schema.md', schema_reference) 

@click.group()
def cli():
    pass


@cli.command()
def pre_commit():
    """Update derivative schema files, examples and reference documentation:
      - network-schema.csv
      - examples/csv/template
      - examples/csv
      - reference/publication_formats/csv.md
      - reference/codelists.md
      - reference/schema.md
      - examples/geojson/nodes.geojson
      - examples/geojson/spans.geojson
      Also run:
      - mdformat
    """

    # Load schema
    schema = json_load('network-schema.json')
    jsonref_schema = json_load('network-schema.json', jsonref)
     
    # Generate network-schema.csv
    schema_table = mapping_sheet(schema, include_codelist=True, include_definitions=False)

    with (schemadir / 'network-schema.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=schema_table[0], lineterminator='\n')
        
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
      root_list_path='networks',
      line_terminator='LF',
    )

    # Update examples/csv/template
    create_template(
      schema='schema/network-schema.json',
      output_name='examples/csv/template',
      output_format="csv",
      main_sheet_name="networks",
      truncation_length=9,
      no_deprecated_fields=True,
      line_terminator='LF',
    )

    # Use WKT geometry in CSV examples and templates. This code should be removed once Flatten Tool supports WKT
    replacements = {
       'examples/csv/nodes.csv': [
          ('nodes/0/location/type,nodes/0/location/coordinates','nodes/0/location'),
          ('Point,-0.174;5.625', 'POINT (-0.174 5.625)'),
          ('Point,-1.628;6.711', 'POINT (-1.628 6.711)')
       ],
       'examples/csv/template/nodes.csv': [
          ('nodes/0/location/type,nodes/0/location/coordinates','nodes/0/location')
       ],
       'examples/csv/spans.csv': [
          ('spans/0/route/type,spans/0/route/coordinates','spans/0/route'),
          ('LineString,"-0.173,5.626;-0.178,5.807;-0.112,5.971;-0.211,5.963;-0.321,6.17;-0.488,6.29;-0.56,6.421;-0.752,6.533;-0.867,6.607;-1.101,6.585;-1.304,6.623;-1.461,6.727;-1.628,6.713"', '"LINESTRING (-0.173 5.626,-0.178 5.807,-0.112 5.971,-0.211 5.963,-0.321 6.17,-0.488 6.29,-0.56 6.421,-0.752 6.533,-0.867 6.607,-1.101 6.585,-1.304 6.623,-1.461 6.727,-1.628 6.713)"')
       ],
       'examples/csv/template/spans.csv': [
          ('spans/0/route/type,spans/0/route/coordinates','spans/0/route')
       ]
    }
    
    for key, value in replacements.items():
      with open(key, 'r') as f:
         content = f.read()
      
      for replacement in value:
         content = content.replace(replacement[0], replacement[1])
      
      with open(key, 'w') as f:
         f.write(content)

    # Update docs/reference/publication_formats/csv.md
    update_csv_docs(jsonref_schema)

    # Update docs/reference/codelists.md
    update_codelist_docs(schema)

    # Update docs/reference/schema.md
    update_schema_docs(schema)

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

    with csv_dump('codelists/open/mediaType.csv', ['Code', 'Title']) as writer:
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

    with csv_dump('codelists/open/language.csv', ['Code', 'Title']) as writer:
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

    with open('codelists/closed/country.csv', 'w') as f:
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

    with csv_dump('codelists/closed/currency.csv', ['Code', 'Title', 'Valid Until']) as writer:
        for code in sorted(current_codes):
            writer.writerow([code, current_codes[code], None])
        for code in sorted(historic_codes):
            writer.writerow([code, historic_codes[code]['Title'], historic_codes[code]['Valid Until']])

    network_schema = json_load('network-schema.json')
    codes = sorted(list(current_codes) + list(historic_codes))
    network_schema['definitions']['Value']['properties']['currency']['enum'] = codes

    json_dump('network-schema.json', network_schema)

@cli.command()
def update_organisation_identifier_scheme():
  """
  Update organisationIdentifierScheme.csv from org-id.guide.
  """   
   
  reader = csv_load('http://org-id.guide/download.csv')

  with open('codelists/open/organisationIdentifierScheme.csv', 'w', encoding='utf-8') as f:
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


if __name__ == '__main__':
    cli()
