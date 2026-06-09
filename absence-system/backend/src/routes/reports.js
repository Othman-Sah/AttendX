import express from "express";
import PDFDocument from "pdfkit";
import { Absence } from "../models/Absence.js";
import { requireAuth } from "../middleware/auth.js";

const router = express.Router();

router.get("/", requireAuth, async (req, res) => {
  const { sessionType = "regular", date } = req.query;
  const query = { sessionType };
  if (date) {
    const start = new Date(date);
    const end = new Date(start);
    end.setDate(start.getDate() + 1);
    query.date = { $gte: start, $lt: end };
  }
  const records = await Absence.find(query).populate("student").sort({ date: -1 });
  res.json({ records });
});

router.get("/pdf", requireAuth, async (req, res) => {
  const { sessionType = "regular", date } = req.query;
  const records = await Absence.find({ sessionType }).populate("student").sort({ date: -1 }).limit(150);

  res.setHeader("Content-Type", "application/pdf");
  res.setHeader("Content-Disposition", `attachment; filename=${sessionType}-absence-report.pdf`);

  const doc = new PDFDocument({ margin: 48 });
  doc.pipe(res);
  doc.fontSize(20).text("University Absence Report", { underline: true });
  doc.moveDown(0.5).fontSize(11).text(`Session: ${sessionType}`);
  doc.text(`Generated: ${new Date().toLocaleString()}`);
  if (date) doc.text(`Date filter: ${date}`);
  doc.moveDown();

  records.forEach((record, index) => {
    doc
      .fontSize(10)
      .text(
        `${index + 1}. ${record.student?.studentId || "-"} | ${record.student?.name || "-"} | ${record.className} | ${record.subject} | ${record.status} | ${record.date.toISOString().slice(0, 10)}`
      );
  });

  doc.end();
});

export default router;
