use("project2");

db.executives.aggregate([
  {
    $unwind: "$terms" 
  },
  {
    $match: { "terms.party": "no party" } 
  },
  {
    $group: {
      _id: null, 
      count: { $sum: 1 }, 
      names: { $addToSet: { $concat: ["$name.first", " ", "$name.last"] } } 
    }
  },
  {
    $project: {
      _id: 0, 
      count: 1, 
      names: 1 
    }
  }
]);
