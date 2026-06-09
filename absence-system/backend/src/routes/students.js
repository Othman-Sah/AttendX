import express from "express";
import { Student } from "../models/Student.js";
import { Absence } from "../models/Absence.js";
import { requireAuth } from "../middleware/auth.js";

const router = express.Router();

router.get("/", requireAuth, async (req, res) => {
  const search = req.query.search || "";
  const query = search
    ? {
        $or: [
          { name: new RegExp(search, "i") },
          { studentId: new RegExp(search, "i") },
          { className: new RegExp(search, "i") }
        ]
      }
    : {};

  const students = await Student.find(query).sort({ name: 1 }).limit(100);
  res.json({ students });
});

router.get("/:id", requireAuth, async (req, res) => {
  const student = await Student.findById(req.params.id);
  if (!student) return res.status(404).json({ message: "Student not found." });

  const history = await Absence.find({ student: student._id }).sort({ date: -1 }).limit(80);
  const total = history.length || 1;
  const absent = history.filter((row) => row.status === "absent").length;

  res.json({
    student,
    history,
    absencePercentage: Math.round((absent / total) * 100)
  });
});

export default router;
