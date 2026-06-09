import { Bell, ClipboardCheck, FileText, GraduationCap, LayoutDashboard, LogOut, Menu, Moon, Search, Sun, Users } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const nav = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "absences", label: "Absences", icon: ClipboardCheck },
  { id: "students", label: "Students", icon: Users },
  { id: "reports", label: "Reports", icon: FileText }
];

export default function Shell({ children, page, onNavigate, notice, light, setLight }) {
  const { user, logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="min-h-screen p-4 lg:p-6">
      <div className="mx-auto grid max-w-[1500px] grid-cols-1 gap-4 lg:grid-cols-[auto_1fr]">
        <aside className={`glass rounded-[2rem] p-4 transition-all ${collapsed ? "lg:w-24" : "lg:w-72"}`}>
          <div className="mb-7 flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="grid h-12 w-12 place-items-center rounded-2xl bg-cyan-400/15 text-cyan-200 shadow-glow">
                <GraduationCap />
              </div>
              {!collapsed && (
                <div>
                  <h1 className="font-black text-white">Absence OS</h1>
                  <p className="text-xs text-slate-400">University Command</p>
                </div>
              )}
            </div>
            <button className="rounded-xl p-2 text-slate-400 hover:bg-white/10" onClick={() => setCollapsed(!collapsed)}>
              <Menu size={18} />
            </button>
          </div>

          <nav className="space-y-2">
            {nav.map((item) => {
              const Icon = item.icon;
              const active = page === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left transition ${
                    active ? "bg-cyan-400 text-slate-950 shadow-glow" : "text-slate-300 hover:bg-white/10"
                  }`}
                >
                  <Icon size={20} />
                  {!collapsed && <span className="font-bold">{item.label}</span>}
                </button>
              );
            })}
          </nav>

          <div className="mt-8 rounded-3xl border border-cyan-300/15 bg-cyan-300/5 p-4">
            {!collapsed && (
              <>
                <p className="text-sm font-bold text-cyan-100">Role-based access</p>
                <p className="mt-1 text-xs text-slate-400">Current role: {user.role}</p>
              </>
            )}
          </div>
        </aside>

        <main className="min-w-0">
          <header className="glass mb-4 flex flex-col gap-4 rounded-[2rem] p-4 md:flex-row md:items-center md:justify-between">
            <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <Search size={18} className="text-slate-400" />
              <input className="w-full bg-transparent text-sm outline-none placeholder:text-slate-500" placeholder="Search student, class, report..." />
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2 rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-3 py-2 text-sm text-cyan-100">
                <Bell size={16} />
                <span>{notice}</span>
              </div>
              <button onClick={() => setLight(!light)} className="rounded-2xl border border-white/10 bg-white/5 p-3 text-slate-200">
                {light ? <Moon size={18} /> : <Sun size={18} />}
              </button>
              <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-2">
                <p className="text-sm font-black text-white">{user.name}</p>
                <p className="text-xs text-slate-400">{user.department}</p>
              </div>
              <button onClick={logout} className="rounded-2xl bg-rose-500/15 p-3 text-rose-200 hover:bg-rose-500/25">
                <LogOut size={18} />
              </button>
            </div>
          </header>

          {children}
        </main>
      </div>
    </div>
  );
}
