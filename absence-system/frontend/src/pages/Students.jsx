import { useState } from "react";
import { sampleStudents } from "../data/mock.js";

export default function Students() {
  const [active, setActive] = useState(sampleStudents[0]);

  return (
    <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
      <div className="glass rounded-[2rem] p-5">
        <h2 className="text-2xl font-black text-white">Student profiles</h2>
        <div className="mt-5 space-y-3">
          {sampleStudents.map((student) => (
            <button key={student._id} onClick={() => setActive(student)} className={`w-full rounded-2xl p-4 text-left ${active._id === student._id ? "bg-cyan-400 text-slate-950" : "bg-white/5 hover:bg-white/10"}`}>
              <p className="font-black">{student.name}</p>
              <p className="text-sm opacity-75">{student.studentId} · {student.className}</p>
            </button>
          ))}
        </div>
      </div>

      <div className="glass rounded-[2rem] p-6">
        <p className="text-sm text-cyan-200">Profile</p>
        <h2 className="mt-1 text-3xl font-black text-white">{active.name}</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl bg-white/5 p-4"><p className="text-sm text-slate-400">Student ID</p><strong>{active.studentId}</strong></div>
          <div className="rounded-2xl bg-white/5 p-4"><p className="text-sm text-slate-400">Class</p><strong>{active.className}</strong></div>
          <div className="rounded-2xl bg-white/5 p-4"><p className="text-sm text-slate-400">Absence %</p><strong>8%</strong></div>
        </div>
        <div className="mt-6 rounded-3xl border border-white/10 bg-white/5 p-5">
          <h3 className="font-black text-white">Attendance history</h3>
          <div className="mt-4 space-y-3">
            {["Calculus - Present", "Algorithms - Absent", "Physics - Present", "Exam: Data Structures - Present"].map((item) => (
              <div key={item} className="flex items-center justify-between rounded-2xl bg-slate-950/40 p-3 text-sm">
                <span>{item}</span>
                <span className="text-slate-500">2026-04-28</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
