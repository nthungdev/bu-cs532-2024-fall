import app.utils as utils

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


def query_1():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": {
                "path": "$terms",
            }
        },
        {
            "$match": {
                "terms.type": "prez"
            }
        },
        {
            "$project": {
                "_id": 0,
                "full_name": {
                    "$concat": [
                        "$name.first",
                        " ",
                        {"$ifNull": ["$name.middle", ""]},
                        " ",
                        "$name.last"
                    ]
                },
                "party": "$terms.party",
                "temp_start_date": "$terms.start"
            }
        },
        {
            "$sort": {
                "temp_start_date": 1
            }
        },
        {
            "$project": {
                "full_name": 1,
                "party": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output

# TODO Implement remaining queries


def query_2():
    return 'query_2 result'


def query_3():
    return 'query_3 result'


def query_4():
    return 'query_4 result'


def query_5():
    return 'query_5 result'


def query_6():
    return 'query_6 result'


def query_7():
    return 'query_7 result'


def query_8():
    return 'query_8 result'


def query_9():
    return 'query_9 result'


def query_10():
    return 'query_10 result'


def query_11():
    return 'query_11 result'


def query_12():
    return 'query_12 result'


def query_13():
    return 'query_13 result'


def query_14():
    return 'query_14 result'


def query_15():
    return 'query_15 result'
