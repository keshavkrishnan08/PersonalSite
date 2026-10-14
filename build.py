"""Generate the inner pages of keshavkrishnan.vercel.app from one template so every page shares the tab bar.

Edit the content below, then run `python3 build.py`. The home page (index.html) is written by hand."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent
ICON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgcng9IjI0IiBmaWxsPSIjMWQxZDFmIi8+PGcgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxsaW5lIHgxPSIzNCIgeTE9IjI3IiB4Mj0iMzQiIHkyPSI3MyIvPjxsaW5lIHgxPSIzOCIgeTE9IjUxIiB4Mj0iNjkiIHkyPSIyNyIvPjxsaW5lIHgxPSIzOCIgeTE9IjUxIiB4Mj0iNjkiIHkyPSI3MyIvPjwvZz48L3N2Zz4K"
TABS = [("/", "Home"), ("/entrepreneurship", "Entrepreneurship"), ("/research", "Research"), ("/projects", "Projects"),
        ("/school", "School"), ("/work", "Work"), ("/awards", "Awards")]


def nav(current):
    links = "\n".join(
        f'    <a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in TABS)
    return f'  <nav class="tabs">\n{links}\n  </nav>'


def link(href, text):
    return f'<a class="u" href="{href}" target="_blank" rel="noopener">{text}</a>'


def entry(name, role, desc, links=()):
    tail = ""
    if links:
        tail = '\n          <span class="links">' + "".join(link(h, t) for h, t in links) + "</span>"
    return (f'      <div class="entry">\n        <span class="name">{name}</span>, {role}<br>\n'
            f'        <span class="desc">{desc}{tail}\n        </span>\n      </div>')


def group(label, items, spaced=True):
    cls = "label spaced" if spaced else "label"
    return f'    <section class="group">\n      <p class="{cls}">{label}</p>\n' + "\n".join(items) + "\n    </section>"


def page(slug, title, description, sections):
    url = f"https://keshavkrishnan.vercel.app/{slug}"
    body = "\n\n".join(sections)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Keshav Krishnan</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#f1efe9">
<link rel="canonical" href="{url}">
<meta property="og:type" content="profile">
<meta property="og:title" content="{title} · Keshav Krishnan">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://keshavkrishnan.vercel.app/assets/keshav.jpg">
<link rel="icon" type="image/svg+xml" href="{ICON}">
<link rel="stylesheet" href="/site.css">
</head>
<body class="doc">
<div class="wrap">
{nav('/' + slug)}
  <main>
{body}
  </main>
</div>
</body>
</html>
"""
    (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")


page("entrepreneurship", "Entrepreneurship", "Companies Keshav Krishnan founded: Kilra, CropConnect, and VolunteerU.", [
    group("Founded", [
        entry("Kilra", "Founder, CEO",
              "A digital health app that learns how your body reacts to what you do and shows the real triggers behind how you feel. I built and lead it end to end.",
              [("https://apps.apple.com/us/app/kilra-symptom-tracker/id6760767331", "App Store")]),
        entry("CropConnect", "Founder",
              "Done-for-you local produce sourcing for restaurants. We find the farms and run delivery, so kitchens can serve local food and charge more for it.",
              [("https://cropconnect.dev", "cropconnect.dev")]),
        entry("VolunteerU", "Cofounder",
              "A free platform that helps people start and run a nonprofit, and helps volunteers find work that fits them.",
              [("https://volunteeruapp.com", "volunteeruapp.com")]),
    ]),
])

page("research", "Research", "Keshav Krishnan's research: safe battery fast charging (IEEE IECON 2026), AI and crypto power use at George Mason ASSIP, and a crop waste forecasting patent.", [
    group("Papers", [
        entry("Safe Fast Charging Robust to Battery Aging", "1st Author",
              "A lightweight safety layer that keeps lithium-ion fast charging within safe limits as the battery ages. Accepted at IEEE IECON 2026.",
              [("https://github.com/keshavkrishnan08/safe-charge", "GitHub")]),
    ]),
    group("Ongoing", [
        entry("AI and Crypto Power Use", "1st Author, Project Coordinator",
              "How the power demand of AI data centers and crypto mining affects grid carbon. George Mason University ASSIP, under Dr. Jiasun Li, presented at the George Mason student conference."),
    ]),
    group("Patents", [
        entry("Crop Waste Forecasting", "Inventor",
              "A graph neural network that predicts which harvests will go to waste by following price shocks through the U.S. supply chain. Filed as a U.S. provisional patent.",
              [("https://github.com/keshavkrishnan08/CasCrop", "GitHub")]),
    ]),
])

page("projects", "Projects", "Keshav Krishnan's projects: FIREWATCH, CROSSING, and GridWatch.", [
    group("Selected projects", [
        entry("FIREWATCH", "wildfire tracking",
              "Combines camera, satellite, weather, and terrain data into a forecast of where a wildfire will spread, and turns it into evacuation decisions a person approves.",
              [("https://keshavkrishnan08.github.io/firewatch/", "Live site"), ("https://github.com/keshavkrishnan08/firewatch", "GitHub")]),
        entry("CROSSING", "pedestrian safety",
              "Watches ordinary street video and predicts which pedestrians a vehicle is about to hit, before anyone steps into the road.",
              [("https://crossing-pi.vercel.app", "Live site"), ("https://github.com/keshavkrishnan08/ProjectCROSSING", "GitHub")]),
        entry("GridWatch", "data centers and the power grid",
              "An interactive map of every data center planned or running in Indiana, set against the power grid, with each figure linked to its public filing.",
              [("https://gridwatch-indiana.vercel.app", "Live map"), ("https://github.com/keshavkrishnan08/GridWatch", "GitHub")]),
    ]),
    '    <section class="group">\n      <p class="label">Familiar with</p>\n      <ul>\n'
    '        <li>Python, C++, Java, TypeScript, Swift, SQL</li>\n'
    '        <li>PyTorch, scikit-learn, NumPy, pandas, computer vision, data assimilation</li>\n'
    '        <li>Agentic AI systems, LLM applications, retrieval, fine-tuning, prompt engineering</li>\n'
    '      </ul>\n    </section>',
])

page("school", "School", "Keshav Krishnan's school involvement at Park Tudor: VEX Robotics and Mock Trial.", [
    group("Park Tudor School", [
        entry("VEX Robotics", "Captain, Programmer, Strategy Design",
              "Led Team 6842V Vicious Vortex and built our autonomy software in C++: localization, path following, and vision. Also mentored the middle school team."),
        entry("Mock Trial", "Cofounder &amp; President",
              "Cofounded and lead the school&#8217;s mock trial program, and ran its first bipartisan roundtable with state and national officials."),
    ]),
])

page("work", "Work", "Keshav Krishnan's work experience: EP Industrial Coatings and McDonald's.", [
    group("Experience", [
        entry("EP Industrial Coatings", "Operations &amp; Engineering Intern",
              "Built a computer vision tool that turns photos of equipment into coating quotes, and wrote the company&#8217;s standard operating procedures."),
        entry("McDonald&#8217;s", "Crew Member",
              "Part of the restaurant crew, serving customers and keeping orders moving."),
    ]),
])

page("awards", "Awards", "Keshav Krishnan's awards in robotics and mock trial.", [
    group("Robotics", [
        "      <ul>\n        <li>VEX Robotics, Team 6842V: international placements and the most wins in the world across the 2024 and 2025 seasons</li>\n"
        "      </ul>",
    ], spaced=False),
    group("Mock trial", [
        "      <ul>\n        <li>Outstanding Witness award</li>\n      </ul>",
    ], spaced=False),
])
print("pages written")
