import app.utils as utils

description = 'List vice presidents and their matching legislators from the same party during overlapping terms.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        { 
            "$unwind": "$terms" 
        },
        { 
            "$match": { "terms.type": "viceprez" } 
        },
        {
            "$lookup": {
                "from": "legislators",
                "let": {
                    "vpParty": "$terms.party",
                    "vpStart": "$terms.start",
                    "vpEnd": "$terms.end"
                },
                "pipeline": [
                    { "$unwind": "$terms" },
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    { "$eq": ["$terms.party", "$$vpParty"] },
                                    { "$gte": ["$terms.start", "$$vpStart"] },
                                    { "$lte": ["$terms.end", "$$vpEnd"] }
                                ]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "name": { 
                                "$concat": [
                                    { "$trim": { "input": { "$concat": ["$name.first", " ", "$name.last"] } } }
                                ]
                            }
                        }
                    }
                ],
                "as": "matchingLegislators"
            }
        },
        { 
            "$match": { "matchingLegislators": { "$ne": [] } } 
        },
        { 
            "$unwind": "$matchingLegislators" 
        },
        {
            "$group": {
                "_id": { 
                    "name": { "$concat": ["$name.first", " ", "$name.last"] } 
                },
                "matchingLegislators": { "$addToSet": "$matchingLegislators.name" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "vicePresident": "$_id.name",
                "matchingLegislators": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
