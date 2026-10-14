# PersonalSite

**Keshav Krishnan's portfolio: one hand-written HTML file with no framework, no build step, and no third-party requests, animated by about 150 lines of vanilla JavaScript.**

A portfolio is read once, quickly, often on a phone, by someone deciding whether to keep going. Many are framework apps that ship a runtime to render what is mostly static text. This one treats the page as a document. Everything lives in `index.html`, the content is plain markup, and motion is layered on only after the browser shows the page is live, so nothing stays hidden if the script fails or the reader never scrolls. The same content also ships as plain Markdown, once behind a button for people and once as `llms.txt` for language models.

Live site: **https://keshavkrishnan.vercel.app**

```
index.html  ->  first paint: every section visible, no script required
            ->  IntersectionObserver probe fires  ->  motion enabled
            ->  headings split into words; anything already on screen animates now
            ->  first scroll: hide what is below the fold, observe each element
            ->  element enters the viewport  ->  its keyframe plays once  ->  unobserved
```

Visible first, animated second.

## The core idea

1. **One file, nothing to build.** Markup, styles, and script sit in a single `index.html` (615 lines). There is no bundler, no package manifest, no web font, and no analytics. The only network requests are the local images in `assets/`, about 2 MB of optimized JPEG and SVG, lazy-loaded below the fold with intrinsic sizes so nothing shifts as they arrive.
2. **Visible by default, still on request.** The page renders complete without JavaScript, and readers who ask their system for reduced motion get the page with no animation at all. Motion switches on only after an IntersectionObserver probe confirms the page is live, and elements below the fold are hidden only after the first scroll event, right before they are observed.
3. **The same content in three forms.** The HTML page, a "Markdown" overlay with a copy button, and `llms.txt` carry the same text, so a reader or a model can take the whole page as plain text.

## What it does

| Piece | Detail |
|---|---|
| **Sections** | Intro with portrait, "What I'm interested in," Ventures, Selected research, Projects, Selected CV, "Familiar with" (three skill columns), and a dark contact footer. |
| **Navigation** | A fixed frosted-glass pill (`backdrop-filter: saturate(180%) blur(20px)`) with five anchor links and CSS smooth scrolling. |
| **Reveal** | 21 blocks animate once on entry. Plain blocks fade and rise into place (`omUp`, 1.05 s); blocks that hold an entry or a figure use the slide or zoom below. |
| **Unravel** | 8 large headings are split into one `<span>` per word in script, and each word settles in from a blur, a slight rotation, and a smaller scale (`omWord`, 0.98 s), staggered 56 ms apart. |
| **Alternating entries** | 10 text-and-image entries alternate sides by their index on the page: the script sets column order, text alignment, and which side each half slides in from (`omInL` / `omInR`, 155 px, 1.15 s, 90 ms apart). |
| **Zoom** | 11 figures scale to 1.03 on hover. The full-width FIREWATCH figure, which stands outside an entry, opens from a rounded inner rectangle with an animated `clip-path` (`omImg`, 1.35 s); the others slide in with their entry. |
| **Rules and arrows** | 5 section dividers grow with `scaleX` (`omLine`). 15 arrow links nudge their arrow 4 px on hover. |
| **Markdown view** | A fixed button opens the whole page as Markdown in a dialog, with Copy (Clipboard API), Close, Escape, and click-outside to dismiss. Below 920 px wide the button moves to the bottom-right corner, clear of the nav. |
| **Favicon and previews** | An inline base64 SVG monogram, so there is no icon file to fetch. A meta description, canonical URL, and Open Graph and Twitter tags give link previews a title, summary, and portrait. |

## How it works

**Markup and styles.** Two small `<style>` blocks hold the base rules, six `@keyframes`, a `prefers-reduced-motion` override, and the overlay styles. Everything else is inline on the elements, so each section can be read and edited in one place. Animation behavior is declared with data attributes (`data-reveal`, `data-unravel`, `data-entry`, `data-zoom`, `data-rule`, `data-arrow`) rather than classes.

**Layout.** Sections are centered with `max-width`, and type and spacing scale with `clamp()`, from phone to desktop. Entries use `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`, which collapses to one column on narrow screens without a single media query. Entry titles use `text-wrap: balance`, paragraphs `text-wrap: pretty`, and the body uses `overflow-x: clip` so off-screen slide-ins never create a horizontal scrollbar.

**Motion.** One IIFE wires everything on `DOMContentLoaded`. If the reader prefers reduced motion it stops after laying out the entries. Otherwise a probe observer on `<body>` calls `enableMotion` the first time it fires. That splits the unravel headings, plays every element whose top is already within 97% of the viewport, and arms a one-time scroll listener. On the first scroll, the remaining elements are hidden (words to opacity 0, rules to `scaleX(0)`, blocks to opacity 0) and handed to a second IntersectionObserver (threshold 0.01), which plays each element once and unobserves it. A passive scroll handler also plays anything within 99% of the viewport as a fallback. Each element is marked `data-played` so nothing animates twice.

**Theme.** A single light palette: near-black `#1d1d1f` on white, three grays for secondary text, a dark `#1d1d1f` footer for contrast, and a custom `::selection` color. Type is the system stack (`-apple-system`, BlinkMacSystemFont, Helvetica Neue), so San Francisco renders on Apple devices with nothing to download.

## Run it

```bash
python3 -m http.server 8787     # then open http://localhost:8787
```

To deploy, put `index.html`, `llms.txt`, and `assets/` on any static host. There is nothing to build.

## Layout

```
index.html         the whole site: markup, inline styles, motion script, Markdown overlay
llms.txt           the page as Markdown for language models (same text as the overlay)
assets/            portrait, App Store screenshots, project screenshots, figures
assets/README.md   where each image came from
```

## Honesty

* There is no dark mode. The page is one light palette by design.
* The content is maintained by hand in three places: the HTML, the Markdown overlay, and `llms.txt`.
  They match today, but nothing keeps them in sync.
* Four figures are illustrative drawings, not data plots: `research-charging.svg`,
  `research-energy.svg`, `robotics.svg`, and `crop-county.svg`, as `assets/README.md` notes.
* Figures quoted on the page, such as revenue, research results, and awards, are not sourced in this
  repo. Each project's own repository is the place to check them.
