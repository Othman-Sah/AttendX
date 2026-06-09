import mongoose from "mongoose";

const absenceSchema = new mongoose.Schema(
  {
    student: { type: mongoose.Schema.Types.ObjectId, ref: "Student", required: true },
    className: { type: String, required: true },
    subject: { type: String, required: true },
    sessionType: { type: String, enum: ["regular", "exam"], default: "regular" },
    status: { type: String, enum: ["present", "absent"], required: true },
    date: { type: Date, required: true },
    markedBy: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    note: String
  },
  { timestamps: true }
);

absenceSchema.index({ student: 1, date: 1, subject: 1 }, { unique: true });

export const Absence = mongoose.model("Absence", absenceSchema);
