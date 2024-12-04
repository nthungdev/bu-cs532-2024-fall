import app.utils as utils

description = 'Calculate the average duration of presidential terms by party.'

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
            "$addFields": {
                "termDuration": {
                    "$divide": [
                        {
                            "$subtract": [
                                { "$dateFromString": { "dateString": "$terms.end" } },
                                { "$dateFromString": { "dateString": "$terms.start" } }
                            ]
                        },
                        1000 * 60 * 60 * 24  # Convert milliseconds to days
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$terms.party",
                "averageDuration": {
                    "$avg": "$termDuration"
                }
            }
        },
        {
            "$sort": {
                "averageDuration": -1
            }
        },
        {
            "$project": {
                "_id": 0,
                "party": "$_id",
                "averageDuration": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
