"""Generate the inner pages of keshavkrishnan.vercel.app from one template so every page shares the tab bar.

Edit the content below, then run `python3 build.py`. The home page (index.html) is written by hand."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent
ICON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgcng9IjI0IiBmaWxsPSIjMWQxZDFmIi8+PGcgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxsaW5lIHgxPSIzNCIgeTE9IjI3IiB4Mj0iMzQiIHkyPSI3MyIvPjxsaW5lIHgxPSIzOCIgeTE9IjUxIiB4Mj0iNjkiIHkyPSIyNyIvPjxsaW5lIHgxPSIzOCIgeTE9IjUxIiB4Mj0iNjkiIHkyPSI3MyIvPjwvZz48L3N2Zz4K"
TABS = [("/", "Home"), ("/entrepreneurship", "Entrepreneurship"), ("/research", "Research"), ("/projects", "Projects"),
        ("/school", "School"), ("/work", "Work")]


def nav(current):
    links = "\n".join(
        f'    <a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in TABS)
    return f'  <nav class="tabs">\n{links}\n  </nav>'


def link(href, text):
    return f'<a class="u" href="{href}" target="_blank" rel="noopener">{text}</a>'


def entry(name, role, desc, links=(), stack=None):
    tail = ""
    if stack:
        tail += f'\n          <span class="meta">{stack}</span>'
    if links:
        tail += '\n          <span class="links">' + "".join(link(h, t) for h, t in links) + "</span>"
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
              "A digital health app that learns how your body reacts to what you do and shows the real triggers behind how you feel. "
              "I built and lead it end to end, from the iOS app to the custom ML models that find each person&#8217;s triggers.",
              [("https://apps.apple.com/us/app/kilra-symptom-tracker/id6760767331", "App Store"),
               ("https://github.com/keshavkrishnan08/Kilra", "GitHub")],
              stack="Swift, SwiftUI, SwiftData, HealthKit, CloudKit, Core ML, scikit-learn"),
        entry("CropConnect", "Founder",
              "Done-for-you local produce sourcing for restaurants. We find the farms and run delivery, so kitchens can serve local food and charge more for it. "
              "I built the site and the platform behind it.",
              [("https://cropconnect.dev", "cropconnect.dev")],
              stack="Next.js, React, TypeScript, Tailwind CSS, Supabase (Postgres, auth), Stripe, Leaflet, Vercel"),
        entry("VolunteerU", "Cofounder",
              "A free platform that helps people start and run a nonprofit, and helps volunteers find work that fits them. "
              "Applications, rosters, attendance, and verified hours live in one shared workspace.",
              [("https://volunteeruapp.com", "volunteeruapp.com")],
              stack="Next.js, React, Supabase (Postgres, auth), PostHog"),
    ]),
])

page("research", "Research", "Keshav Krishnan's research: safe battery fast charging (IEEE IECON 2026), a published George Mason paper on the grid carbon of AI and crypto loads, and a crop waste forecasting patent.", [
    group("Completed", [
        entry("Safe Fast Charging Robust to Battery Aging", "1st Author",
              "A lightweight safety layer that keeps lithium-ion fast charging within safe limits as the battery ages. "
              "Instead of solving an optimization at every step, it runs a short, fixed bisection on a reduced-order electro-thermal cell model, "
              "tested against a full physics simulation of aged cells. Accepted at IEEE IECON 2026.",
              [("https://github.com/keshavkrishnan08/safe-charge", "GitHub")],
              stack="Python, NumPy, PyBaMM (Doyle-Fuller-Newman model), OSQP and PPO-Lagrangian baselines"),
        entry("The Carbon Effect of Flexible Computing Loads", "1st Author, Project Coordinator",
              "When AI data centers and crypto miners can turn their power use up and down, do they make the grid cleaner or dirtier? "
              "A game-theoretic model of dispatch, investment, and contracts that holds for any demand distribution, checked against U.S. grid data from the EIA. "
              "The answer: dirtier, unless the load runs on surplus renewable power. "
              "Published in the Journal of Student-Scientists&#8217; Research at George Mason University, from ASSIP under Dr. Jiasun Li.",
              [("https://journals.gmu.edu/jssr/article/view/5665", "Paper"), ("https://doi.org/10.13021/jssr2026.5665", "DOI"),
               ("https://github.com/keshavkrishnan08/flexible-load-carbon", "Code"),
               ("https://github.com/keshavkrishnan08/bitcoin-mining-emissions", "Screening analysis")],
              stack="Python, NumPy, SciPy, pandas, statsmodels, matplotlib"),
    ]),
    group("Patents", [
        entry("Crop Waste Forecasting", "Inventor",
              "A graph neural network that predicts which harvests will go to waste by following price shocks through the U.S. supply chain. "
              "Price drops spread along a commodity graph and price rises along a geographic one, and a small neural network turns both into a forecast for each county. "
              "Filed as a U.S. provisional patent.",
              [("https://github.com/keshavkrishnan08/CasCrop", "GitHub")],
              stack="PyTorch, PyTorch Geometric, scikit-learn, XGBoost, statsmodels, GeoPandas, Google Earth Engine"),
    ]),
])

page("projects", "Projects", "Keshav Krishnan's projects: ECHO, FIREWATCH, CROSSING, and GridWatch.", [
    group("Selected projects", [
        entry("ECHO", "Wi-Fi sensing",
              "Finds people with Wi-Fi, no cameras. It turns the radio signals between ordinary Wi-Fi devices into a live 3D picture of where people are, "
              "and marks space no signal reaches as unknown instead of empty. "
              "A channel simulator feeds a signal pipeline, Bayesian radio tomography reconstructs where people are in 3D, and a Hungarian and Kalman tracker follows each one; "
              "a Python port matches the TypeScript engine bit for bit.",
              [("https://github.com/keshavkrishnan08/ECHOSPACE", "GitHub")],
              stack="TypeScript, Next.js, React Three Fiber, Web Workers, Python, FastAPI, C++20, Bayesian tomography, Kalman filters, Hungarian algorithm"),
        entry("FIREWATCH", "wildfire tracking",
              "Combines camera, satellite, weather, and terrain data into a forecast of where a wildfire will spread, and turns it into evacuation decisions a person approves. "
              "Smoke detection feeds an ensemble of physics-based spread runs, a particle filter reweights them as new observations arrive, and a learned surrogate makes the forecast fast.",
              [("https://keshavkrishnan08.github.io/firewatch/", "Live site"), ("https://github.com/keshavkrishnan08/firewatch", "GitHub")],
              stack="Python, PyTorch, YOLO, RT-DETR, SAM 2, U-Net, OpenCV, Shapely, DuckDB, FastAPI, GOES-18 and HRRR data, React, TypeScript, deck.gl, MapLibre"),
        entry("CROSSING", "pedestrian safety",
              "Watches ordinary street video and predicts which pedestrians a vehicle is about to hit, before anyone steps into the road. "
              "It detects and tracks every person and car, maps them onto the road in meters, and a recurrent network I wrote from scratch in NumPy estimates who is about to cross.",
              [("https://crossing-pi.vercel.app", "Live site"), ("https://github.com/keshavkrishnan08/ProjectCROSSING", "GitHub")],
              stack="Python, YOLOv3 (ONNX Runtime), OpenCV, ByteTrack, Kalman filters, homography, NumPy GRU, scikit-learn, FastAPI"),
        entry("GridWatch", "data centers and the power grid",
              "An interactive map of every data center planned or running in Indiana, set against the power grid, with each figure linked to its public filing. "
              "A Python pipeline gathers the data from OpenStreetMap and public records, and a static TypeScript map adds a build-out timeline and a household bill calculator.",
              [("https://gridwatch-indiana.vercel.app", "Live map"), ("https://github.com/keshavkrishnan08/GridWatch", "GitHub")],
              stack="TypeScript, Vite, MapLibre GL, D3, Python, Overpass API, Vitest, Playwright"),
    ]),
    '    <section class="group">\n      <p class="label">Familiar with</p>\n      <ul>\n'
    '        <li>Languages: Python, C++, Java, TypeScript, Swift, SQL</li>\n'
    '        <li>Machine learning: PyTorch, PyTorch Geometric, scikit-learn, XGBoost, NumPy, SciPy, pandas, statsmodels</li>\n'
    '        <li>Computer vision: YOLO, SAM 2, CLIP, OpenCV, ONNX Runtime</li>\n'
    '        <li>Estimation: Kalman and particle filters, data assimilation, Monte Carlo localization</li>\n'
    '        <li>Apps: Next.js, React, FastAPI, Flask, Supabase, SwiftUI</li>\n'
    '        <li>Applied AI: agentic systems, LLM applications, retrieval, fine-tuning, prompt engineering</li>\n'
    '      </ul>\n    </section>',
])

page("school", "School", "Keshav Krishnan's school involvement at Park Tudor: VEX Robotics and Mock Trial.", [
    group("Park Tudor School", [
        entry("VEX Robotics", "Captain, Programmer, Strategy Design",
              "Captained Team 6842V Vicious Vortex to international placements and the most wins in the world across the 2024 and 2025 seasons. "
              "I wrote the robot&#8217;s autonomy: it works out where it is on the field, follows smooth curved paths, and finds game objects with its vision sensor. "
              "Also mentored the middle school team to a state title.",
              stack="C++, Monte Carlo localization, pure pursuit over B&#233;zier curves, vision sensing"),
        entry("Mock Trial", "Cofounder &amp; President",
              "Cofounded the school&#8217;s mock trial program and built it from the ground up, then took the team to districts, where I won an Outstanding Witness award. "
              "Also organized the school&#8217;s first bipartisan roundtable, bringing state and national officials to speak with students."),
    ]),
])

page("work", "Work", "Keshav Krishnan's work experience: EP Industrial Coatings and McDonald's.", [
    group("Experience", [
        entry("EP Industrial Coatings", "Operations &amp; Engineering Intern",
              "Built a computer vision tool that turns photos of equipment into coating quotes, and wrote the company&#8217;s standard operating procedures. "
              "The tool embeds each photo with CLIP, finds the most similar past coating jobs, and drafts a priced estimate from them. "
              "I later moved the model to ONNX Runtime with 8-bit weights so the live demo runs on a small server.",
              [("https://enviropeel-project.onrender.com", "Live demo"), ("https://github.com/keshavkrishnan08/Enviropeel-Project", "GitHub")],
              stack="Python, Flask, SQLAlchemy, CLIP, ONNX Runtime, NumPy, Pillow, PyTorch"),
        entry("McDonald&#8217;s", "Crew Member",
              "Part of the restaurant crew, serving customers and keeping orders moving."),
    ]),
])
print("pages written")
