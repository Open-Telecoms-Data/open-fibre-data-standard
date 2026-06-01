import csv
import pytest
from pathlib import Path

basedir = Path(__file__).resolve().parent.parent
datamodeldir = basedir / 'docs' / 'reference' / 'data_model'


def _entity_names():
    with (datamodeldir / 'entities.csv').open() as f:
        return [row['name'] for row in csv.DictReader(f)]


ENTITY_NAMES = _entity_names()


@pytest.fixture(scope='module')
def data_model_index_md():
    return (datamodeldir / 'index.md').read_text()


@pytest.mark.parametrize("entity", ENTITY_NAMES)
def test_entity_heading(entity, data_model_index_md):
    """Each entity in entities.csv must have a heading in data_model/index.md."""
    assert f"# {entity}\n" in data_model_index_md, \
        f"{entity} is missing from data_model/index.md"
