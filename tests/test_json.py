from warnings import warn
from collections import Counter
from jscc.testing.checks import get_empty_files, get_misindented_files, get_invalid_json_files
from jscc.testing.util import warn_and_assert
from jscc.testing.filesystem import walk_json_data, walk_csv_data
from jscc.schema import is_json_schema
from jscc.testing.checks import validate_items_type, validate_letter_case, validate_schema

import pytest
import os
import json


this_dir = os.path.dirname(os.path.realpath(__file__))
absolute_source_schema_dir = this_dir + '/../schema/'
absolute_source_codelist_dir = this_dir + '/../codelists/'


def test_empty():
    """Tests that files (JSON and other files) are not empty."""
    empty_files_paths = [path for path in get_empty_files() if "src/" not in path[0]]
    warn_and_assert(empty_files_paths, "{0} is empty, run: rm {0}", "Files are empty. See warnings below.")


def test_indent():
    """
    Test that JSON files are indented properly.
    Note this test can often fail on problems that are not to do with indents.
    """
    misindented_files_paths = [path for path in get_misindented_files() if "src/" not in path[0]]
    warn_and_assert(
        misindented_files_paths,
        "{0} is not indented as expected",
        "Files are not indented as expected. See warnings below",
    )


def test_invalid_json():
    """Test whether all JSON files can be parsed."""
    warn_and_assert(
        get_invalid_json_files(excluded=('.git', '.ve', '_static', 'build', 'fixtures', "_build")), "{0} is not valid JSON: {1}", "JSON files are invalid. See warnings below."
    )


schemas = [(path, name, data) for path, name, _, data in walk_json_data(top=absolute_source_schema_dir) if is_json_schema(data) and not path.endswith('tests/schema/meta-schema.json')]
# with open(os.path.join(this_dir, 'schema', 'meta-schema.json')) as fp:
#     metaschema = json.load(fp)


# @pytest.mark.parametrize("path,name,data", schemas)
# def test_schema_valid(path, name, data):

#     # skip schemas generated by tests for now
#     if "schema/testing" in path or "src/" in path:
#         return
#     validate_json_schema(path, name, data, metaschema)


@pytest.mark.parametrize("path,name,data", schemas)
def test_codelist_enums(path, name, data):
    """
    Make sure the codes in the codelist CSVs match the equivalent enums in the schema.
    """
    if "src/" in path:
        return

    errors = 0

    codelist_codes = collect_codelist_codes()
    codelist_info = collect_codelist_enums(path, data)

    for codelist_file, codes in codelist_codes.items():
        if codelist_file in codelist_info:
            codelist_enum = codelist_info[codelist_file][0]
            open_codelist = codelist_info[codelist_file][1]
            if not open_codelist and Counter(codelist_enum) != Counter(codes):
                errors += 1
                warn("""Codelist mismatch:\n
                    {}: \n
                    {}\n
                    {} enum:\n
                    {}\n
                    """.format(codelist_file, codes, name, codelist_enum))

    assert not errors, "Codelist files and schema enums out of sync, see warnings below."


def test_codelists_used():
    codelist_files = collect_codelist_files(absolute_source_codelist_dir)

    print('potato', codelist_files)

    codelists = set()
    for path, name, data in schemas:
        codelists.update(collect_codelist_values(path, data))

    unused_codelists = [codelist for codelist in codelist_files if codelist not in codelists]
    missing_codelists = [codelist for codelist in codelists if codelist not in codelist_files]

    assert len(unused_codelists) == 0, "Codelist files found not in schema: {}".format(unused_codelists)
    assert len(missing_codelists) == 0, "Codelists in schema missing CSVs: {}".format(missing_codelists)


def validate_json_schema(path, name, data, schema):
    if name == "codelist-schema.json":
        return
    errors = 0
    errors += validate_schema(path, data, schema)
    errors += validate_items_type(path, data)
    errors += validate_letter_case(path, data)
    assert not errors, "One or more JSON Schema files are invalid. See warnings below."


def collect_codelist_values(path, data, pointer=''):
    """
    Collects ``codelist`` values from JSON Schema.
    From https://github.com/open-contracting/jscc/blob/main/jscc/testing/checks.py#L674
    """
    codelists = set()

    if isinstance(data, list):
        for index, item in enumerate(data):
            codelists.update(collect_codelist_values(path, item, pointer='{}/{}'.format(pointer, index)))
    elif isinstance(data, dict):
        if 'codelist' in data:
            codelists.add(data['codelist'])

        for key, value in data.items():
            codelists.update(collect_codelist_values(path, value, pointer='{}/{}'.format(pointer, key)))

    return codelists


def collect_codelist_enums(path, data, pointer=''):
    """
    Collects values of ``codelist``, ``enum`` and ``openCodelist`` from JSON Schema.
    Adapted from collect_codelist_values
    """
    codelists = {}

    if isinstance(data, list):
        for index, item in enumerate(data):
            codelists.update(collect_codelist_enums(path, item, pointer='{}/{}'.format(pointer, index)))
    elif isinstance(data, dict):
        if 'codelist' in data:
          if data.get('type') == 'array' and 'items' in data:
            codelists[data.get('codelist')] = ((data['items'].get('enum'), data.get('openCodelist')))
          else:
            codelists[data.get('codelist')] = ((data.get('enum'), data.get('openCodelist')))

        for key, value in data.items():
            codelists.update(collect_codelist_enums(path, value, pointer='{}/{}'.format(pointer, key)))

    return codelists


def collect_codelist_files(schema_dir):
    codelist_files = set()
    for csvpath, csvname, _, fieldnames, _ in walk_csv_data(top=schema_dir):
        if 'Code' in fieldnames:
            codelist_files.add(csvname)

    return codelist_files


def collect_codelist_codes():
    """
    Walk through all the codelist CSV files and get just the codes
    """
    codelist_codes = {}
    codelist_csvs = walk_csv_data(top=absolute_source_codelist_dir)
    # (file path, file name, text content, fieldnames, rows)
    for _, codelist_file, _, _, rows in codelist_csvs:
        codes = []
        for row in rows:
            codes.append(row.get('Code'))
        codelist_codes[codelist_file] = codes

    return codelist_codes
