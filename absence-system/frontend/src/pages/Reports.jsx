import { FileDown } from "lucide-react";
import { api } from "../api.js";

export default function Reports() {
  const token = localStorage.getItem("absence_token");

  async function exportPdf(sessionType) {
    if (!token || token === "demo-token") {
      alert("PDF export needs the backend running with a real login token.");
      return;
    }

    const response = await api.get(`/reports/pdf?sessionType=${sessionType}`, {
      responseType: "blob"
    });
    const url = URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `${sessionType}-absence-report.pdf`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {[
        { type: "regular", title: "Daily session report", desc: "Attendance and absence records for regular classes." },
        { type: "exam", title: "Exam session report", desc: "Absence report focused on ongoing exam sessions." }
      ].map((report) => (
        <article key={report.type} className="glass rounded-[2rem] p-6">
          <div className="grid h-14 w-14 place-items-center rounded-2xl bg-cyan-400/15 text-cyan-200">
            <FileDown />
          </div>
          <h2 className="mt-5 text-2xl font-black text-white">{report.title}</h2>
          <p className="mt-2 text-slate-400">{report.desc}</p>
          <button onClick={() => exportPdf(report.type)} className="glow-btn mt-6 rounded-2xl bg-cyan-400 px-5 py-3 font-black text-slate-950">Export PDF</button>
        </article>
      ))}
    </div>
  );
}
