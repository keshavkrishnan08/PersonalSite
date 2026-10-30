"""Generate the inner pages of keshavkrishnan.vercel.app from one template so every page shares the tab bar.

Edit the content below, then run `python3 build.py`. The home page (index.html) is written by hand."""
import datetime, json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(__file__).resolve().parent
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


def github_stats():
    """The On GitHub block, from the snapshot stats.py writes. Omitted if there is no snapshot."""
    path = SRC / "stats.json"
    if not path.exists():
        return ""
    s = json.loads(path.read_text(encoding="utf-8"))
    month = datetime.date.fromisoformat(s["as_of"]).strftime("%B %Y")
    langs = [l for l in s["languages"] if l["share"] >= 5]
    mix = ", ".join(f'{l["name"]} ({round(l["share"])}%)' for l in langs[:-1])
    mix = f'{mix}, and {langs[-1]["name"]} ({round(langs[-1]["share"])}%)' if len(langs) > 1 else mix
    stat = lambda num, what: f'        <div class="stat"><span class="num">{num}</span><span class="what">{what}</span></div>'
    return ('    <section class="group">\n      <p class="label">On GitHub</p>\n      <div class="stats">\n'
            + "\n".join([stat(s["public_repos"], "public repositories"), stat(f'{s["commits"]:,}', "commits"),
                         stat(s["language_count"], "languages")])
            + f'\n      </div>\n      <p class="meta">Mostly {mix}. Counted {month}.</p>\n    </section>')


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
              "A symptom and wellness tracker for iPhone that shows the real triggers behind how you feel. I built the whole app: people log symptoms, mood, sleep, and medications, "
              "and on-device statistics test which of those actually go with their worse days, with Apple Health and weather context and a report to bring to a doctor. "
              "It is live on the App Store, rated 4.4, with about $10K in annualized revenue.",
              [("https://apps.apple.com/us/app/kilra-symptom-tracker/id6760767331", "App Store"),
               ("https://kilra.vercel.app", "Website"), ("https://github.com/keshavkrishnan08/Kilra", "GitHub")],
              stack="Swift, SwiftUI, SwiftData, HealthKit, CloudKit, StoreKit 2, on-device statistics"),
        entry("CropConnect", "Founder",
              "Done-for-you local produce sourcing for restaurants. We find and vet the farms and run delivery, so kitchens can put named local farms on the menu and charge more for it. "
              "I built the site and the operator app behind it: a margin model that prices a menu with local produce, farm ranking, and supply contracts with quality specs.",
              [("https://cropconnect.dev", "cropconnect.dev"), ("https://github.com/keshavkrishnan08/crop-connect", "GitHub")],
              stack="Next.js, React, TypeScript, Tailwind CSS, Supabase (Postgres, auth), Leaflet, Vercel"),
        entry("VolunteerU", "Cofounder",
              "A free platform that helps students start and run volunteer organizations and log hours their organizers verify. "
              "I wrote most of the app, including the organization workspace and a sync layer that never overwrites cloud data with a stale copy.",
              [("https://volunteeruapp.com", "volunteeruapp.com"), ("https://github.com/keshavkrishnan08/VolunteerU", "GitHub")],
              stack="Next.js, React, Supabase (Postgres, auth), PostHog"),
    ]),
])

