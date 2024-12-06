use('project2')
db.legislators
    .aggregate([
        {
            $unwind: '$terms',
        },
        {
            $match: { 'terms.party': { $ne: null } },
        },
        {
            $group: {
                _id: '$terms.party',
            },
        },
        {
            $sort: { _id: 1 },
        },
        {
            $project: {
                _id: 0,
                party: '$_id',
            },
        },
    ])
    .toArray()
