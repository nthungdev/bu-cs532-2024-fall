import app.utils as utils

description = 'Count the total number of terms served by each party across all presidents and vice presidents.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": {
                "path": "$terms"
            }
        },
        {
            "$group": {
                "_id": "$terms.party",
                "totalTerms": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "totalTerms": -1
            }
        },
        {
            "$project": {
                "_id": 0,
                "party": "$_id",
                "totalTerms": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
