import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcssVite from '@tailwindcss/vite';

export default defineConfig({
  plugins: [vue(), tailwindcssVite()],
});
