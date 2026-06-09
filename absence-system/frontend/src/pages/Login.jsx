import { motion } from "framer-motion";
import { ShieldCheck } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const { login, demoLogin } = useAuth();
  const [email, setEmail] = useState("admin@university.edu");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      await login(email, password);
    } catch {
      setError("API unavailable or invalid credentials. Use demo mode or run the backend seed.");
    }
  }

  return (
    <div className="grid min-h-screen place-items-center p-4">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute left-[15%] top-[12%] h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
        <div className="absolute right-[12%] top-[20%] h-80 w-80 rounded-full bg-purple-500/20 blur-3xl" />
      </div>

      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} className="glass relative grid w-full max-w-5xl overflow-hidden rounded-[2rem] lg:grid-cols-[0.95fr_1.05fr]">
        <form onSubmit={submit} className="p-8 md:p-12">
          <div className="mb-8 flex items-center gap-3">
            <div className="grid h-12 w-12 place-items-center rounded-2xl bg-cyan-400 text-slate-950 shadow-glow">
              <ShieldCheck />
            </div>
            <div>
              <h1 className="text-2xl font-black text-white">Absence OS</h1>
              <p className="text-sm text-slate-400">Secure university attendance command</p>
            </div>
          </div>

          <h2 className="text-4xl font-black text-white">Welcome back</h2>
          <p className="mt-2 text-slate-400">Sign in as admin or professor to manage exam and regular absences.</p>

          {error && <div className="mt-5 rounded-2xl border border-rose-300/20 bg-rose-500/10 p-3 text-sm text-rose-100">{error}</div>}

          <div className="mt-8 grid gap-4">
            <label className="grid gap-2 text-sm font-bold text-slate-300">
              Email
              <input value={email} onChange={(e) => setEmail(e.target.value)} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-cyan-300" />
            </label>
            <label className="grid gap-2 text-sm font-bold text-slate-300">
              Password
              <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none focus:border-cyan-300" />
            </label>
          </div>

          <button className="glow-btn mt-6 w-full rounded-2xl bg-cyan-400 px-5 py-3 font-black text-slate-950">Login securely</button>

          <div className="mt-4 grid grid-cols-2 gap-3">
            <button type="button" onClick={() => demoLogin("admin")} className="rounded-2xl border border-white/10 px-4 py-3 text-sm font-bold text-slate-200 hover:bg-white/10">Demo Admin</button>
            <button type="button" onClick={() => demoLogin("professor")} className="rounded-2xl border border-white/10 px-4 py-3 text-sm font-bold text-slate-200 hover:bg-white/10">Demo Professor</button>
          </div>
        </form>

        <div className="scanner hidden min-h-[620px] bg-gradient-to-br from-slate-950 via-blue-950 to-cyan-950 p-10 lg:block">
          <div className="flex h-full flex-col justify-end">
            <div className="rounded-[2rem] border border-cyan-300/25 bg-white/10 p-6 backdrop-blur-xl">
              <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Live academic signal</p>
              <h3 className="mt-3 text-3xl font-black text-white">Apple dashboard meets futuristic university system.</h3>
              <p className="mt-3 text-slate-300">Fast, reliable, and role-aware absence tracking for exams and regular sessions.</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
