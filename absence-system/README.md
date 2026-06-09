# Absence OS

Modern full-stack university absence management system for exams and regular sessions.

## Stack

- Frontend: React, Vite, Tailwind CSS, Framer Motion, Recharts, Lucide
- Backend: Node.js, Express, JWT, Socket.IO
- Database: MongoDB
- Reports: PDFKit

## Features

- JWT login for Admin and Professor roles
- Futuristic glassmorphism dashboard
- Fullscreen animated loading screen during page transitions
- Overview cards for students, absences, and exams
- Attendance trend chart
- Absence management with class, subject, and student filters
- Student profiles with attendance history and absence percentage
- Daily and exam-session PDF report export
- Realtime notification channel through Socket.IO
- Dark/light mode toggle
- Responsive sidebar layout

## Run Locally

1. Start MongoDB locally.

2. Backend:

```bash
cd backend
copy .env.example .env
npm install
npm run seed
npm run dev
```

Seed users:

- Admin: `admin@university.edu` / `admin123`
- Professor: `professor@university.edu` / `prof123`

3. Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## Project Structure

```text
absence-system/
  backend/
    src/
      middleware/
      models/
      routes/
      utils/
      server.js
  frontend/
    src/
      components/
      context/
      data/
      pages/
      App.jsx
      main.jsx
```

## Notes

The frontend includes demo login buttons, so the UI can be explored before the backend is running. PDF export requires a real backend login token.
