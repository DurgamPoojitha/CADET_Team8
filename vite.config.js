import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Using relative base ('./') allows seamless deployment across any GitHub repository
  // name, subpath, or custom domain without breaking asset links.
  // Can be overridden via environment variable VITE_BASE_PATH if required.
  base: process.env.VITE_BASE_PATH || './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false
  }
});
