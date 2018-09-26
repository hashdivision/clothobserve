"""
    clothobserve.logic.utils.random
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Random values generation for random purposes.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
import random
import string

def generate_random_string(length: int) -> str:
    """
    Generates random ASCII characters string of certain length.

    :param length: random string length.
    """
    return ''.join(random.choice(string.ascii_letters) for x in range(length))
