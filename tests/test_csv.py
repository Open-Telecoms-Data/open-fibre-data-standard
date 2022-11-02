from jscc.testing.checks import get_invalid_csv_files
from jscc.testing.util import warn_and_assert


def test_csv_valid():
    warn_and_assert(get_invalid_csv_files(), '{0} is not valid CSV: {1}',
                    'CSV files are invalid. See warnings below.')

