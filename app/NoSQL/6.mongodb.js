use('project2')

db.executives
    .aggregate([
        {
            $unwind: '$terms',
        },
        {
            $group: {
                _id: '$terms.party',
                presidents: {
                    $addToSet: {
                        $cond: [
                            { $eq: ['$terms.type', 'prez'] },
                            {
                                $concat: [
                                    '$name.first',
                                    {
                                        $cond: [
                                            {
                                                $ifNull: [
                                                    '$name.middle',
                                                    false,
                                                ],
                                            },
                                            { $concat: [' ', '$name.middle'] },
                                            '',
                                        ],
                                    },
                                    ' ',
                                    '$name.last',
                                ],
                            },
                            null,
                        ],
                    },
                },
                vicePresidents: {
                    $addToSet: {
                        $cond: [
                            { $eq: ['$terms.type', 'viceprez'] },
                            {
                                $concat: [
                                    '$name.first',
                                    {
                                        $cond: [
                                            {
                                                $ifNull: [
                                                    '$name.middle',
                                                    false,
                                                ],
                                            },
                                            { $concat: [' ', '$name.middle'] },
                                            '',
                                        ],
                                    },
                                    ' ',
                                    '$name.last',
                                ],
                            },
                            null,
                        ],
                    },
                },
            },
        },
        {
            $project: {
                _id: 1,
                presidents: {
                    $filter: {
                        input: '$presidents',
                        as: 'pres',
                        cond: { $ne: ['$$pres', null] },
                    },
                },
                vicePresidents: {
                    $filter: {
                        input: '$vicePresidents',
                        as: 'vp',
                        cond: { $ne: ['$$vp', null] },
                    },
                },
            },
        },
        {
            $sort: { _id: 1 },
        },
    ])
    .toArray()
