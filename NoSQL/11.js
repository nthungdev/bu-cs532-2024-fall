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

    // Unwind the terms array to process each term individually
    // Match only presidential terms
    // Add a calculated field for the duration of each term in days
    // Convert milliseconds to days
    // Group by party and calculate the average term duration
    // Sort by average duration in descending order