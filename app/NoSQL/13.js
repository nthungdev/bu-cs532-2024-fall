use("project2");
db.executives.aggregate([
    { $unwind: "$terms" },
    { $match: { "terms.type": "viceprez" } },
    {
        $lookup: {
            from: "legislators",
            let: { vpParty: "$terms.party", vpStart: "$terms.start", vpEnd: "$terms.end" },
            pipeline: [
                { $unwind: "$terms" }, 
                { 
                    $match: { 
                        $expr: {
                            $and: [
                                { $lte: [ "$terms.start", "$$vpStart" ] }, 
                                { $lte: [ "$$vpEnd", "$terms.end" ] }, 
                                { $eq: [ "$terms.party", "$$vpParty" ] } 
                            ]
                        }
                    }
                },
                {
                    $project: { 
                        _id: 0, 
                        name: { $concat: ["$name.first", " ", "$name.last"] }
                    } 
                }
            ],
            as: "matchingLegislators"
        }
    },
    { $match: { matchingLegislators: { $ne: [] } } },
    {
        $group: {
            _id: { 
                name: { $concat: ["$name.first", " ", "$name.last"] }
            },
            matchingLegislators: { $addToSet: "$matchingLegislators.name" }
        }
    },
    {
        $project: {
            _id: 0,
            vicePresident: "$_id.name",
            matchingLegislators: 1
        }
    }
]);