page("research", "Research", "Keshav Krishnan's research: safe battery fast charging (IEEE IECON 2026), a published George Mason paper on the grid carbon of flexible computing loads, and a crop waste forecasting patent.", [
    group("Completed", [
        entry("Safe Fast Charging Robust to Battery Aging", "Sole author",
              "A safety filter that keeps lithium-ion fast charging within temperature and voltage limits as the battery ages, with no optimizer in the loop: "
              "a fixed bisection on a reduced-order cell model, in 36 lines of NumPy. In simulation it stayed within limits on all 156 aged-cell draws at a median 56 microseconds per step, "
              "where standard fast-charging protocols broke them. Accepted at IEEE IECON 2026.",
              [("https://github.com/keshavkrishnan08/safe-charge", "GitHub")],
              stack="Python, NumPy, SciPy, OSQP baseline"),
        entry("The Carbon Effect of Flexible Computing Loads", "1st Author, Project Coordinator",
              "When do AI data centers and crypto miners, loads that can switch off at will, raise a grid&#8217;s carbon emissions? I led the carbon theory and the optimal contract "
              "and integrated our four-person team&#8217;s work. The answer: a large flexible load raises emissions unless it runs only on renewable power that would otherwise be wasted. "
              "Published in the Journal of Student-Scientists&#8217; Research at George Mason University, from ASSIP under Dr. Jiasun Li.",
              [("https://journals.gmu.edu/jssr/article/view/5665", "Paper"), ("https://doi.org/10.13021/jssr2026.5665", "DOI"),
               ("https://github.com/keshavkrishnan08/flexible-load-carbon", "Code"),
               ("https://github.com/keshavkrishnan08/bitcoin-mining-emissions", "Screening analysis")],
              stack="Python, NumPy, SciPy, closed-form analysis, numerical verification"),
    ]),
    group("Patents", [
        entry("Crop Waste Forecasting", "Inventor",
              "Forecasts which corn, soybean, and wheat harvests will go to waste across 2,130 U.S. counties by following price shocks through the supply chain: "
              "price drops travel a commodity graph and price rises a geographic one. It reaches an AUC of 0.935 against 0.917 for local features alone. "
              "Filed as a U.S. provisional patent.",
              [("https://github.com/keshavkrishnan08/CasCrop", "GitHub")],
              stack="Python, PyTorch, scikit-learn, XGBoost, statsmodels, GeoPandas"),
    ]),
])

page("projects", "Projects", "Keshav Krishnan's projects: ECHO, FIREWATCH, CROSSING, GridWatch, and more, with GitHub stats.", [
    group("Selected projects", [
        entry("ECHO", "Wi-Fi sensing",
              "Finds people with Wi-Fi, no cameras. It turns the radio signals between ordinary Wi-Fi devices into a live 3D picture of where people are, "
              "and reports space no signal reaches as unknown instead of empty. I built the simulator, signal pipeline, Bayesian radio tomography, and tracker in TypeScript, "
              "with a Python port that matches it bit for bit; the results so far are on simulated data.",
              [("https://github.com/keshavkrishnan08/ECHOSPACE", "GitHub")],
              stack="TypeScript, Next.js, React Three Fiber, Web Workers, Python, FastAPI, C++20"),
        entry("FIREWATCH", "wildfire tracking",
              "Combines satellite, camera, weather, and terrain data into a forecast of where a wildfire will spread, and turns it into evacuation decisions a person approves. "
              "A physics spread ensemble is corrected by a particle filter as new observations arrive. On pre-registered replays of five real fires, it improved the perimeter forecast on all five.",
              [("https://keshavkrishnan08.github.io/firewatch/", "Live site"), ("https://github.com/keshavkrishnan08/firewatch", "GitHub")],
              stack="Python, PyTorch, OpenCV, DuckDB, FastAPI, GOES-18, HRRR, React, TypeScript, deck.gl, MapLibre"),
        entry("CROSSING", "pedestrian safety",
              "Watches ordinary street video and predicts which pedestrians a vehicle is about to hit, before anyone steps into the road. "
              "It tracks every person and car, maps them onto the road in meters, and a recurrent network I wrote from scratch in NumPy estimates who is about to cross; "
              "in simulation it flags crossing intent 2.8 seconds early.",
              [("https://crossing-pi.vercel.app", "Live site"), ("https://github.com/keshavkrishnan08/ProjectCROSSING", "GitHub")],
              stack="Python, YOLOv3, ONNX Runtime, OpenCV, Kalman filters, NumPy, scikit-learn, FastAPI"),
        entry("GridWatch", "data centers and the power grid",
              "An interactive map of every data center planned or running in Indiana, set against the power grid, with each figure linked to its public filing. "
              "It tracks 76 projects across 32 counties, about 15,000 MW at full build-out, and a Python pipeline checks every cited source for changes.",
              [("https://gridwatch-indiana.vercel.app", "Live map"), ("https://github.com/keshavkrishnan08/GridWatch", "GitHub")],
              stack="TypeScript, Vite, MapLibre GL, D3, Python, Overpass API, Vitest, Playwright"),
    ]),
    github_stats(),
    group("More projects", [
        entry("Axon", "astrology for business",
              "Turns a birth date, time, and place into a natal chart computed from planetary positions, a numerology life path, and a Chinese zodiac sign, then writes a reading from them. "
              "Accounts, payments, and email run in production.",
              [("https://axonservices.dev", "Live site"), ("https://github.com/keshavkrishnan08/AgencySite", "GitHub")],
              stack="Next.js, TypeScript, astronomy-engine, Supabase, Stripe, Resend, language models"),
        entry("Dwillo", "home maintenance app",
              "A SwiftUI app for a home&#8217;s maintenance history. Log a repair once and it works out when the task is due again, reminds you, and scores how well the house is kept up.",
              [("https://keshavkrishnan08.github.io/Dwello/", "Website"), ("https://github.com/keshavkrishnan08/Dwello", "GitHub")],
              stack="Swift, SwiftUI, CloudKit, StoreKit 2"),
        entry("Drobe", "wardrobe app site",
              "The landing site for Drobe, an iOS app that turns photos of your clothes into a digital closet and suggests what to wear each day.",
              [("https://drobe-blush.vercel.app", "Live site"), ("https://github.com/keshavkrishnan08/Drobe", "GitHub")],
              stack="Next.js, React, TypeScript, Tailwind CSS, Framer Motion"),
    ]) + '\n    <p class="more"><a class="u" href="https://github.com/keshavkrishnan08?tab=repositories" target="_blank" rel="noopener">'
         'Every public repository on GitHub</a></p>',
    '    <section class="group">\n      <p class="label">Familiar with</p>\n      <ul>\n'
    '        <li>Languages: Python, C++, Java, TypeScript, Swift, SQL</li>\n'
    '        <li>Machine learning: PyTorch, scikit-learn, XGBoost, NumPy, SciPy, pandas, statsmodels</li>\n'
    '        <li>Computer vision: YOLO, SAM 2, CLIP, OpenCV, ONNX Runtime</li>\n'
    '        <li>Estimation: Kalman and particle filters, data assimilation, Monte Carlo localization</li>\n'
    '        <li>Apps: Next.js, React, FastAPI, Flask, Supabase, SwiftUI</li>\n'
    '        <li>Applied AI: agentic systems, LLM applications, retrieval, fine-tuning, prompt engineering</li>\n'
    '      </ul>\n    </section>',
])

