/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f4f2eb',
          100: '#e8dfd0',
          500: '#7a5b2d',
          600: '#634821',
          800: '#3b2a16',
        },
        accent: {
          500: '#4f7a3c',
          600: '#365f2f',
        },
      },
      boxShadow: {
        premium: '0 20px 60px -30px rgba(56, 39, 18, 0.45)',
      },
    },
  },
  plugins: [],
};

