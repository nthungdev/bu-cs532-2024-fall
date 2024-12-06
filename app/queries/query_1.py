import app.utils as utils

description = 'List all U.S. presidents with their full names and party affiliation, in the order of dates.'


def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": {
                "path": "$terms"
            }
        },
        {
            "$match": {
                "terms.type": "prez"
            }
        },
        {
            "$group": {
                "_id": {
                    "full_name": {
                        "$concat": [
                            '$name.first',
                            {
                                "$cond": [
                                    {"$ifNull": ['$name.middle', False]},
                                    {"$concat": [' ', '$name.middle']},
                                    '',
                                ],
                            },
                            ' ',
                            '$name.last',
                        ],
                    },
                    "party": "$terms.party"
                },
                "start_date": {"$min": "$terms.start"}
            }
        },
        {
            "$sort": {
                "start_date": 1
            }
        },
        {
            "$project": {
                "_id": 0,
                "full_name": "$_id.full_name",
                "party": "$_id.party"
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
