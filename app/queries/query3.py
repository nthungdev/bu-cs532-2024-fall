import app.utils as utils

description = 'Count the total number of U.S. presidents who were elected without party affiliation (party: "no party"), and display their names.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": "$terms"
        },
        {
            "$match": { "terms.party": "no party" }
        },
        {
            "$group": {
                "_id": None,
                "count": { "$sum": 1 },
                "names": {
                    "$addToSet": {
                        "$concat": ["$name.first", " ", "$name.last"]
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "count": 1,
                "names": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
