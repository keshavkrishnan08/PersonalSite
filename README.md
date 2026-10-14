# PersonalSite

**Keshav Krishnan's portfolio: five hand-written HTML pages, one stylesheet, no framework, and no build step. An animated about page up front, and four plain, type-only pages for work, projects, research, and awards.**

A portfolio is read once, quickly, often on a phone, by someone deciding whether to keep going. Most of
that reader's questions are plain ones: what does this person do, what have they built, what have they
published, what have they won. This site answers the first one with a full-bleed about page, and the
rest the way a good CV does: a name, a role, one paragraph, a link, and nothing in the way.

Live site: **https://keshavkrishnan.vercel.app**

```
/            index.html     about: hero, portrait, interests, contact (system type, scroll motion)
/work        work.html      current and past roles, then skills
/projects    projects.html  FIREWATCH, CROSSING, GridWatch, crop waste forecasting
/research    research.html  paper, research in progress, patent
/awards      awards.html    research, robotics, leadership
             site.css       the shared tab bar and the inner-page type
             vercel.json    clean URLs: /work serves work.html
```

Say it once, plainly.

## The core idea

1. **Two registers.** The about page keeps its large type, portrait, and scroll motion. Every other page
   is text only, so the facts read at a glance and nothing animates between the reader and a link.
2. **One column, one size.** Inner pages sit in a single 580 px column set in 15 px Helvetica Neue at a
   1.6 line height. Section labels are 11 px uppercase with 0.08 em tracking. Entries hang: the name
   starts at the margin and the description is indented beneath it. Links are underlined at 30%
   opacity with a 3 px offset.
3. **Nothing to build.** Static HTML and one stylesheet. Vercel serves `/work` from `work.html` through
   `cleanUrls`, and every push to `main` deploys.

## What it does

| Page | What is on it |
|---|---|
| **Home** | Intro and portrait, "What I'm interested in," and a dark contact footer with email, GitHub, LinkedIn, and a CV request. A Markdown button opens the whole profile as copyable plain text. |
| **Work** | Currently: Kilra, CropConnect, George Mason ASSIP, Park Tudor VEX Robotics, Mock Trial, VolunteerU. Previously: EP Industrial Coatings. Then the skills list. |
| **Projects** | FIREWATCH, CROSSING, GridWatch, and crop waste forecasting, each with its stack and links to the live site and the code. |
| **Research** | 1. Research papers (IEEE IECON 2026), 2. research in progress (George Mason ASSIP), 3. patents (a U.S. provisional application with 26 claims). |
| **Awards** | Research, robotics, and leadership honors. |

## How it works

**Tab bar.** `site.css` defines one `.tabs` bar used on every page: 14 px links with 24 px gaps, muted
until hovered, and the current page marked with `aria-current="page"` in the text color at weight 500.
Below 420 px the gap tightens to 18 px so all five tabs stay on one line.

**Inner pages.** `body.doc` sets the column, type, and colors. `.group` spaces sections by 2.5 em,
`.label` sets the small uppercase headings, `.entry` is the hanging-indent role or project with a
`.desc` block indented 30 px further, `.pub` is a citation with a smaller muted `.meta` line, and `li`
items indent 30 px with 0.75 em between them.

**About page motion.** One script wires everything on `DOMContentLoaded`. Nothing is hidden until an
IntersectionObserver probe confirms the page is live; then the two large headings split into words
that settle in from a blur, the hero slides in from both sides, and blocks rise into place as they
enter the viewport, each playing once. Readers who ask their system for reduced motion get no
animation at all.

**Deploys.** The Vercel project is connected to this repository, so a push to `main` builds and
serves the site at keshavkrishnan.vercel.app. `.vercelignore` is an allowlist: only the five pages,
`site.css`, `llms.txt`, `vercel.json`, and `assets/` ship.

## Run it

```bash
python3 -m http.server 8787     # then open http://localhost:8787
```

Locally, open inner pages by file name (`/work.html`); the extensionless URLs come from Vercel.

## Layout

```
index.html       about page: markup, inline styles, motion script, Markdown overlay
work.html        roles and skills
projects.html    projects with links
research.html    paper, research in progress, patent
awards.html      honors
site.css         tab bar and inner-page typography
vercel.json      clean URLs
llms.txt         the profile as Markdown for language models
assets/          the portrait (also the link-preview image)
```

## Honesty

* There is no dark mode. Every page uses one light palette by design.
* The profile text is maintained by hand in the pages, the Markdown overlay, and `llms.txt`. Nothing
  keeps them in sync.
* Figures quoted on the site, such as revenue, research results, and awards, are not sourced in this
  repo. Each project's own repository is the place to check them.
