import express from "express";
import { Absence } from "../models/Absence.js";
import { Student } from "../models/Student.js";
import { requireAuth } from "../middleware/auth.js";

const router = express.Router();

router.get("/", requireAuth, async (_req, res) => {
  const start = new Date();
  start.setHours(0, 0, 0, 0);
  const end = new Date(start);
  end.setDate(start.getDate() + 1);

  const [totalStudents, absencesToday, examsOngoing, trends] = await Promise.all([
    Student.countDocuments(),
    Absence.countDocuments({ date: { $gte: start, $lt: end }, status: "absent" }),
    Absence.distinct("subject", { sessionType: "exam", date: { $gte: start, $lt: end } }),
    Absence.aggregate([
      { $match: { date: { $gte: new Date(Date.now() - 1000 * 60 * 60 * 24 * 9) } } },
      {
        $group: {
          _id: {
            day: { $dateToString: { format: "%Y-%m-%d", date: "$date" } },
            status: "$status"
          },
          count: { $sum: 1 }
        }
      },
      { $sort: { "_id.day": 1 } }
    ])
  ]);

  res.json({
    cards: {
      totalStudents,
      absencesToday,
      examsOngoing: examsOngoing.length
    },
    trends
  });
});

export default router;
