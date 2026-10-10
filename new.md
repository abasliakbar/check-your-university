# Redesign Brief: Keçid Balları

You are redesigning an existing, working web app called "Keçid Balları": a university admission score guide for Azerbaijani students. Files to edit: `index.html`, `style.css`, `app.js` (only for small additive animation hooks or markup changes the redesign requires). Do NOT touch `data/` or `scraper/`.

## GOAL

A modern, clean, fast-feeling UI with smooth, polished button animations and compact lists. It must work comfortably on phones (design mobile-first at 390px wide, then scale up to desktop). Modern does NOT mean flashy: no blur, no glass, no glow.

## STEP 1 - READ BEFORE CODING

Read these skills in `.agents/skills/` and apply them:

- `redesign-existing-projects` (process: how to restyle without breaking the project)
- `design-taste-frontend` (general taste and quality bar)
- `minimalist-ui` (flat surfaces, restraint)
- `stitch-design-taste` (read both `SKILL.md` and `DESIGN.md`)
- `brandkit` (keep the "K" logo mark consistent with the new palette)
- `gpt-taste` (read its contents and apply whatever fits)
- `high-end-visual-design` (use ONLY for typography, spacing and alignment quality; ignore any blur, glass, glow or heavy motion it suggests)
- `full-output-enforcement` (output complete files, no placeholders or truncation)

Do NOT use: `industrial-brutalist-ui`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `image-to-code`, `design-taste-frontend-v1` (outdated duplicate).

