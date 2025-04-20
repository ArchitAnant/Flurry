/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Red Hat Display"', 'sans-serif'],
      },
      colors: {
        lightGray: '#CDCDCD',     
        darkGray : '#A3A3A3',
        accent: '#FF007F',
        lightHighlight: '#80FFBF',
        highlight : '#00FF7F',
      },
    },
  },
  plugins: [],
}

