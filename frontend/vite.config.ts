import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

import { defineConfig } from 'vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["beacon.theol.au"],
    port: 9877,
    host: '10.42.42.3',
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
