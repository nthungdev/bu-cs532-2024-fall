use("project2");
db.executives.aggregate([
    { $match: { "terms.type": "prez" } },
    {
        $lookup: {
            from: "legislators",
            localField: "id.bioguide",
            foreignField: "id.bioguide",
            as: "legislatorRecord"
        }
    },
    { $match: { legislatorRecord: { $eq: [] } } },
    {
        $project: {
            _id: 0,
            name: { $concat: ["$name.first", " ", "$name.last"] },
        }
    }
]);

 // Match only U.S. presidents
    // Lookup corresponding records in the legislators collection
    // Match presidents who have no record in the legislators collection
    // Project relevant details