import app.utils as utils

description = 'List all U.S. presidents with their full names and party affiliation.'


def execute():
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
