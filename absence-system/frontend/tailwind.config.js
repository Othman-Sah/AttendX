export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"]
      },
      colors: {
        void: "#0f172a",
        panel: "rgba(15, 23, 42, 0.72)",
        cyanGlow: "#22d3ee",
        blueGlow: "#38bdf8",
        purpleGlow: "#a855f7"
      },
      boxShadow: {
        glow: "0 0 35px rgba(34, 211, 238, 0.22)",
        card: "0 24px 70px rgba(0, 0, 0, 0.28)"
      }
    }
  },
  plugins: []
};
