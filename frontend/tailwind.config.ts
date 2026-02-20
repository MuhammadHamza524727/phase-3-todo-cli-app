import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],

  darkMode: "class", // or 'media' if you prefer system preference

  theme: {
    extend: {
      colors: {
        // Light theme base (default)
        background: "#f8fafc", // very light lavender-gray
        surface: "#ffffff",
        glass: "rgba(255, 255, 255, 0.65)", // for glassmorphism in light mode

        text: {
          primary: "#1e293b",
          secondary: "#64748b",
        },

        border: "#e0e7ff", // soft purple border

        accent: {
          DEFAULT: "#a78bfa", // light purple main
          hover: "#8b5cf6",
          light: "#c4b5fd",
          dark: "#7c3aed",
        },

        success: "#10b981",
        warning: "#f59e0b",
        error: "#ef4444",

        // Purple palette (accessible via purple-50, purple-100, etc.)
        purple: {
          50: "#f5f3ff",
          100: "#ede9fe",
          200: "#ddd6fe",
          300: "#c4b5fd",
          400: "#a78bfa",
          500: "#8b5cf6",
          600: "#7c3aed",
          700: "#6d28d9",
          800: "#5b21b6",
          900: "#4c1d95",
        },

        // Optional dark mode variants (you can toggle with dark: prefix)
        "dark-background": "#0f172a",
        "dark-surface": "#1e293b",
        "dark-text-primary": "#f1f5f9",
        "dark-text-secondary": "#94a3b8",
        "dark-border": "#334155",
      },

      borderRadius: {
        "4xl": "2rem", // larger modern rounded corners
        "5xl": "2.5rem",
      },

      boxShadow: {
        soft: "0 4px 20px -2px rgba(0, 0, 0, 0.05)",
        "soft-purple": "0 10px 25px -5px rgba(167, 139, 250, 0.18)",
        "purple-glow": "0 0 20px 2px rgba(167, 139, 250, 0.25)",
        glass: "0 8px 32px rgba(31, 38, 135, 0.07)",
      },

      // Optional: fluid typography helpers
      fontSize: {
        "fluid-xs": "clamp(0.75rem, 2.5vw + 0.1rem, 0.875rem)",
        "fluid-sm": "clamp(0.875rem, 3vw + 0.1rem, 1rem)",
        "fluid-base": "clamp(1rem, 3.5vw + 0.1rem, 1.125rem)",
        "fluid-lg": "clamp(1.125rem, 4vw + 0.2rem, 1.25rem)",
        "fluid-xl": "clamp(1.25rem, 4.5vw + 0.2rem, 1.5rem)",
      },

      transitionProperty: {
        height: "height",
        spacing: "margin, padding",
      },
    },
  },

  plugins: [
    // Optional: add official plugins if needed
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
  ],
};

export default config;