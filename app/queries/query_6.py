import app.utils as utils

description = 'List presidents and vice presidents grouped by party affiliation.'


def execute():
    _, db = utils.get_mongo()

    pipeline = [
        {
            "$unwind": "$terms"
        },
        {
            "$group": {
                "_id": "$terms.party",
                "presidents": {
                    "$addToSet": {
                        "$cond": [
                            {"$eq": ["$terms.type", "prez"]},
                            {
                                "$concat": [
                                    '$name.first',
                                    {
                                        "$cond": [
                                            {
                                                "$ifNull": [
                                                    '$name.middle',
                                                    False,
                                                ],
                                            },
                                            {"$concat": [' ', '$name.middle']},
                                            '',
                                        ],
                                    },
                                    ' ',
                                    '$name.last',
                                ],
                            },
                            None
                        ]
                    }
                },
                "vicePresidents": {
                    "$addToSet": {
                        "$cond": [
                            {"$eq": ["$terms.type", "viceprez"]},
                            {
                                "$concat": [
                                    '$name.first',
                                    {
                                        "$cond": [
                                            {
                                                "$ifNull": [
                                                    '$name.middle',
                                                    False,
                                                ],
                                            },
                                            {"$concat": [' ', '$name.middle']},
                                            '',
                                        ],
                                    },
                                    ' ',
                                    '$name.last',
                                ],
                            },
                            None
                        ]
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 1,
                "presidents": {
                    "$filter": {
                        "input": "$presidents",
                        "as": "pres",
                        "cond": {"$ne": ["$$pres", None]}
                    }
                },
                "vicePresidents": {
                    "$filter": {
                        "input": "$vicePresidents",
                        "as": "vp",
                        "cond": {"$ne": ["$$vp", None]}
                    }
                }
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
