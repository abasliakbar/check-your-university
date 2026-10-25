# Plan: Full Visual Redesign From Scratch (check-your-university / "Keçid Balları")

## Goal
Rebuild the visual design of the site from scratch. The project is already fully functional, so do NOT change any logic, data handling, scraper, or calculation code, and do NOT add new features. Only the UI layer changes (HTML structure, CSS, and minimal UI-related JS such as class toggles and animations).

Use the installed taste-skills in `.agents/skills` as design guidance, but follow the decisions in this document where they differ.

## About the Site
Students enter their score (graduation score max 300 + block exam max 400 = 700), choose a group (1st–5th), and the site lists specialties/universities with their passing scores. The entire site is in Azerbaijani. Keep all existing functional text; the only new copy is the hero text and footer note suggested below (adjust wording if needed).

## Scope
- Allowed to edit: `index.html`, `style.css`, and UI-only parts of `app.js` (rendering markup, class names, animation hooks).
- Do NOT touch: score calculation logic, filtering logic, `scraper/`, `data/`.
- Preserve existing element IDs and data attributes that `app.js` depends on, or update both sides consistently and verify nothing breaks.

## Steps
1. Read `index.html`, `style.css`, `app.js`, and the taste-skills in `.agents/skills`.
2. Give a short plan: what will be rebuilt, which IDs/classes `app.js` depends on, and any risk.
3. Wait for approval, then implement.
4. Verify using the checklist at the end.

## Design Decisions
- **Layout:** single page, top to bottom: hero → score input → group selection → results → footer. No multi-step screens.
- **Feel:** very clean and simple, Apple / Linear style. Lots of whitespace, restrained UI, strong typography, no decoration for its own sake.
- **Theme:** light only. No dark mode, no theme toggle.
- **Brand:** text-only "Keçid Balları" (small wordmark at the top). No logo.
- **Typography:** Inter from Google Fonts with the `latin-ext` subset so Azerbaijani letters (ə, ı, ş, ç, ğ, ö, ü, İ) render correctly. System-font fallback stack. Clear hierarchy: large bold hero heading, medium labels, line height 1.5+, tabular numbers for scores.
- **Shape:** consistent border radius (10–12px), 1px borders, very soft shadows at most. No heavy blur, glassmorphism, big gradients, or colored shadows.
- **Container:** centered, max-width about 720px on desktop, comfortable side padding on mobile.

## Color System (define all as CSS variables in `:root`)

```css
:root {
  --bg: #ffffff;
  --surface: #f8fafc;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --text: #0f172a;
  --text-muted: #64748b;
  --accent: #047857;        /* emerald, dark enough for white text (AA) */
  --accent-hover: #065f46;
  --accent-press: #064e3b;
  --accent-bright: #10b981; /* non-text use only: dots, badges, markers, progress */
  --accent-soft: #ecfdf5;   /* subtle backgrounds for qualified rows */
  --danger: #dc2626;
  --focus-ring: #047857;
}
```

Rules: no hard-coded colors outside `:root`. Remove the old `#a6a68d` completely. Use the accent sparingly: primary button, selected group chip, qualified-row marker, focus ring.

## Sections

### 1. Top bar
Small text wordmark "Keçid Balları" on the left. No navigation needed.

### 2. Hero
- Big bold heading, e.g. "Keçid balını hesabla, universitetini seç" (suggested copy).
- One short supporting line, e.g. "Balını daxil et, qrupunu seç və sənə uyğun ixtisasları gör." (suggested copy).
- Generous spacing below before the score input.

### 3. Score input
- Large, clear inputs with visible labels for the graduation score (max 300) and block exam score (max 400); show the total out of 700.
- Focus ring in `--focus-ring`, inline validation using `--danger` without layout jumps.
- Inputs at 16px+ font size (prevents iOS zoom), height at least 48px.

### 4. Group selection
- Segmented control or pill chips for groups 1–5.
- Selected: `--accent` background, white text. Unselected: `--surface` background with `--border`.
- Touch targets at least 44px.

### 5. Primary button
- Background `--accent`, white text, hover `--accent-hover`, pressed `--accent-press`.
- Full width on mobile.

### 6. Results
- Compact list, NOT big cards. Each row: specialty name on the left (university as small muted secondary text if present) and passing score on the right, bold, tabular numbers.
- White rows separated by 1px `--border` dividers inside a single rounded container.
- Rows the student's score qualifies for get an `--accent-soft` background and a small `--accent-bright` marker or badge (use the existing wording if the site already has one).
- On mobile each specialty stays on one line (name + score); long names wrap gracefully or truncate with ellipsis.
- Empty and "no results" states: simple muted text, centered.

### 7. Footer
- Short muted note, e.g. "Məlumatlar məlumat xarakterlidir. Dəqiq məlumat üçün rəsmi mənbələrə baxın." (suggested copy).
- Small text, `--text-muted`, with top divider.

## Animations (light only)
- Buttons and chips: 150–200ms transitions (background change, `translateY(-1px)` on hover, `scale(0.98)` on press).
- Results: gentle fade-in with 4–8px slide-up when they appear, tiny stagger (max about 30ms per item, capped total).
- No looping or distracting animations. Respect `prefers-reduced-motion` by disabling animations.

## Responsive / Mobile-First
- Design for 360–430px first, then scale up.
- No horizontal scrolling at any width.
- Comfortable thumb-friendly spacing; results list stays compact on phones.

## Accessibility
- Semantic HTML (header, main, section, footer), labels bound to inputs, visible keyboard focus (2px outline, 2px offset).
- WCAG AA contrast for all text.
- `lang="az"` on the `<html>` element.

## Verification Checklist
- [ ] Score calculation, group filtering, and results data work exactly as before.
- [ ] No hard-coded colors outside `:root`; `#a6a68d` is gone.
- [ ] No blur, gradients, or colored shadows.
- [ ] Inter loads with Azerbaijani letters rendering correctly.
- [ ] Single-page flow: hero → score → group → results → footer.
- [ ] Results list is compact on mobile (name + score per row).
- [ ] Animations are light and disabled under `prefers-reduced-motion`.
- [ ] Looks correct at 360px, 430px, tablet, and desktop widths.
- [ ] No console errors.

## Final Output
Give a short summary of the files changed and confirm that no functionality was altered.
