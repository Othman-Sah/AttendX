import { motion } from "framer-motion";

export default function StatCard({ icon: Icon, label, value, detail, tone = "cyan" }) {
  const tones = {
    cyan: "from-cyan-400/20 to-blue-500/10 text-cyan-200",
    purple: "from-purple-400/20 to-fuchsia-500/10 text-purple-200",
    blue: "from-blue-400/20 to-cyan-500/10 text-blue-200"
  };

  return (
    <motion.article whileHover={{ y: -5 }} className="glass rounded-[2rem] p-5">
      <div className={`mb-5 grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br ${tones[tone]}`}>
        <Icon />
      </div>
      <p className="text-sm text-slate-400">{label}</p>
      <strong className="mt-1 block text-3xl font-black text-white">{value}</strong>
      <span className="mt-3 block text-xs text-slate-500">{detail}</span>
    </motion.article>
  );
}
