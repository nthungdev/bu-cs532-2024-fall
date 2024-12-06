use('project2')
db.executives.aggregate([
    { $unwind: '$terms' },
    { $match: { 'terms.type': 'viceprez' } },
    { $match: { 'terms.how': { $ne: 'election' } } },
    {
        $project: {
            _id: 0,
            name: { $concat: ['$name.first', ' ', '$name.last'] },
        },
    },
])
