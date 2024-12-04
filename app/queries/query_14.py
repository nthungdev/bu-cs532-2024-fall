import app.utils as utils

description = 'List presidents who had overlapping terms with legislators from the same state.'

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
            "$lookup": {
                "from": "legislators",
                "let": {
                    "prezState": "$terms.state",
                    "prezStart": {
                        "$dateFromString": { "dateString": "$terms.start" }
                    },
                    "prezEnd": {
                        "$dateFromString": { "dateString": "$terms.end" }
                    }
                },
                "pipeline": [
                    {
                        "$unwind": {
                            "path": "$terms"
                        }
                    },
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    { "$eq": ["$terms.state", "$$prezState"] },
                                    {
                                        "$lte": [
                                            {
                                                "$dateFromString": { "dateString": "$terms.start" }
                                            },
                                            "$$prezEnd"
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            {
                                                "$dateFromString": { "dateString": "$terms.end" }
                                            },
                                            "$$prezStart"
                                        ]
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "legislator_name": {
                                "$concat": [
                                    "$name.first",
                                    " ",
                                    { "$ifNull": ["$name.middle", ""] },
                                    " ",
                                    "$name.last"
                                ]
                            }
                        }
                    }
                ],
                "as": "overlapping_legislators"
            }
        },
        {
            "$match": {
                "overlapping_legislators": { "$ne": [] }
            }
        },
        {
            "$project": {
                "_id": 0,
                "president_name": {
                    "$concat": [
                        "$name.first",
                        " ",
                        { "$ifNull": ["$name.middle", ""] },
                        " ",
                        "$name.last"
                    ]
                },
                "state": "$terms.state",
                "overlapping_legislators": 1
            }
        }
    ]

    result = db.get_collection('executives').aggregate(pipeline)
    output = utils.convert_to_pretty_string(list(result))
    return output
