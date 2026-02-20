---
name: frontend-pages-components
description: Build clean, responsive web pages, reusable components, layouts and modern styling. Core frontend building block skill.
---
# Frontend – Pages, Components, Layout & Styling

## Instructions

1. **Page Structure & Semantics**
   - Use semantic HTML5 elements (`<header>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<nav>`)
   - Include proper document outline (h1 → h2 → h3 hierarchy)
   - Add ARIA landmarks when needed (role="banner", role="main", etc.)

2. **Layout Systems** (choose one primary system per project)
   - Flexbox → for navigation bars, card grids, centered content, one-dimensional layouts
   - CSS Grid → for overall page layout, dashboards, galleries, multi-dimensional arrangements
   - Container queries + modern layout (2024–2026 style) when building reusable card/list components

3. **Component Thinking**
   - Build small, reusable, single-responsibility components
   - Use composition: Button → Card → Section → Page
   - Name components clearly: `PrimaryButton`, `FeatureCard`, `TestimonialItem`, `PricingTier`
   - Support variants (size, color, state: hover/focus/disabled)

4. **Styling Approach** (pick consistent strategy)
   - Utility-first (Tailwind CSS)
   - CSS Modules / Scoped styles
   - Modern CSS (cascade layers, `:has()`, custom properties, oklch colors)
   - Design tokens: define --primary, --radius, --spacing-4, etc.

5. **Responsive & Mobile-first Rules**
   - Start with mobile (min-width media queries going up)
   - Use relative units: rem, em, ch, vw/vh, clamp()
   - Fluid typography: `font-size: clamp(1.25rem, 5vw + 0.5rem, 2.5rem)`
   - Respect reduced motion & color-scheme preferences

## Best Practices
- Mobile-first + progressive enhancement
- Single source of truth for colors, spacing, typography (design tokens)
- Components should be testable in isolation (Storybook / Ladle mindset)
- Aim for Core Web Vitals: LCP < 2.5s, CLS < 0.1, FID/INP < 150ms
- Use `aspect-ratio` instead of padding-bottom hacks
- Prefer `:focus-visible` over `:focus` for keyboard users
- Avoid `!important` except in very specific utility overrides

## Example – Modern 2026 Dark Glassmorphism Theme (Neon Violet Accent)

