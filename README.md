# PersonalSite

Keshav Krishnan's personal portfolio. A single-page, Apple-clean scroll site: a hero introduction,
an interests statement, a startup, selected research, projects, a selected CV, a familiar-with skills
grid, and a contact footer. It is one self-contained HTML file with no framework, no build step, and
no runtime dependencies. Open it and it works.

## What is on the site

The page reads top to bottom as a narrative:

1. **Hero** name, one-line mission, short bio, and a portrait.
2. **What I am interested in** a short thesis on where the work is headed.
3. **Startup** Kilra, a digital-health OS, with revenue and App Store stats and three product shots.
4. **Selected research** the battery fast-charging safety filter (IEEE IECON 2026) and the AI/crypto
   grid-power study (George Mason ASSIP), each with a figure.
5. **Projects** FIREWATCH (probabilistic wildfire tracking) and CasCrop (a provisional-patent GNN for
   crop-waste forecasting).
6. **Selected CV** work and leadership entries (EP Industrial Coatings, VEX Robotics, VolunteerU).
7. **Familiar with** a three-column skills grid: Languages, Machine learning and research, Tools and systems.
8. **Contact** a dark footer with the closing line, a request-CV button, and email, GitHub and LinkedIn.

## Files

| Path | What it is |
|------|------------|
| `index.html` | The website. Self-contained: markup, styles, content and the animation script all live in this one file. |
| `assets/` | Images referenced by `index.html` (portrait, product screenshots, research figures). See `assets/README.md` for the list. |
| `design-source/` | An earlier static export kept only for reference. It is not the live site and does not render standalone. |

## How it is built (methods)

**One file, no build.** Everything is inline: a small CSS block in `<head>`, the page markup in
`<body>`, and one vanilla-JavaScript IIFE at the end. There is no bundler, no framework, and no
network request beyond the local images, so the page loads instantly and deploys as a static asset.

**Layout.** Sections are centered with `max-width` and fluid `clamp()` padding so type and spacing
scale smoothly from phone to desktop. Project and CV entries use a two-column CSS grid
(`repeat(auto-fit, minmax(...))`) that collapses to one column on narrow screens. Alternating entries
flip which side the text and image sit on, set from script by the entry index.

**Scroll animation system.** The script drives four reveal behaviors, all triggered as elements enter
the viewport through an `IntersectionObserver`:

- **reveal** fade and rise on enter (`omUp`).
- **unravel** headings are split into per-word `<span>`s in script, then each word animates in with a
  staggered blur-and-rotate (`omWord`), which produces the word-by-word settle on the large titles.
- **slide** paired text and image blocks come in from opposite sides (`omInL` / `omInR`).
- **zoom** figures scale in with a clip-path reveal (`omImg`) and lift slightly on hover.

A short intro probe enables motion only once the page is interactive, so nothing janks on first paint.
Rules (the thin dividers under section titles) grow with a `scaleX` animation, and arrow links nudge
their tip on hover. All of this is a few hundred lines of dependency-free JavaScript.

**Type and color.** System San Francisco stack, near-black text on white, a single dark contact
footer for contrast. No icon fonts or web fonts, so there is nothing extra to download.

## Preview locally

```bash
python3 -m http.server 8787
```

Then open http://localhost:8787/index.html

## Deploy

It is a static site, so there is nothing to build. Push it and enable GitHub Pages on the branch, or
drag the folder onto any static host. The only requirement is that the `assets/` images ship alongside
`index.html`.

## Editing

- Content lives directly in the markup of `index.html`; edit the text of a section in place.
- To add a project or CV entry, copy an existing `data-entry` block and swap its text and image; the
  script picks up the new block and alternates its layout automatically.
- To change the skills grid, edit the three columns under the "Familiar with" section.
