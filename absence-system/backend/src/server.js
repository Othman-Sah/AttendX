import dotenv from "dotenv";
import express from "express";
import http from "http";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import { Server } from "socket.io";
import { connectDB } from "./utils/db.js";
import authRoutes from "./routes/auth.js";
import studentRoutes from "./routes/students.js";
import absenceRoutes from "./routes/absences.js";
import reportRoutes from "./routes/reports.js";
import dashboardRoutes from "./routes/dashboard.js";

dotenv.config();

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: process.env.CLIENT_URL || "http://localhost:5173" }
});

app.set("io", io);
app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_URL || "http://localhost:5173" }));
app.use(express.json());
app.use(morgan("dev"));

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", service: "absence-system-api" });
});

app.use("/api/auth", authRoutes);
app.use("/api/dashboard", dashboardRoutes);
app.use("/api/students", studentRoutes);
app.use("/api/absences", absenceRoutes);
app.use("/api/reports", reportRoutes);

io.on("connection", (socket) => {
  socket.emit("notification", {
    type: "system",
    message: "Realtime absence channel connected."
  });
});

const port = process.env.PORT || 5000;

connectDB().then(() => {
  server.listen(port, () => {
    console.log(`API running on http://localhost:${port}`);
  });
});
