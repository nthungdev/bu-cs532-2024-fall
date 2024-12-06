from pymongo import MongoClient
import importlib
import json
from bson import json_util
from pathlib import Path


def get_query_description(index):
    """
    Returns the query description for the given 1-based index.
    """
    description = None
    try:
        module_name = f'app.queries.query_{index}'
        module = importlib.import_module(module_name)
        description = getattr(module, 'description')
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
        module_name = f'app.queries.query_{index}'
        module = importlib.import_module(module_name)
        query = getattr(module, 'execute')
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


def get_query(index):

    file_name = f'{index}.mongodb.js'

    file_path = Path(f'app/NoSQL/{file_name}')

    if not file_path.exists():
        print(f"File {file_name} does not exist in the NoSQL folder.")
        return None

    try:
        with open(file_path, 'r') as file:
            file_content = file.read().strip()
            query_str = file_content.split('=')[-1].strip().rstrip(';')
            return query_str

    except Exception as e:
        print(f"An error occurred while reading {file_name}: {e}")
        return None
