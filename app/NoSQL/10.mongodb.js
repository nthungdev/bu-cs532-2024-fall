use('project2')
db.executives.aggregate([
    { $match: { 'terms.type': 'prez' } },
    {
        $lookup: {
            from: 'legislators',
            localField: 'id.bioguide',
            foreignField: 'id.bioguide',
            as: 'legislatorRecord',
        },
    },
    { $match: { legislatorRecord: { $eq: [] } } },
    {
        $project: {
            _id: 0,
            name: { $concat: ['$name.first', ' ', '$name.last'] },
        },
    },
])
