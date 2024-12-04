import app.utils as utils

description = 'List all unique parties represented by legislators.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": "$terms" 
        },
        {
            "$match": { "terms.party": { "$ne": None } }
        },
        {
            "$group": {
                "_id": "$terms.party"
            }
        },
        {
            "$sort": { "_id": 1 }
        },
        {
            "$project": {
                "_id": 0,
                "party": "$_id"
            }
        }
    ]

    result = db.get_collection('legislators').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
