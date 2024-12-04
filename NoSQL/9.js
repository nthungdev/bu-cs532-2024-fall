use("project2");
db.executives.aggregate([
    { $unwind: "$terms" },
    { $match: { "terms.type": "viceprez", "terms.how": "appointment" } },
    {
        $project: {
            _id: 0,
            name: { $concat: ["$name.first", " ", "$name.last"] },
        }
    }
]);

// Unwind the terms array to process each term individually
    // Match only vice presidents who were appointed
    // Project relevant details