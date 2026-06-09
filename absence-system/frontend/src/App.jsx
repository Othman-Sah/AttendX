import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { io } from "socket.io-client";
import { useAuth } from "./context/AuthContext.jsx";
import Login from "./pages/Login.jsx";
import Shell from "./components/Shell.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Absences from "./pages/Absences.jsx";
import Students from "./pages/Students.jsx";
import Reports from "./pages/Reports.jsx";
import Loader from "./components/Loader.jsx";

const pages = {
  dashboard: Dashboard,
  absences: Absences,
  students: Students,
  reports: Reports
};

export default function App() {
  const { user } = useAuth();
  const [page, setPage] = useState("dashboard");
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState("System online");
  const [light, setLight] = useState(false);

  useEffect(() => {
    document.body.classList.toggle("light", light);
  }, [light]);

  useEffect(() => {
    if (!user) return;
    const socket = io(import.meta.env.VITE_SOCKET_URL || "http://localhost:5000", { transports: ["websocket"] });
    socket.on("notification", (payload) => setNotice(payload.message));
    socket.on("absence:updated", () => setNotice("Absence record updated in realtime."));
    return () => socket.disconnect();
  }, [user]);

  function navigate(nextPage) {
    setLoading(true);
    setTimeout(() => {
      setPage(nextPage);
      setLoading(false);
    }, 520);
  }

  if (!user) return <Login />;

  const ActivePage = pages[page];

  return (
    <Shell page={page} onNavigate={navigate} notice={notice} light={light} setLight={setLight}>
      <AnimatePresence mode="wait">
        {loading ? (
          <Loader key="loader" />
        ) : (
          <motion.div
            key={page}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -18 }}
            transition={{ duration: 0.32 }}
          >
            <ActivePage />
          </motion.div>
        )}
      </AnimatePresence>
    </Shell>
  );
}
