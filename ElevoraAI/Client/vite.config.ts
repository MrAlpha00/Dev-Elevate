import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    // Only expose the environment variables the client bundle actually reads.
    // Inlining the whole `process.env` object leaks every environment variable
    // (secrets included) into the browser bundle.
    "process.env.REACT_APP_GITHUB_TOKEN": JSON.stringify(
      process.env.REACT_APP_GITHUB_TOKEN ?? "",
    ),
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
});