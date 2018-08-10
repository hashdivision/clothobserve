"""
    clothobserve.core.database.mongo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    MongoEngine instance for managing MongoDB database.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask_mongoengine import MongoEngine

#: MongoEngine instance for managing MongoDB database.
MONGO_DB = MongoEngine()