page("school", "School", "Keshav Krishnan's school involvement at Park Tudor: VEX Robotics, Mock Trial, DECA, and Speech and Debate.", [
    group("Park Tudor School", [
        entry("VEX Robotics", "Captain, Programmer, Strategy Design",
              "Captained Team 6842V Vicious Vortex to international placements and the most wins in the world across the 2024 and 2025 seasons. "
              "I wrote the robot&#8217;s autonomy in C++: it works out where it is on the field, follows smooth curved paths, and finds game objects with its vision sensor. "
              "Also mentored the middle school team to a state title.",
              stack="C++, Monte Carlo localization, pure pursuit over B&#233;zier curves, vision sensing"),
        entry("Mock Trial", "Cofounder &amp; President",
              "Cofounded the school&#8217;s mock trial program and built it from the ground up, then took the team to districts, where I won an Outstanding Witness award. "
              "Also organized the school&#8217;s first bipartisan roundtable, bringing state and national officials to speak with students."),
        entry("DECA", "International Career Development Conference qualifier",
              "Qualified for DECA&#8217;s International Career Development Conference, the international round of its business competitions."),
        entry("Speech and Debate", "NSDA District finalist",
              "Reached the finals at the National Speech and Debate Association district tournament."),
    ]),
])

page("work", "Work", "Keshav Krishnan's work experience: EP Industrial Coatings and McDonald's.", [
    group("Experience", [
        entry("EP Industrial Coatings", "Operations &amp; Engineering Intern",
              "Built a computer vision tool that turns a photo of a bearing, flange, or gearbox into a priced coating quote by matching it against past coating jobs, "
              "and wrote the company&#8217;s standard operating procedures. I later moved the model to ONNX Runtime with 8-bit weights so the live demo runs on a small server.",
              [("https://enviropeel-project.onrender.com", "Live demo"), ("https://github.com/keshavkrishnan08/Enviropeel-Project", "GitHub")],
              stack="Python, Flask, CLIP, ONNX Runtime, NumPy, Pillow"),
        entry("McDonald&#8217;s", "Crew Member",
              "Part of the restaurant crew, serving customers and keeping orders moving."),
    ]),
])

print("pages written")
