use('project2')

db.legislators.aggregate([
    {
        $unwind: '$terms',
    },
    {
        $match: { 'bio.gender': 'F' },
    },
    {
        $project: {
            name: {
                $concat: [
                    '$name.first',
                    {
                        $cond: [
                            { $ifNull: ['$name.middle', false] },
                            { $concat: [' ', '$name.middle'] },
                            '',
                        ],
                    },
                    ' ',
                    '$name.last',
                ],
            }, // Combine first, middle, and last names
            duration: {
                $subtract: [
                    { $dateFromString: { dateString: '$terms.end' } },
                    { $dateFromString: { dateString: '$terms.start' } },
                ],
            },
        },
    },
    {
        $group: {
            _id: '$name',
            totalDuration: { $sum: '$duration' },
        },
    },
    {
        $sort: { totalDuration: -1 },
    },
    {
        $limit: 1,
    },
    {
        $project: {
            _id: 0,
            name: '$_id',
            totalDurationInYears: {
                $divide: ['$totalDuration', 1000 * 60 * 60 * 24 * 365],
            },
        },
    },
])
