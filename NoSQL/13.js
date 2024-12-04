use("project2");
db.executives.aggregate([
    // Unwind the terms array to process each vice presidential term
    { $unwind: "$terms" },
    // Match only vice presidents
    { $match: { "terms.type": "viceprez" } },
    // Lookup overlapping terms from legislators
    {
        $lookup: {
            from: "legislators",
            let: { vpParty: "$terms.party", vpStart: "$terms.start", vpEnd: "$terms.end" },
            pipeline: [
                { $unwind: "$terms" }, // Unwind legislator terms
                { 
                    $match: { 
                        $expr: {
                            $and: [
                                { $gte: [ "$terms.end", "$$vpStart" ] }, // Overlapping term
                                { $lte: [ "$terms.start", "$$vpEnd" ] }, // Overlapping term
                                { $eq: [ "$terms.party", "$$vpParty" ] } // Same party
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
    // Only keep records where there are matching legislators
    { $match: { matchingLegislators: { $ne: [] } } },
    // Group by vice president to combine all their matching legislators
    {
        $group: {
            _id: { 
                name: { $concat: ["$name.first", " ", "$name.last"] }
            },
            matchingLegislators: { $addToSet: "$matchingLegislators.name" }
        }
    },
    // Project final output
    {
        $project: {
            _id: 0,
            vicePresident: "$_id.name",
            matchingLegislators: 1
        }
    }
]);
