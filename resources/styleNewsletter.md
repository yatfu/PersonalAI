# Web Page Style Ruleset

Reusable styling rules for any HTML page/artifact built in this workspace (reports, digests, dashboards, tools). Goal: consistent, lightweight, readable pages without re-deriving a design system every time.

## Core rules

1. **Neutral background by default.** Use true greys with no hue bias (e.g. `#F1F1EF` light / `#161615` dark), not tinted cream, sage, or blue-black, unless the subject specifically calls for a tinted ground.
2. **Minimal token set.** Seven CSS custom properties is enough for most pages: `--bg`, `--surface`, `--ink`, `--ink-soft`, `--accent`, `--accent2`, `--line`. Don't add `-strong`/`-faint` variants unless a real contrast problem shows up — extra tokens are the main source of CSS bloat.
3. **Description/body text should be comfortably large.** Intro/lede text ~1.2rem, body paragraphs ~1.05rem, line-height 1.6–1.65. Undersized body text is the most common readability mistake — don't default to ~0.9rem for anything meant to be read, only for metadata/labels.
4. **Write longer, more informative descriptions, not just longer sentences.** Each content block should carry a mechanism (what actually happens, in order) plus a concrete detail (a number, a name, a specific consequence) — not just padded adjectives. If there's a lot of information that's important for understanding the topic, don't skip it.
5. **No decorative structure that doesn't encode real information.** Skip connector lines, rails, or numbered badges unless the number/order is genuinely meaningful (a real ranking, a real sequence). Prefer flat `.card` lists with `display:flex; flex-direction:column; gap:` over nested grid/rail layouts.
6. **Both themes, always.** Define tokens on `:root`, override under `@media (prefers-color-scheme: dark)`, then override again under `:root[data-theme="dark"]` and `:root[data-theme="light"]` so the viewer's manual toggle always wins over the OS setting.

## Token template

Swap the six color values per subject; keep the variable names and the three-layer override pattern.

```css
:root {
  --bg: #F1F1EF;
  --surface: #FFFFFF;
  --ink: #1B1B1A;
  --ink-soft: #5B5B58;
  --accent: #C97A24;
  --accent2: #1E7A6C;
  --line: #D8D8D5;
  --font-display: 'Bahnschrift', 'SF Compact Display', 'Archivo Narrow', 'Arial Narrow', sans-serif;
  --font-body: Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Book Antiqua', serif;
  --font-mono: 'Cascadia Code', 'SF Mono', Consolas, 'Roboto Mono', monospace;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #161615; --surface: #1E1E1C; --ink: #ECECEA; --ink-soft: #A8A8A4; --accent: #E7A24C; --accent2: #4FC0AC; --line: #333331; }
}
:root[data-theme="dark"]  { --bg: #161615; --surface: #1E1E1C; --ink: #ECECEA; --ink-soft: #A8A8A4; --accent: #E7A24C; --accent2: #4FC0AC; --line: #333331; }
:root[data-theme="light"] { --bg: #F1F1EF; --surface: #FFFFFF; --ink: #1B1B1A; --ink-soft: #5B5B58; --accent: #C97A24; --accent2: #1E7A6C; --line: #D8D8D5; }
```

Pick `--accent` / `--accent2` to fit the subject's own vernacular (not a generic brand blue/purple). Verify contrast in both themes before shipping.

## Typography

Three font roles, no more:

- `--font-display` — headings only, used sparingly.
- `--font-body` — all reading text (paragraphs, descriptions). A serif or humanist face reads better at length than a geometric sans.
- `--font-mono` — metadata only: tags, labels, source links, timestamps, numbers.

Avoid Inter and Space Grotesk as the default choice — pick a stack that fits the specific subject instead of the generic AI-page default.

Type scale (starting point, adjust per page):

| Role | Size | Notes |
|---|---|---|
| h1 | `clamp(2rem, 5vw, 2.6rem)` | `text-wrap: balance`, constrain `max-width` in `ch` |
| lede/dek | `1.2rem` | line-height 1.6 |
| h2 (card/section title) | `1.2–1.3rem` | |
| body paragraph | `1.05rem` | line-height 1.6–1.65, `max-width: 58ch` |
| metadata/mono | `0.7–0.8rem` | letter-spacing ~0.05em for uppercase labels |

## Layout

- Single-column pages: `max-width: 720–760px`, centered, `padding: 3rem 1.5rem`.
- Space sibling blocks with a parent `flex`/`grid` + `gap`, not per-child margins.
- Wide content (tables, code) gets its own `overflow-x: auto` container.
- Cards: `border: 1px solid var(--line); border-radius: 6px; padding: ~1.2rem`. No shadows, no gradients, no rounded-full pills unless the subject calls for it.

## Checklist before shipping a page

- [ ] Background is a deliberate neutral or subject-appropriate tint, not left as a default
- [ ] Body/description text ≥1.05rem, lede ≥1.2rem
- [ ] Token count stays near 7 unless a real need justifies more
- [ ] Both `prefers-color-scheme` and `data-theme` overrides present
- [ ] No purely decorative structural element (numbers, rails, dividers) — everything present encodes real information
- [ ] Descriptions state a mechanism + a concrete detail, not just adjectives
