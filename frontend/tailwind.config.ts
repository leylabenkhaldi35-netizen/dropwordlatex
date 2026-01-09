import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          500: "#e11d48",
          600: "#be123c"
        }
      }
    }
  },
  plugins: []
};

export default config;
