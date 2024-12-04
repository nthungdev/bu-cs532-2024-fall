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
      names: {
        $addToSet: {
          $concat: ["$name.first", " ", "$name.last"]
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      count: { $size: "$names" },
      names: 1
    }
  }
]).toArray();
