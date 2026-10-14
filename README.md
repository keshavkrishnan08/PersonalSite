# PersonalSite

**Keshav Krishnan's portfolio: six hand-written HTML pages, one stylesheet, no framework, and no build step. An animated home page with a portrait, and five plain, type-only pages in a single centered column.**

A portfolio is read once, quickly, often on a phone, by someone deciding whether to keep going. Most of
that reader's questions are plain ones: what does this person do, what have they built, what have they
published, and what did they build it with. This site answers the first one on the home page, and
the rest the way a good CV does: a name, a role, a sentence or two, the tools it was built with, a
link, and nothing in the way.

Live site: **https://keshavkrishnan.vercel.app**

```
/                  index.html             intro and portrait, interests, contact
/entrepreneurship  entrepreneurship.html  Kilra, CropConnect, VolunteerU
/research          research.html          papers, patent
/projects          projects.html          FIREWATCH, CROSSING, GridWatch, skills
/school            school.html            VEX Robotics, Mock Trial
/work              work.html              EP Industrial Coatings, McDonald's
                   site.css               tab bar, column, type, colors
                   vercel.json            clean URLs: /work serves work.html, /awards redirects
```

Say it once, plainly.

## The core idea

1. **One column, one voice.** Every page sits in a centered 580 px column on a warm off-white
   (`#f1efe9`) with near-black text (`#14130f`) and a warm gray (`#6b675e`) for labels and inactive
   tabs. Type is Helvetica Neue, 15 px at a 1.6 line height on the inner pages.
2. **Organized by what a reader asks.** Companies, research, projects, school, and jobs each
   get their own tab, so nothing is buried under anything else.
3. **Nothing to build.** Static HTML and one stylesheet. The inner pages come from one generator so
   the tab bar and spacing never drift, Vercel serves `/work` from `work.html` through `cleanUrls`,
   and every push to `main` deploys.

## How it works

**Tab bar.** `.tabs` is 14 px links with 20 px gaps, gray until hovered, with the current page marked
by `aria-current="page"` in the text color at weight 500. It wraps to a second line on narrow phones.

**Inner pages.** `.group` spaces sections by 2.5 em and `.label` sets the small uppercase headings
(11 px, 0.08 em tracking). An `.entry` puts the name and role on the first line and indents the
description 30 px beneath it, with a smaller gray line naming the stack. List items are indented
30 px. Links are underlined at 30% opacity with a 3 px offset.

**Home.** An intro with the portrait, "What I'm interested in," and a contact section with a CV
request, email, GitHub, and LinkedIn, in the same palette and type. Blocks rise into place and the
large headings settle in word by word as they enter the viewport; readers who ask for reduced
motion get none. A Markdown button opens the whole profile as copyable plain text.

**Deploys.** The Vercel project is connected to this repository, and keshavkrishnan.vercel.app is a
project domain, so a push to `main` updates the live site. `.vercelignore` is an allowlist: only the
pages, `site.css`, `llms.txt`, `vercel.json`, and `assets/` ship.

## Run it

```bash
python3 -m http.server 8787     # then open http://localhost:8787
```

Locally, open inner pages by file name (`/work.html`); the extensionless URLs come from Vercel.
To change an inner page, edit its content in `build.py` and run `python3 build.py`.

## Layout

```
index.html              home: intro and portrait, interests, contact, motion, Markdown overlay
entrepreneurship.html   companies
research.html           papers, patent
projects.html           projects and skills
school.html             school involvement
work.html               jobs
site.css                shared styles
vercel.json             clean URLs
llms.txt                the profile as Markdown for language models
assets/                 the portrait
build.py                generates the five inner pages from one template
```

## Honesty

* There is no dark mode. Every page uses one warm light palette by design.
* The profile text is maintained by hand in the pages, the Markdown overlay, and `llms.txt`. Nothing
  keeps them in sync.
* Figures quoted on the site, such as revenue, research results, and placements, are not sourced in this
  repo. Each project's own repository is the place to check them.
