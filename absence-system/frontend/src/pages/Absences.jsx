import { useMemo, useState } from "react";
import { sampleAbsences, sampleStudents } from "../data/mock.js";

export default function Absences() {
  const [records, setRecords] = useState(sampleAbsences);
  const [search, setSearch] = useState("");
  const [className, setClassName] = useState("");
  const [subject, setSubject] = useState("");

  const filtered = useMemo(() => {
    return records.filter((record) => {
      const matchesSearch = `${record.student.name} ${record.student.studentId}`.toLowerCase().includes(search.toLowerCase());
      return matchesSearch && (!className || record.className === className) && (!subject || record.subject === subject);
    });
  }, [records, search, className, subject]);

  function toggle(recordId) {
    setRecords((rows) => rows.map((row) => row._id === recordId ? { ...row, status: row.status === "absent" ? "present" : "absent" } : row));
  }

  return (
    <div className="glass rounded-[2rem] p-5">
      <div className="mb-5 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-black text-white">Absence management</h2>
          <p className="text-sm text-slate-400">Mark students present or absent and filter by class, subject, and identity.</p>
        </div>
        <div className="grid gap-2 md:grid-cols-3">
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search name or ID" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <select value={className} onChange={(e) => setClassName(e.target.value)} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none">
            <option value="">All classes</option>
            {[...new Set(sampleStudents.map((s) => s.className))].map((item) => <option key={item}>{item}</option>)}
          </select>
          <select value={subject} onChange={(e) => setSubject(e.target.value)} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none">
            <option value="">All subjects</option>
            <option>Calculus</option>
            <option>Algorithms</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="text-slate-400">
            <tr>
              <th className="py-3">Student</th>
              <th>ID</th>
              <th>Class</th>
              <th>Subject</th>
              <th>Session</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((record) => (
              <tr key={record._id} className="border-t border-white/10">
                <td className="py-4 font-bold text-white">{record.student.name}</td>
                <td>{record.student.studentId}</td>
                <td>{record.className}</td>
                <td>{record.subject}</td>
                <td>{record.sessionType}</td>
                <td>
                  <span className={`rounded-full px-3 py-1 text-xs font-black ${record.status === "absent" ? "bg-rose-500/15 text-rose-200" : "bg-emerald-500/15 text-emerald-200"}`}>
                    {record.status}
                  </span>
                </td>
                <td>
                  <button onClick={() => toggle(record._id)} className="rounded-xl bg-cyan-400 px-3 py-2 text-xs font-black text-slate-950">Toggle</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