```html
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>SpekkitPlus – 2026 Edition</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            background: '#02040a',      // deep cosmic black
            surface:   '#0a0f1a',       // dark base for glass
            glass:     'rgba(10, 15, 26, 0.45)', // translucent glass
            text: {
              primary:   '#f1f5f9',
              secondary: '#94a3b8'
            },
            accent: {
              DEFAULT: '#8b5cf6',       // vivid neon violet
              hover:   '#7c3aed',
              glow:    '#a78bfa'        // glow / lighter variant
            },
            border:    '#1e293b'
          },
          backdropBlur: { xs: '3px', sm: '6px' },
          boxShadow: {
            'neon': '0 0 35px -10px rgba(139, 92, 246, 0.55)',
            'glass': '0 10px 40px rgba(0, 0, 0, 0.4)'
          }
        }
      }
    }
  </script>
  <style>
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body class="bg-background text-text-primary antialiased font-sans">

  <!-- Glassmorphic Header -->
  <header class="sticky top-0 z-50 border-b border-border/40 bg-glass backdrop-blur-sm shadow-glass">
    <nav class="mx-auto max-w-7xl px-6 py-5 flex items-center justify-between">
      <a href="/" class="font-black text-2xl bg-clip-text text-transparent bg-gradient-to-r from-accent to-accent-glow">
        SpekkitPlus
      </a>
      <div class="hidden md:flex gap-10">
        <a href="#features" class="text-text-secondary hover:text-text-primary transition duration-300">Features</a>
        <a href="#pricing" class="text-text-secondary hover:text-text-primary transition duration-300">Pricing</a>
        <a href="#docs"   class="text-text-secondary hover:text-text-primary transition duration-300">Docs</a>
      </div>
      <button class="rounded-xl bg-accent px-7 py-3 font-semibold text-background hover:bg-accent-hover transition shadow-neon hover:shadow-neon/70 transform hover:-translate-y-0.5 duration-200">
        Get Access
      </button>
    </nav>
  </header>

  <!-- Hero with subtle orb glow -->
  <main>
    <section class="relative min-h-[90vh] grid place-items-center px-6 py-28 md:py-44 overflow-hidden">
      <!-- Background glow orbs -->
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute -top-20 left-1/4 w-[500px] h-[500px] bg-accent/20 rounded-full blur-3xl opacity-40 animate-pulse-slow"></div>
        <div class="absolute bottom-10 right-1/4 w-[400px] h-[400px] bg-accent-glow/15 rounded-full blur-3xl opacity-30"></div>
      </div>

      <div class="relative max-w-5xl text-center space-y-12 z-10">
        <h1 class="text-5xl md:text-7xl font-black leading-tight tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-text-primary via-text-primary to-accent">
          Build. Launch.<br>Dominate.
        </h1>
        <p class="text-xl md:text-2xl text-text-secondary max-w-3xl mx-auto leading-relaxed font-light">
          The all-in-one toolkit for creators & teams — faster workflows, stunning output, zero hassle. 2026 ready.
        </p>
        <div class="flex flex-col sm:flex-row gap-6 justify-center pt-10">
          <button class="bg-accent text-background px-10 py-5 rounded-2xl font-bold text-lg hover:bg-accent-hover transition shadow-neon hover:shadow-neon/80 transform hover:scale-105 duration-200">
            Start Free Trial
          </button>
          <button class="border border-border/50 bg-glass backdrop-blur-sm px-10 py-5 rounded-2xl font-semibold text-lg hover:bg-surface/30 hover:border-accent/50 transition duration-300">
            Watch Demo
          </button>
        </div>
      </div>
    </section>

    <!-- Features – Glass cards -->
    <section id="features" class="py-28 px-6 border-t border-border/30 bg-gradient-to-b from-background to-surface/20">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-4xl md:text-6xl font-black text-center mb-20 bg-clip-text text-transparent bg-gradient-to-r from-text-primary to-accent/70">
          Why SpekkitPlus in 2026
        </h2>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-glass backdrop-blur-md border border-border/40 rounded-3xl p-9 shadow-glass hover:shadow-neon hover:border-accent/60 transition-all duration-300 group">
            <div class="text-5xl mb-6 text-accent opacity-90 group-hover:scale-110 transition-transform">⚡</div>
            <h3 class="text-2xl font-bold mb-4">Lightning Speed</h3>
            <p class="text-text-secondary">Sub-100ms responses. Built for performance from day one.</p>
          </div>

          <!-- Add 2 more cards as needed -->
          <div class="bg-glass backdrop-blur-md border border-border/40 rounded-3xl p-9 shadow-glass hover:shadow-neon hover:border-accent/60 transition-all duration-300 group">
            <div class="text-5xl mb-6 text-accent opacity-90 group-hover:scale-110 transition-transform">✨</div>
            <h3 class="text-2xl font-bold mb-4">Glass Beauty</h3>
            <p class="text-text-secondary">Modern glassmorphism + neon glows that feel premium.</p>
          </div>

          <div class="bg-glass backdrop-blur-md border border-border/40 rounded-3xl p-9 shadow-glass hover:shadow-neon hover:border-accent/60 transition-all duration-300 group">
            <div class="text-5xl mb-6 text-accent opacity-90 group-hover:scale-110 transition-transform">🛠️</div>
            <h3 class="text-2xl font-bold mb-4">Dev-First</h3>
            <p class="text-text-secondary">Components, tokens & DX you actually enjoy using.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Add Pricing / CTA / Footer sections as needed -->

  </main>

  <footer class="border-t border-border/40 py-16 text-center text-text-secondary bg-glass backdrop-blur-sm">
    <p>© 2026 SpekkitPlus — Made with modern CSS & ambition</p>
  </footer>

</body>
</html>