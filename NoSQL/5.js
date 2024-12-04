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
    $group: {
      _id: "$name",
      full_name: {
        $first: {
          $concat: [
            "$name.first",
            " ",
            { $ifNull: ["$name.middle", ""] },
            " ",
            "$name.last"
          ]
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      full_name: 1
    }
  }
]).toArray();
