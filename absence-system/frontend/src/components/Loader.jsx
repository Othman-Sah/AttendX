import { motion } from "framer-motion";

export default function Loader() {
  return (
    <motion.div
      className="fixed inset-0 z-50 grid place-items-center bg-slate-950/92"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="scanner glass w-80 rounded-3xl p-8 text-center">
        <div className="mx-auto mb-5 h-20 w-20 rounded-full border-4 border-cyan-300/20 border-t-cyan-300 animate-spin" />
        <p className="text-lg font-black text-white">Loading system...</p>
        <p className="mt-2 text-sm text-slate-400">Processing academic data stream</p>
      </div>
    </motion.div>
  );
}
