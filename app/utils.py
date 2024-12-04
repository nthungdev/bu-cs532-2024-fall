from pymongo import MongoClient
import importlib
import json
from bson import json_util

query_descriptions = {
    1: 'List all U.S. presidents with their full names and party affiliation.',
    2: 'List all unique parties represented by legislators.',
    3: 'Count the total number of U.S. presidents who were elected without party affiliation (party: "no party"), also display their names.',
    4: 'Identify the longest serving female legislator.',
    5: 'List all presidents who came to power through succession.',
    6: 'List presidents and vice presidents grouped by party affiliation.',
    7: 'List all legislators who served in both the house and the senate.',
    8: 'Count the number of terms served by each party across all presidents and vice presidents.',
    9: 'List vice presidents who were appointed rather than elected.',
    10: 'Identify legislators who did not serve in Congress and later became U.S. presidents.',
    11: 'Calculate the average duration of presidential terms by party.',
    12: 'Calculate the total number of years served by each vice president in office.',
    13: "List legislators who served in Congress during a vice president's term and shared the same party affiliation.",
    14: 'List presidents who had overlapping terms with legislators in the same state.',
    15: 'Identify all presidents and vice presidents who served terms under the same party affiliation in both roles.',
}


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

def get_query(index):
    # Define the path to the JSON file (query_{index}.js)
    query_file_path = f'app/queries/query_{index}.js'
    
    # Check if the file exists
    try:
        with open(query_file_path, 'r') as file:
            # Parse the JSON content from the file
            query_data = json.load(file)
            # Convert the entire JSON content to a string
            query_content = json.dumps(query_data)
            return query_content
    except FileNotFoundError:
        # Handle case where the file doesn't exist
        return None


def get_mongo():
    db_name = 'project2'
    client = MongoClient()
    db = client[db_name]
    return client, db


def convert_to_pretty_string(mongo_docs):
    # Convert the MongoDB documents list to a pretty JSON string
    pretty_string = json.dumps(mongo_docs, indent=4, default=json_util.default)
    return pretty_string
