use('project2')
db.executives.aggregate([
    { $unwind: '$terms' },
    {
        $group: {
            _id: '$terms.party',
            totalTerms: { $sum: 1 },
        },
    },
    { $sort: { totalTerms: -1 } },
    {
        $project: {
            _id: 0,
            party: '$_id',
            totalTerms: 1,
        },
    },
])
