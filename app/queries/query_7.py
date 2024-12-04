import app.utils as utils

description = 'List all legislators who served in both the House and the Senate.'

def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$project": {
                "name": {
                    "$concat": [
                        "$name.first",
                        " ",
                        {"$ifNull": ["$name.middle", ""]},
                        " ",
                        "$name.last"
                    ]
                },
                "hasHouse": {
                    "$anyElementTrue": {
                        "$map": {
                            "input": "$terms",
                            "as": "term",
                            "in": {"$eq": ["$$term.type", "rep"]}
                        }
                    }
                },
                "hasSenate": {
                    "$anyElementTrue": {
                        "$map": {
                            "input": "$terms",
                            "as": "term",
                            "in": {"$eq": ["$$term.type", "sen"]}
                        }
                    }
                }
            }
        },
        {
            "$match": {
                "hasHouse": True,
                "hasSenate": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1
            }
        }
    ]

    result = db.get_collection('legislators').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
