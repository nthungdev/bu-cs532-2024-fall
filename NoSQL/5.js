use("project2");

db.executives.aggregate([
  {
    $unwind: "$terms" 
  },
  {
    $match: { 
      "terms.type": "prez", 
      "terms.how": "succession" 
    }
  },
  {
    $project: {
      _id: 0, 
      full_name: { 
        $concat: [ "$name.first", " ", { $ifNull: ["$name.middle", "" ] }, " ", "$name.last" ] 
      }, 
      start_date: "$terms.start", 
      reason: "$terms.how" 
    }
  },
  {
    $sort: { start_date: 1 } 
  }
]).toArray();
