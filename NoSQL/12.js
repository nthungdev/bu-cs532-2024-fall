use("project2");
db.executives.aggregate([
    // Unwind the terms array to process each term individually
    { $unwind: "$terms" },
    // Match only vice presidential terms
    { $match: { "terms.type": "viceprez" } },
    // Add a calculated field for the duration of each term in years
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
                    1000 * 60 * 60 * 24 * 365  // Convert milliseconds to years
                ]
            }
        }
    },
    // Group by vice president and sum up the total years served
    {
        $group: {
            _id: { name: { $concat: ["$name.first", " ", "$name.last"] } },
            totalYears: { $sum: "$termYears" }
        }
    },
    // Sort by total years in descending order
    { $sort: { totalYears: -1 } },
    {
        $project:{
            _id: 0,
            name: "$_id.name",
            totalYears :1
        }
    }
]);
