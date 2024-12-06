use('project2')

db.legislators.aggregate([
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
            },
            hasHouse: {
                $anyElementTrue: {
                    $map: {
                        input: '$terms',
                        as: 'term',
                        in: { $eq: ['$$term.type', 'rep'] },
                    },
                },
            }, // Check if they served in the House
            hasSenate: {
                $anyElementTrue: {
                    $map: {
                        input: '$terms',
                        as: 'term',
                        in: { $eq: ['$$term.type', 'sen'] },
                    },
                },
            }, // Check if they served in the Senate
        },
    },
    {
        $match: {
            hasHouse: true,
            hasSenate: true,
        },
    },
    {
        $project: {
            _id: 0,
            name: 1,
        },
    },
])
