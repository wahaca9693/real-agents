/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0A0D12',
        'bg-secondary': '#111520',
        'bg-card': '#161B27',
        'bg-hover': '#1E2535',
        'accent-primary': '#4F8EF7',
        'accent-secondary': '#7C5CFC',
        'accent-glow': 'rgba(79, 142, 247, 0.25)',
        'success': '#22C55E',
        'warning': '#F59E0B',
        'danger': '#EF4444',
        'text-primary': '#F1F5F9',
        'text-secondary': '#8B95A7',
        'text-muted': '#4B5563',
        'border': '#1E2D40',
        'border-active': 'rgba(79, 142, 247, 0.4)',
      },
      fontFamily: {
        'syne': ['Syne', 'sans-serif'],
        'ibm': ['IBM Plex Sans Arabic', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'fade-in': 'fadeIn 0.3s ease-out',
      },
      keyframes: {
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}