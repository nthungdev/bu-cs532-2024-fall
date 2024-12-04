import app.utils as utils

description = 'List presidents and vice presidents who served terms under the same party affiliation in both roles.'

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
                "_id": {
                    "bioguide": "$id.bioguide",
                    "name": {
                        "$concat": ["$name.first", " ", "$name.last"]
                    }
                },
                "prezParties": {
                    "$addToSet": {
                        "$cond": [
                            { "$eq": ["$terms.type", "prez"] },
                            "$terms.party",
                            "$$REMOVE"
                        ]
                    }
                },
                "vpParties": {
                    "$addToSet": {
                        "$cond": [
                            { "$eq": ["$terms.type", "viceprez"] },
                            "$terms.party",
                            "$$REMOVE"
                        ]
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": "$_id.name",
                "prezParties": 1,
                "vpParties": 1,
                "sameParty": { "$setIntersection": ["$prezParties", "$vpParties"] }
            }
        },
        {
            "$match": {
                "sameParty.0": { "$exists": True }
            }
        },
        {
            "$project": {
                "name": 1,
                "sameParty": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
