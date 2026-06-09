import dotenv from "dotenv";
import bcrypt from "bcryptjs";
import { connectDB } from "./db.js";
import { User } from "../models/User.js";
import { Student } from "../models/Student.js";
import { Absence } from "../models/Absence.js";

dotenv.config();

const users = [
  { name: "Admin Director", email: "admin@university.edu", password: "admin123", role: "admin" },
  { name: "Professor Lina", email: "professor@university.edu", password: "prof123", role: "professor" }
];

const students = [
  ["Amina El Idrissi", "STU-1001", "CS-2A", "Computer Science", 2],
  ["Youssef Haddad", "STU-1002", "CS-2A", "Computer Science", 2],
  ["Maya Cohen", "STU-1003", "ENG-1B", "Engineering", 1],
  ["Adam Brooks", "STU-1004", "BUS-3C", "Business", 3],
  ["Sara Mansouri", "STU-1005", "MED-1A", "Medicine", 1]
];

async function seed() {
  await connectDB();
  await Promise.all([User.deleteMany({}), Student.deleteMany({}), Absence.deleteMany({})]);

  const createdUsers = await User.insertMany(
    await Promise.all(
      users.map(async (user) => ({
        ...user,
        passwordHash: await bcrypt.hash(user.password, 10)
      }))
    )
  );

  const createdStudents = await Student.insertMany(
    students.map(([name, studentId, className, program, year]) => ({ name, studentId, className, program, year }))
  );

  const today = new Date();
  const records = createdStudents.flatMap((student, index) => [
    {
      student: student._id,
      className: student.className,
      subject: index % 2 ? "Algorithms" : "Calculus",
      sessionType: index % 3 ? "regular" : "exam",
      status: index % 2 ? "present" : "absent",
      date: today,
      markedBy: createdUsers[0]._id,
      note: "Seed record"
    }
  ]);
  await Absence.insertMany(records);

  console.log("Seed complete");
  console.log("Admin: admin@university.edu / admin123");
  console.log("Professor: professor@university.edu / prof123");
  process.exit(0);
}

seed();
