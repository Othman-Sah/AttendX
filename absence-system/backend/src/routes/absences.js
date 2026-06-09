import express from "express";
import { Absence } from "../models/Absence.js";
import { Student } from "../models/Student.js";
import { requireAuth } from "../middleware/auth.js";

const router = express.Router();

router.get("/", requireAuth, async (req, res) => {
  const { className, subject, date, search } = req.query;
  const query = {};
  if (className) query.className = className;
  if (subject) query.subject = subject;
  if (date) {
    const start = new Date(date);
    const end = new Date(start);
    end.setDate(start.getDate() + 1);
    query.date = { $gte: start, $lt: end };
  }

  let studentIds;
  if (search) {
    const students = await Student.find({
      $or: [{ name: new RegExp(search, "i") }, { studentId: new RegExp(search, "i") }]
    }).select("_id");
    studentIds = students.map((student) => student._id);
    query.student = { $in: studentIds };
  }

  const records = await Absence.find(query).populate("student").sort({ date: -1 }).limit(200);
  res.json({ records });
});

router.post("/mark", requireAuth, async (req, res) => {
  const { studentId, className, subject, sessionType, status, date, note } = req.body;
  const student = await Student.findOne({ studentId });
  if (!student) return res.status(404).json({ message: "Student not found." });

  const record = await Absence.findOneAndUpdate(
    { student: student._id, subject, date: new Date(date) },
    {
      student: student._id,
      className: className || student.className,
      subject,
      sessionType,
      status,
      date: new Date(date),
      note,
      markedBy: req.user._id
    },
    { new: true, upsert: true, setDefaultsOnInsert: true }
  ).populate("student");

  req.app.get("io").emit("absence:updated", record);
  res.json({ record });
});

export default router;
