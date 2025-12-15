/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // MANDATORY DESIGN SYSTEM - NO DEVIATIONS
        'studio-dark': '#0F1115',      // Base Background
        'studio-gray': '#1A1D23',      // Panel Background  
        'studio-light': '#2A2D35',     // Elevated Surfaces
        'studio-cyan': '#4ECDC4',      // Primary Accent (actions)
        'studio-amber': '#F7B731',     // Secondary Accent (warnings/highlights)
        'studio-border': 'rgba(255,255,255,0.06)', // Border Subtle
        'studio-text-primary': '#FFFFFF',    // Text Primary
        'studio-text-secondary': '#B8BCC8', // Text Secondary
        'studio-text-muted': '#6B7280',     // Text Muted
      },
      fontFamily: {
        // Typography System
        'ui': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Monaco', 'Menlo', 'monospace'],
      },
      fontSize: {
        // Exact Typography Scale
        'section': ['16px', { lineHeight: '1.4', fontWeight: '600' }],
        'label': ['12px', { lineHeight: '1.3', fontWeight: '500', letterSpacing: '0.05em' }],
        'body': ['14px', { lineHeight: '1.5', fontWeight: '400' }],
        'numeric': ['13px', { lineHeight: '1.4', fontWeight: '400' }],
      },
      borderRadius: {
        'studio': '12px',
        'studio-lg': '16px',
      },
      animation: {
        // Professional Animation System
        'fade-in': 'fadeIn 150ms ease-out',
        'slide-in': 'slideIn 200ms ease-out',
        'dissolve': 'dissolve 300ms ease-out',
        'shimmer': 'shimmer 2s ease-in-out infinite',
        'grain': 'grain 8s ease-in-out infinite',
        'breathe': 'breathe 4s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(8px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        dissolve: {
          '0%': { opacity: '0', transform: 'scale(0.98)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        shimmer: {
          '0%, 100%': { opacity: '0.3' },
          '50%': { opacity: '0.8' },
        },
        grain: {
          '0%, 100%': { opacity: '0.02' },
          '50%': { opacity: '0.05' },
        },
        breathe: {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '0.8' },
        },
      },
      backdropBlur: {
        'studio': '12px',
      },
    },
  },
  plugins: [],
}