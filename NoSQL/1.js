use("project2");
db.executives.aggregate([
  {
    $unwind: {
      path: "$terms",
    }
  },
  {
    $match: { "terms.type": "prez" }
  },
  {
    $project: {
      _id: 0,
      full_name: { 
        $concat: [ "$name.first", " ", { $ifNull: ["$name.middle", "" ] }, " ", "$name.last" ] 
      },
      party: "$terms.party",
      temp_start_date: "$terms.start" 
    }
  },
  {
    $sort: { temp_start_date: 1 } 
  },
  {
    $project: {
      full_name: 1,
      party: 1 
    }
  }
]).toArray();
