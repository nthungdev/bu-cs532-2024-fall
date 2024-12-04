from pymongo import MongoClient
import importlib
import json
from bson import json_util

module_name = 'app.queries'
queries = importlib.import_module(module_name)


def get_query_description(index):
    """
    Returns the query description for the given 1-based index.
    """
    try:
        descriptions = getattr(queries, 'query_descriptions')
        description = descriptions.get(index, 'None')
    except AttributeError:
        print(f"Description for query {index} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

    return description


def get_query_fn(index):
    """
    Returns the query function for the given 1-based index.
    """
    query = None
    try:
        query = getattr(queries, f'query_{index}')
    except AttributeError:
        print(f"Description for query {index} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

    return query


def get_mongo():
    db_name = 'project2'
    client = MongoClient()
    db = client[db_name]
    return client, db


def convert_to_pretty_string(mongo_docs):
    # Convert the MongoDB documents list to a pretty JSON string
    pretty_string = json.dumps(mongo_docs, indent=4, default=json_util.default)
    return pretty_string
