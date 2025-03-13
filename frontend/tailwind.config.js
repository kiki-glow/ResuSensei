/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#102F6B',  // Deep Blue
        accent: '#D2232A',   // Bold Red
        dark: '#081A36',     // Navy/Dark BG
        lightGray: '#F3F4F6', // Soft Gray for backgrounds
        white: '#FFFFFF',    // Clean White
      },
    },
  },
  plugins: [],
};
