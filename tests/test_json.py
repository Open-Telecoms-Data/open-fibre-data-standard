from jscc.testing.checks import get_empty_files, get_misindented_files, get_invalid_json_files
from jscc.testing.util import warn_and_assert


def test_empty():
    empty_files_paths = [path for path in get_empty_files() if "src/" not in path[0]]
    warn_and_assert(empty_files_paths, "{0} is empty, run: rm {0}", "Files are empty. See warnings below.")


def test_invalid_json():
    warn_and_assert(
        get_invalid_json_files(excluded=('.git', '.ve', '_static', 'build', 'fixtures', "_build")), "{0} is not valid JSON: {1}", "JSON files are invalid. See warnings below."
    )

