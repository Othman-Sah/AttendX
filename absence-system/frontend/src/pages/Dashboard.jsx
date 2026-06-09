import { Activity, CalendarClock, UserCheck } from "lucide-react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import StatCard from "../components/StatCard.jsx";
import { mockTrends } from "../data/mock.js";

export default function Dashboard() {
  return (
    <div className="space-y-4">
      <section className="grid gap-4 md:grid-cols-3">
        <StatCard icon={UserCheck} label="Total students" value="1,284" detail="+42 registered this month" tone="cyan" />
        <StatCard icon={Activity} label="Absences today" value="37" detail="12 during exam sessions" tone="purple" />
        <StatCard icon={CalendarClock} label="Exams ongoing" value="8" detail="Across 5 departments" tone="blue" />
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.35fr_0.65fr]">
        <div className="glass rounded-[2rem] p-5">
          <div className="mb-5">
            <h2 className="text-xl font-black text-white">Attendance trends</h2>
            <p className="text-sm text-slate-400">Regular sessions and exam presence rate.</p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockTrends}>
                <defs>
                  <linearGradient id="present" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.55} />
                    <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.16)" />
                <XAxis dataKey="day" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid rgba(148,163,184,.2)", borderRadius: 16 }} />
                <Area type="monotone" dataKey="present" stroke="#22d3ee" fill="url(#present)" strokeWidth={3} />
                <Area type="monotone" dataKey="absent" stroke="#a855f7" fill="rgba(168,85,247,.14)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass rounded-[2rem] p-5">
          <h2 className="text-xl font-black text-white">System alerts</h2>
          <div className="mt-5 space-y-3">
            {["Exam absence threshold reached in MED-1A", "3 pending professor confirmations", "Daily PDF report ready"].map((alert) => (
              <div key={alert} className="rounded-2xl border border-cyan-300/15 bg-cyan-300/5 p-4 text-sm text-slate-300">{alert}</div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
