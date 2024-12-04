import app.utils as utils

description = 'List all presidents who came to power through succession.'

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
                "start_date": "$terms.start",
                "reason": "$terms.how"
            }
        },
        {
            "$sort": {
                "start_date": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
