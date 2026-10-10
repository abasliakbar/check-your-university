# Redesign Brief: Keçid Balları

You are redesigning an existing, working web app called "Keçid Balları": a university admission score guide for Azerbaijani students. Files to edit: `index.html`, `style.css`, `app.js` (only if a markup change requires it). Do NOT touch `data/` or `scraper/`.

## GOAL

Make the site look serious, official and trustworthy, like a government or university information portal. Not a startup landing page. Calm, precise, readable. It must work comfortably on phones (design mobile-first at 390px wide, then scale up to desktop).

## STEP 1 - READ BEFORE CODING

Read these skills in `.agents/skills/` and apply them:

- `redesign-existing-projects` (process: how to restyle without breaking the project)
- `design-taste-frontend` (general taste and quality bar)
- `minimalist-ui` (flat surfaces, restraint)
- `stitch-design-taste` (read both `SKILL.md` and `DESIGN.md`)
- `brandkit` (keep the "K" logo mark consistent with the new navy palette)
- `gpt-taste` (read its contents and apply whatever fits)
- `high-end-visual-design` (use ONLY for typography, spacing and alignment quality; ignore any effects, glass, glow or heavy motion it suggests)
- `full-output-enforcement` (output complete files, no placeholders or truncation)

Do NOT use: `industrial-brutalist-ui`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `image-to-code`, `design-taste-frontend-v1` (outdated duplicate).

**PRIORITY RULE:** if any skill conflicts with STEP 3 (design system), STEP 4 (layout) or STEP 5 (don'ts) below, this document wins. Skills only fill gaps this document does not specify.

Then read `index.html`, `style.css` and `app.js` fully. Before editing, write a short list of the IDs, classes and data attributes that `app.js` depends on. Keep all of them unchanged.

## STEP 2 - HARD CONSTRAINTS

- Visual redesign only. Do not change functionality: score calculation, group tabs (1-5), university dropdown, specialty search, the "only eligible" checkbox, data loading.
- Keep all Azerbaijani text exactly as it is.
- No new features, no new libraries, no frameworks. Plain HTML/CSS/JS.

## STEP 3 - DESIGN SYSTEM (use exactly these)

### Colors (define as CSS variables)

| Variable | Value | Use |
|---|---|---|
| `--navy` | `#0B2545` | header, primary button, active tab, table section headers text |
| `--blue` | `#1F4E8C` | links, focus ring, secondary accents |
| `--ink` | `#1A2433` | body text |
| `--muted` | `#5B6675` | secondary text, labels |
| `--bg` | `#F4F6F9` | page background |
| `--surface` | `#FFFFFF` | cards, table |
| `--line` | `#D5DBE3` | 1px borders |
| `--ok` | `#1E7B4F` | status only, never decoration |
| `--warn` | `#B7791F` | status only, never decoration |
| `--bad` | `#B3261E` | status only, never decoration |

### Typography

- Headings: "Source Serif 4", Georgia, serif, weight 600.
- Body/UI: "Inter", system-ui, sans-serif.
- All numbers (scores, passing scores): `font-variant-numeric: tabular-nums`.
- Base size 16px on mobile (never smaller than 14px for any text), line-height 1.5.

### Shape and depth

- Border radius 6px for inputs, buttons, tabs; 8px for cards. No pill shapes.
- Separation by 1px borders only. At most one very subtle shadow: `0 1px 2px rgba(11,37,69,0.06)`.
- Spacing scale: 4, 8, 12, 16, 24, 32, 48.

## STEP 4 - LAYOUT

**Header:** slim solid navy bar with the logo mark and "Keçid Balları" in white, subtitle on the right (hidden on mobile).

**Calculator section:** a white card with a 1px border (NOT a big dark hero block). Title in serif, short description, two inputs side by side on desktop and stacked on mobile, large numeric inputs (min height 48px, `inputmode="decimal"`), full-width navy "Hesabla" button on mobile. The result (0 / 700) is shown in the same card as a large serif number. Keep the existing gauge, but make it flat: thin stroke, navy on a light grey track, no glow.

**Group tabs:** one horizontally scrollable row on mobile (no wrapping, hidden scrollbar, scroll-snap), rectangular 6px tabs, active tab solid navy with white text, inactive white with 1px border.

**Filters:** stacked on mobile, in one row on desktop, inside a white card.

**Specialties on MOBILE (under 768px):** replace the wide table with compact list rows. Each row: specialty name on the left (semi-bold, may wrap to 2 lines), the 2026 passing score on the right (bold, tabular), and below a muted small line with 2025 score, form and language as small plain-text tags (1px border, 4px radius, no colors). University names are sticky section headers with a light `--bg` background and navy text.

**Specialties on DESKTOP:** keep the table, with a sticky header row, 1px row dividers, no zebra stripes, generous row padding.

Tap targets at least 44x44px. No horizontal page scroll at any width.

## STEP 5 - STRICT DON'Ts

- No blur, no `backdrop-filter`, no glassmorphism, no glow, no neon, no decorative gradients, no emoji, no decorative illustrations, no animated backgrounds.
- No more than one accent color visible at a time. Do not use orange/yellow for buttons.
- Animations: only 150ms color/border transitions on hover and focus. Respect `prefers-reduced-motion`.
- Do not invent new copy, badges or sections.

## STEP 6 - ACCESSIBILITY

Text contrast WCAG AA minimum. Visible focus ring on all interactive elements (2px `--blue` outline, 2px offset). Labels remain associated with inputs.

## STEP 7 - VERIFY

After editing, check the page at 390px, 768px and 1280px widths. Confirm: no horizontal scroll, all tabs/filters/calculator still work, no console errors. Then give me a short summary (max 10 lines) of what changed in each file.
