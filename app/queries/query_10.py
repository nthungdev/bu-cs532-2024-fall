import app.utils as utils

description = 'List all presidents who did not serve in Congress.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$match": {
                "terms.type": "prez"
            }
        },
        {
            "$lookup": {
                "from": "legislators",
                "localField": "id.bioguide",
                "foreignField": "id.bioguide",
                "as": "legislatorRecord"
            }
        },
        {
            "$match": {
                "legislatorRecord": { "$eq": [] }
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
