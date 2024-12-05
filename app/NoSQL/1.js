use('project2')

db.executives
  .aggregate([
    {
      $unwind: {
        path: '$terms',
      },
    },
    {
      $match: {
        'terms.type': 'prez',
      },
    },
    {
      $group: {
        _id: {
          full_name: {
            $concat: [
              '$name.first',
              ' ',
              { $ifNull: ['$name.middle', ''] },
              ' ',
              '$name.last',
            ],
          },
          party: '$terms.party',
        },
        start_date: { $min: '$terms.start' },
      },
    },
    {
      $sort: {
        start_date: 1,
      },
    },
    {
      $project: {
        _id: 0,
        full_name: '$_id.full_name',
        party: '$_id.party',
      },
    },
  ])
  .toArray()
