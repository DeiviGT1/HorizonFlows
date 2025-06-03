/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary:   "#003F88",
        secondary: "#005DA8",
        accent:    "#21A0A0",
        neutral:   "#F5F7FA",
        muted:     "#7A7D7D",
      }
    },
  },
  plugins: [],
};