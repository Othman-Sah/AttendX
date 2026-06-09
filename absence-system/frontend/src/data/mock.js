export const mockTrends = [
  { day: "Mon", present: 94, absent: 6 },
  { day: "Tue", present: 91, absent: 9 },
  { day: "Wed", present: 96, absent: 4 },
  { day: "Thu", present: 89, absent: 11 },
  { day: "Fri", present: 93, absent: 7 }
];

export const sampleStudents = [
  { _id: "1", name: "Amina El Idrissi", studentId: "STU-1001", className: "CS-2A", program: "Computer Science", year: 2 },
  { _id: "2", name: "Youssef Haddad", studentId: "STU-1002", className: "CS-2A", program: "Computer Science", year: 2 },
  { _id: "3", name: "Maya Cohen", studentId: "STU-1003", className: "ENG-1B", program: "Engineering", year: 1 },
  { _id: "4", name: "Adam Brooks", studentId: "STU-1004", className: "BUS-3C", program: "Business", year: 3 }
];

export const sampleAbsences = sampleStudents.map((student, index) => ({
  _id: String(index),
  student,
  className: student.className,
  subject: index % 2 ? "Algorithms" : "Calculus",
  sessionType: index % 2 ? "regular" : "exam",
  status: index % 2 ? "present" : "absent",
  date: new Date().toISOString()
}));
