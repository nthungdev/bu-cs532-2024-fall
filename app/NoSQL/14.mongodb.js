use('project2')
db.executives.aggregate([
    { $unwind: { path: '$terms' } },
    { $match: { 'terms.type': 'prez' } },
    {
        $lookup: {
            from: 'legislators',
            let: {
                prezState: '$terms.state',
                prezStart: {
                    $dateFromString: { dateString: '$terms.start' },
                },
                prezEnd: {
                    $dateFromString: { dateString: '$terms.end' },
                },
            },
            pipeline: [
                { $unwind: { path: '$terms' } },
                {
                    $match: {
                        $expr: {
                            $and: [
                                { $eq: ['$terms.state', '$$prezState'] },
                                {
                                    $lte: [
                                        {
                                            $dateFromString: {
                                                dateString: '$terms.start',
                                            },
                                        },
                                        '$$prezEnd',
                                    ],
                                },
                                {
                                    $gte: [
                                        {
                                            $dateFromString: {
                                                dateString: '$terms.end',
                                            },
                                        },
                                        '$$prezStart',
                                    ],
                                },
                            ],
                        },
                    },
                },
                {
                    $project: {
                        _id: 0,
                        legislator_name: {
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
                        },
                    },
                },
            ],
            as: 'overlapping_legislators',
        },
    },
    {
        $match: { overlapping_legislators: { $ne: [] } },
    },
    {
        $project: {
            _id: 0,
            president_name: {
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
            },
            state: '$terms.state',
            overlapping_legislators: 1,
        },
    },
])
