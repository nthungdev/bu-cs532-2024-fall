use("project2");
db.executives.aggregate([
    { $unwind: '$terms' },
    { $match: { 'terms.type': 'viceprez' } },
    {
        $lookup: {
            from: 'legislators',
            let: {
                vpParty: '$terms.party',
                vpStart: '$terms.start',
                vpEnd: '$terms.end',
            },
            pipeline: [
                { $unwind: '$terms' },
                {
                    $match: {
                        $expr: {
                            $and: [
                                { $eq: ['$terms.party', '$$vpParty'] },
                                { $gte: ['$terms.start', '$$vpStart'] }, // Legislator's term starts after or at the same time as VP's
                                { $lte: ['$terms.end', '$$vpEnd'] }, // Legislator's term ends before or at the same time as VP's
                            ],
                        },
                    },
                },
                {
                    $project: {
                        _id: 0,
                        name: { $concat: [{ $trim: { input: { $concat: ['$name.first', ' ', '$name.last'] } } }] }, // Trim spaces
                    },
                },
            ],
            as: 'matchingLegislators',
        },
    },
    { $match: { matchingLegislators: { $ne: [] } } }, // Ensure that at least one legislator exists
    { $unwind: '$matchingLegislators' }, // Unwind matchingLegislators to remove array structure
    {
        $group: {
            _id: {
                name: { $concat: ['$name.first', ' ', '$name.last'] },
            },
            matchingLegislators: { $addToSet: '$matchingLegislators.name' }, // Ensure unique legislator names
        },
    },
    {
        $project: {
            _id: 0,
            vicePresident: '$_id.name',
            matchingLegislators: 1,
        },
    },
])
