use("project2");
db.executives.aggregate([
    { $unwind: "$terms" },
    { $match: { "terms.type": "prez" } },
    {
        $addFields: {
            termDuration: {
                $divide: [
                    { 
                        $subtract: [
                            { $dateFromString: { dateString: "$terms.end" } },
                            { $dateFromString: { dateString: "$terms.start" } }
                        ]
                    },
                    1000 * 60 * 60 * 24  
                ]
            }
        }
    },
    
    {
        $group: {
            _id: "$terms.party",
            averageDuration: { $avg: "$termDuration" }
        }
    },
    
    { $sort: { averageDuration: -1 } },
    {
        $project: {
            _id: 0,
            party: "$_id",
            averageDuration: 1,
        }
    }
]);

