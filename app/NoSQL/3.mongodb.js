use('project2')

db.executives.aggregate([
    {
        $unwind: '$terms',
    },
    {
        $match: {
            'terms.party': 'no party',
            'terms.how': 'election',
        },
    },
    {
        $group: {
            _id: None,
            names: {
                $addToSet: {
                    $concat: ['$name.first', ' ', '$name.last'],
                },
            },
        },
    },
    {
        $project: {
            _id: 0,
            count: { $size: '$names' },
            names: 1,
        },
    },
])
