import app.utils as utils

description = 'List all vice presidents who were appointed rather than elected.'

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
                "terms.type": "viceprez",
                "terms.how": "appointment"
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": {
                    "$concat": [
                        "$name.first",
                        " ",
                        "$name.last"
                    ]
                }
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
