import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

// GitHub Pages project site: base MUST equal "/<RepoName>/".
const BASE = "/OhioElections/";

export default defineConfig({
  base: BASE,
  define: {
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
  },
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.png", "icons/apple-touch-icon.png"],
      manifest: {
        name: "Ohio Elections",
        short_name: "Elections",
        description: "What is on the ballot in each Ohio county — candidates, the statewide issue and local levies and questions — from the Boards of Elections.",
        theme_color: "#1a2a3a",
        background_color: "#1a2a3a",
        display: "standalone",
        orientation: "any",
        scope: BASE,
        start_url: BASE,
        icons: [
          { src: "icons/pwa-192.png", sizes: "192x192", type: "image/png" },
          { src: "icons/pwa-512.png", sizes: "512x512", type: "image/png" },
          { src: "icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
        ],
      },
      workbox: {
        // Ballot files are a few KB per county; precache them so the ballot reads offline.
        globPatterns: ["**/*.{js,css,html,png,svg,json}"],
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
      },
    }),
  ],
});
