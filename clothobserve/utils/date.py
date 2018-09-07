"""
    clothobserve.utils.date
    ~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime

def convert_to_datetime(string: str, date_format: str = '%d.%m.%Y') -> datetime:
    """
    # TODO: Fill this docstring.
    """
    try:
        return datetime.strptime(string, date_format)
    except ValueError:
        return None
