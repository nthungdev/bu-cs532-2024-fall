import app.utils as utils

description = 'Identify the longest-serving female legislator.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": "$terms"
        },
        {
            "$match": { "bio.gender": "F" }
        },
        {
            "$project": {
                "name": {
                    "$concat": [
                        "$name.first",
                        " ",
                        { "$ifNull": ["$name.middle", ""] },
                        " ",
                        "$name.last"
                    ]
                },
                "duration": {
                    "$subtract": [
                        { "$dateFromString": { "dateString": "$terms.end" } },
                        { "$dateFromString": { "dateString": "$terms.start" } }
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$name",
                "totalDuration": { "$sum": "$duration" }
            }
        },
        {
            "$sort": { "totalDuration": -1 }
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "_id": 0,
                "name": "$_id",
                "totalDurationInYears": {
                    "$divide": ["$totalDuration", 1000 * 60 * 60 * 24 * 365]
                }
            }
        }
    ]

    result = db.get_collection('legislators').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
