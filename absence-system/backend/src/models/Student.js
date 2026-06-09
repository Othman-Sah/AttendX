import mongoose from "mongoose";

const studentSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    studentId: { type: String, required: true, unique: true },
    className: { type: String, required: true },
    email: String,
    program: String,
    year: Number
  },
  { timestamps: true }
);

export const Student = mongoose.model("Student", studentSchema);
