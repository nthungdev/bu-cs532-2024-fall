use("project2");
db.executives.aggregate([
    { $unwind: "$terms" },
    { $match: { "terms.type": "viceprez" } },
    {
        $addFields: {
            termYears: {
                $divide: [
                    { 
                        $subtract: [
                            { $dateFromString: { dateString: "$terms.end" } },
                            { $dateFromString: { dateString: "$terms.start" } }
                        ]
                    },
                    1000 * 60 * 60 * 24 * 365  
                ]
            }
        }
    },
    {
        $group: {
            _id: { name: { $concat: ["$name.first", " ", "$name.last"] } },
            totalYears: { $sum: "$termYears" }
        }
    },
    { $sort: { totalYears: -1 } },
    {
        $project:{
            _id: 0,
            name: "$_id.name",
            totalYears :1
        }
    }
]);
