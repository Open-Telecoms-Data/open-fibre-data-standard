"""Check that schema/data_model/ is up to date with network-schema.json."""

import json
import tempfile
from pathlib import Path

import pytest

import manage

basedir = Path(__file__).resolve().parent.parent
COMMITTED_DIR = basedir / 'schema' / 'data_model'
SCHEMA_PATH = basedir / 'schema' / 'data_formats' / 'json' / 'network-schema.json'

GENERATED_DIR = Path(tempfile.mkdtemp()) / 'data_model'

with SCHEMA_PATH.open() as f:
    _schema = json.load(f)

_original_schemadir = manage.schemadir
manage.schemadir = GENERATED_DIR.parent
manage.update_data_model_docs(_schema)
manage.schemadir = _original_schemadir

GENERATED_FILES = sorted(p.relative_to(GENERATED_DIR) for p in GENERATED_DIR.rglob('*') if p.is_file())


@pytest.mark.parametrize("relative_path", GENERATED_FILES, ids=str)
def test_data_model_file_up_to_date(relative_path):
    """Each file in schema/data_model/ must match what update_data_model_docs generates from network-schema.json."""
    committed_file = COMMITTED_DIR / relative_path
    assert committed_file.exists(), \
        f"{relative_path} is missing from schema/data_model/ - run `python manage.py pre-commit`"
    assert (GENERATED_DIR / relative_path).read_text() == committed_file.read_text(), \
        f"{relative_path} is out of date - run `python manage.py pre-commit`"


def test_no_stale_entity_directories():
    """schema/data_model/ must not contain leftover directories for entities no longer in network-schema.json."""
    committed_entity_dirs = {p.name for p in COMMITTED_DIR.iterdir() if p.is_dir()}
    generated_entity_dirs = {p.parts[0] for p in GENERATED_FILES if len(p.parts) > 1}
    stale = committed_entity_dirs - generated_entity_dirs
    assert not stale, f"Stale entity directories in schema/data_model/: {stale} - run `python manage.py pre-commit`"