**PRIORITY RULE:** if any skill conflicts with STEP 3 (design system), STEP 4 (layout), STEP 5 (motion) or STEP 6 (don'ts) below, this document wins. Skills only fill gaps this document does not specify.

Then read `index.html`, `style.css` and `app.js` fully. Before editing, write a short list of the IDs, classes and data attributes that `app.js` depends on. Keep all of them unchanged.

## STEP 2 - HARD CONSTRAINTS

- Do not change functionality: score calculation, group tabs (1-5), university dropdown, specialty search, the "only eligible" checkbox, data loading.
- Keep all Azerbaijani text exactly as it is.
- No new features, no new libraries, no frameworks. Plain HTML/CSS/JS.
- Any JS you add must be purely presentational and must not modify calculation or filtering logic.

## STEP 3 - DESIGN SYSTEM (use exactly these)

### Colors (CSS variables)

| Variable | Value | Use |
|---|---|---|
| `--navy` | `#0B2545` | header, headings, university section titles |
| `--accent` | `#2F6BFF` | primary buttons, active tab, focus ring, links (the ONLY accent color) |
| `--accent-hover` | `#2559D9` | button hover |
| `--accent-soft` | `#EAF0FF` | soft highlight for active/selected states |
| `--ink` | `#16202E` | body text |
| `--muted` | `#5F6B7A` | secondary text, labels |
| `--bg` | `#F6F8FB` | page background |
| `--surface` | `#FFFFFF` | cards, list rows |
| `--line` | `#E3E8EF` | 1px borders |
| `--ok` / `--warn` / `--bad` | `#1E7B4F` / `#B7791F` / `#B3261E` | status only, never decoration |

### Typography

- Headings: "Plus Jakarta Sans" (fallback "Inter", system-ui), weight 700, slight negative letter-spacing (-0.02em).
- Body/UI: "Inter", system-ui, sans-serif.
- All numbers (scores): `font-variant-numeric: tabular-nums`.
- Base size 16px. Never below 14px for readable text; chips/tags may be 12px minimum.

### Shape and depth

- Radius: 10px for buttons/inputs, 14px for cards, 999px for tabs and tag chips.
- Soft shadow allowed, no blur effects: `0 1px 2px rgba(11,37,69,0.06), 0 4px 12px rgba(11,37,69,0.05)`.
- Spacing scale: 4, 8, 12, 16, 24, 32, 48.

## STEP 4 - LAYOUT

**Header:** slim clean bar (white or `--bg`, bottom 1px line) with the logo mark and "Keçid Balları". Subtitle on the right (hidden on mobile).

**Calculator section:** one card (no big dark hero block). Title, short description, two large inputs (min height 52px, `inputmode="decimal"`, side by side on desktop, stacked on mobile), full-width `--accent` "Hesabla" button on mobile. The result (0 / 700) sits in the same card as a large number. Keep the existing gauge, flat style: thin stroke in `--accent` on a light track, no glow.

**Group tabs:** one horizontally scrollable row on mobile (no wrapping, hidden scrollbar, scroll-snap). Pill tabs. Active tab solid `--accent` with white text, inactive white with 1px border.

**Filters:** stacked on mobile, one row on desktop, inside a card.

**Specialties = COMPACT LIST on every screen size (no wide table on mobile):**
- University name is a sticky section header (`--bg` background, `--navy` text, semi-bold).
- Each specialty is one compact row, about 56-64px tall, 1px bottom divider, no zebra stripes.
- Left: specialty name (15px, semi-bold, max 2 lines, ellipsis after that).
- Right: 2026 passing score (bold, tabular, 16-17px).
- Below the name: one muted line (13px) with 2025 score, then form and language as small outline chips. If a note ("Qeyd") exists, show it as a muted small text, never as a big badge.
- Desktop (min-width 768px): same row style, but as a grid with columns: name | form | language | 2026 | 2025 | note, with a sticky column header row. Rows stay compact.
- Row hover (only on devices with hover): background `--accent-soft` at low opacity.

Tap targets at least 44x44px. No horizontal page scroll at any width.

## STEP 5 - MOTION (smooth, subtle, fast)

Easing everywhere: `cubic-bezier(0.2, 0.8, 0.2, 1)`. Duration 180-240ms for UI, up to 600ms for the score count-up. Animate only `transform`, `opacity`, `background-color`, `box-shadow`, `border-color`, `stroke-dashoffset`.

**Buttons (primary "Hesabla" and all others):**
- Hover (only inside `@media (hover: hover)`): lift `translateY(-1px)`, shadow grows slightly, background goes to `--accent-hover`.
- Press (`:active`): `scale(0.97)` with a faster 90ms transition, shadow shrinks.
- Focus-visible: 2px `--accent` ring with 2px offset, fades in over 150ms.
- Optional: after clicking "Hesabla", a brief 200ms "pulse" (scale 1 to 1.03 to 1) on the result card.

**Tabs:** background and text color fade smoothly (200ms). Selected tab scrolls into view smoothly on mobile.

**Result:** the score number counts up from the previous value to the new value over ~600ms, and the gauge stroke animates with a CSS transition. Do not change how the score is calculated; only animate the display of the already-calculated value.

**Lists:** when the group changes or filters change, rows fade and slide in (opacity 0 to 1, translateY 6px to 0, 200ms) with a small stagger (20ms per row, only the first 12 rows). Never delay the actual content or block interaction.

**Inputs/select/checkbox:** border color and focus ring transition 150ms.

Respect `prefers-reduced-motion: reduce`: disable transforms, stagger and count-up, keep instant state changes.

## STEP 6 - STRICT DON'Ts

- No blur, no `backdrop-filter`, no glassmorphism, no glow, no neon, no decorative gradients, no emoji, no decorative illustrations, no animated backgrounds, no parallax, no bouncing or looping animations.
- Only one accent color (`--accent`). No orange/yellow buttons.
- No layout shift during animations. No animation that makes the list feel slow.
- Do not invent new copy, badges or sections.

## STEP 7 - ACCESSIBILITY

Text contrast WCAG AA minimum. Visible focus ring on all interactive elements. Labels remain associated with inputs.

## STEP 8 - VERIFY

After editing, check the page at 390px, 768px and 1280px widths. Confirm: no horizontal scroll, all tabs/filters/calculator still work, animations are smooth and not janky on a mobile viewport, no console errors. Then give me a short summary (max 10 lines) of what changed in each file.
