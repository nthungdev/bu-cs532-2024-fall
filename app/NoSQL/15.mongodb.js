use('project2')
db.executives.aggregate([
    { $unwind: '$terms' },
    {
        $group: {
            _id: {
                bioguide: '$id.bioguide',
                name: { $concat: ['$name.first', ' ', '$name.last'] },
            },
            prezParties: {
                $addToSet: {
                    $cond: [
                        { $eq: ['$terms.type', 'prez'] },
                        '$terms.party',
                        '$$REMOVE',
                    ],
                },
            },
            vpParties: {
                $addToSet: {
                    $cond: [
                        { $eq: ['$terms.type', 'viceprez'] },
                        '$terms.party',
                        '$$REMOVE',
                    ],
                },
            },
        },
    },
    {
        $project: {
            _id: 0,
            name: '$_id.name',
            prezParties: 1,
            vpParties: 1,
            sameParty: { $setIntersection: ['$prezParties', '$vpParties'] },
        },
    },
    { $match: { 'sameParty.0': { $exists: true } } },
    {
        $project: {
            name: 1,
            sameParty: 1,
        },
    },
])
