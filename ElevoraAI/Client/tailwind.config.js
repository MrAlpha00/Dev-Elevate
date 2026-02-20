/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        electric: {
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
        },
        neon: {
          500: '#10b981',
          600: '#059669',
        },
        cyber: {
          400: '#8b5cf6',
        },
        gray: {
          750: '#374151',
        },
      },
    },
  },
  plugins: [],
};
