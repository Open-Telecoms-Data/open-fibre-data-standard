import csv
import glob
import re
import warnings
import pytest
from pathlib import Path

basedir = Path(__file__).resolve().parent.parent
codelistdir = basedir / 'codelists'
datamodeldir = basedir / 'schema' / 'data_model'
referencedir = basedir / 'docs' / 'reference'


def _codelist_names():
    return sorted(Path(p).stem for p in glob.glob(str(codelistdir / '*' / '*.csv')))


def _codelist_refs():
    """Return (label, codelist_name) pairs from all data model attributes.csv files."""
    refs = []
    for attrs_csv in sorted(datamodeldir.glob('*/attributes.csv')):
        obj = attrs_csv.parent.name.capitalize()
        with attrs_csv.open() as f:
            for row in csv.DictReader(f):
                codelist = row.get('codelist', '').strip()
                if codelist:
                    label = f"{obj}/{row['path']}"
                    refs.append((label, codelist.removesuffix('.csv')))
    return refs


CODELIST_NAMES = _codelist_names()
CODELIST_REFS = _codelist_refs()


@pytest.fixture(scope='module')
def codelists_md():
    return (referencedir / 'codelists.md').read_text()


@pytest.mark.parametrize("codelist", CODELIST_NAMES)
def test_codelist_heading(codelist, codelists_md):
    """Each codelist CSV must have a heading in codelists.md."""
    assert f"# {codelist}\n" in codelists_md, \
        f"{codelist} codelist is missing from codelists.md"


@pytest.mark.parametrize("label,codelist", CODELIST_REFS)
def test_codelist_links(label, codelist, codelists_md):
    """Each data model attribute referencing a codelist must have a link in codelists.md."""
    assert f"[`{label}`]" in codelists_md, \
        f"{label} is missing from codelists.md"


def test_no_unknown_codelist_links(codelists_md):
    """Warn for code-formatted links in codelists.md that are not attributes that reference a codelist."""
    known_labels = {label for label, _ in CODELIST_REFS}
    for label in re.findall(r'\[`([^`]+)`\]', codelists_md):
        if label not in known_labels:
            warnings.warn(f"{label} appears in codelists.md, but is not an attribute that references a codelist.")
