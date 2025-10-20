import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["beacon.theol.au"],
    proxy: {
      "/api": {
        target: "http://localhost:5961/",
      },
      "/docs": {
        target: "http://localhost:5961/",
      },
      "/openapi.json": {
        target: "http://localhost:5961/",
      },
    },
  },
});
