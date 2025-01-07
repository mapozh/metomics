import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    open: true,           // Automatically opens the browser
    port: 5173,           // Default port
    strictPort: true,     // Avoid port switching
    host: 'localhost',    // Bind to localhost

    // Enable SPA fallback to handle routing properly
    middlewareMode: false,
    fs: {
      allow: ['.'],
    },
    watch: {
      usePolling: true,
    },
    hmr: true,             // Enable Hot Module Replacement
  },
  build: {
    outDir: 'dist',        // Output directory for builds
    emptyOutDir: true,     // Clear old builds
  },
  base: '/',               // Ensure base URL is root
  esbuild: {
    jsx: 'automatic',
  },
});