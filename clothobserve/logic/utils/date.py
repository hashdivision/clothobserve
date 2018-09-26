"""
    clothobserve.logic.utils.date
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Date related utility functions.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime

def convert_to_datetime(string: str, date_format: str = '%d.%m.%Y') -> datetime:
    """
    Converts string in DD.MM.YYYY format to datetime object.

    Returns:
        If conversion succeeds - ``datetime`` object. Otherwise - None.
    """
    try:
        return datetime.strptime(string, date_format)
    except ValueError:
        return None

def convert_to_string(datetime_object: datetime) -> str:
    """
    Converts datetime object to JSON string in DD.MM.YYYY format.

    Returns:
        If conversion succeeds - ``"DD.MM.YYYY"`` string. Otherwise - ``null`` string.
    """
    try:
        return '"' + datetime_object.strftime("%d.%m.%Y") + '"'
    except AttributeError:
        return "null"
