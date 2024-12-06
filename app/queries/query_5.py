import app.utils as utils

description = 'List all presidents who came to power through succession, ensuring unique entries and without sorting.'


def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": "$terms"
        },
        {
            "$match": {
                "terms.type": "prez",
                "terms.how": "succession"
            }
        },
        {
            "$group": {
                "_id": "$name",
                "full_name": {
                    "$first": {
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
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "full_name": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
