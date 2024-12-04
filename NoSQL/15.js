use("project2");
db.executives.aggregate([
    // Unwind the terms array to process each term individually
    { $unwind: "$terms" },
    // Group by individual to segregate terms by role
    {
        $group: {
            _id: { bioguide: "$id.bioguide", name: { $concat: ["$name.first", " ", "$name.last"] } },
            prezParties: {
                $addToSet: {
                    $cond: [{ $eq: ["$terms.type", "prez"] }, "$terms.party", "$$REMOVE"]
                }
            },
            vpParties: {
                $addToSet: {
                    $cond: [{ $eq: ["$terms.type", "viceprez"] }, "$terms.party", "$$REMOVE"]
                }
            }
        }
    },
    // Filter out any nulls and ensure at least one match between president and vice president party affiliations
    {
        $project: {
            _id: 0,
            name: "$_id.name",
            prezParties: 1,
            vpParties: 1,
            sameParty: { $setIntersection: ["$prezParties", "$vpParties"] }
        }
    },
    { $match: { "sameParty.0": { $exists: true } } }, // Ensure there's at least one common party
    // Project final output
    {
        $project: {
            name: 1,
            sameParty: 1
        }
    }
]);
