import mongoose from "mongoose";

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    passwordHash: { type: String, required: true },
    role: { type: String, enum: ["admin", "professor"], default: "professor" },
    department: { type: String, default: "Academic Affairs" }
  },
  { timestamps: true }
);

export const User = mongoose.model("User", userSchema);
