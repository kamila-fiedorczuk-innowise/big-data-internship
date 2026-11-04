// MongoDB aggregation queries on the tiktok.reviews collection.
// 1. Top 5 most frequent comments (placeholder "-" excluded)
const topComments = [  { $match: { content: { $ne: "-" } } },
  { $group: { _id: "$content", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 5 }
];

// 2. All reviews with content shorter than 5 characters (placeholder "-" excluded)
const shortContent = [
  { $match: { content: { $ne: "-" } } },
  { $match: { $expr: { $lt: [{ $strLenCP: "$content" }, 5] } } },
];

// 3. Average score for each day (day returned as a Date)
const avgScorePerDay = [
   {
    $group: {
      _id: { $dateTrunc: { date: "$at", unit: "day" } },
      avgScore: { $avg: "$score" },
    },
   },
   { $sort: { _id: 1 } },
   { $project: { _id: 0, day: "$_id", avgScore: 1 } },
];
