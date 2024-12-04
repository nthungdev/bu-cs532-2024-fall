import app.utils as utils

description = 'Calculate the total number of years served by each vice president in office.'

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
                "terms.type": "viceprez"
            }
        },
        {
            "$addFields": {
                "termYears": {
                    "$divide": [
                        {
                            "$subtract": [
                                { "$dateFromString": { "dateString": "$terms.end" } },
                                { "$dateFromString": { "dateString": "$terms.start" } }
                            ]
                        },
                        1000 * 60 * 60 * 24 * 365  # Convert milliseconds to years
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "name": {
                        "$concat": [
                            "$name.first",
                            " ",
                            "$name.last"
                        ]
                    }
                },
                "totalYears": {
                    "$sum": "$termYears"
                }
            }
        },
        {
            "$sort": {
                "totalYears": -1
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": "$_id.name",
                "totalYears": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
