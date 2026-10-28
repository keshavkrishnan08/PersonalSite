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


FACTS = (("built", "I built"), ("challenge", "Challenge"), ("learned", "I learned"), ("results", "Results"))


def entry(name, role, desc, links=(), stack=None, **facts):
    """One project: a summary, then what I built, the hard part, what I learned, and results, each optional."""
    tail = ""
    for key, label in FACTS:
        if facts.get(key):
            tail += f'\n          <span class="fact"><span class="k">{label}</span> {facts[key]}</span>'
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


page("entrepreneurship", "Entrepreneurship", "Companies Keshav Krishnan founded and built: Kilra, CropConnect, and VolunteerU, with what he built, the hard parts, and results.", [
    group("Founded", [
        entry("Kilra", "Founder, CEO",
              "A symptom and wellness tracker for iPhone that shows the real triggers behind how you feel. People log symptoms, mood, sleep, and medications, "
              "and Kilra works out which of those actually go with their worse days.",
              [("https://apps.apple.com/us/app/kilra-symptom-tracker/id6760767331", "App Store"),
               ("https://kilra.vercel.app", "Website"), ("https://github.com/keshavkrishnan08/Kilra", "GitHub")],
              stack="Swift, SwiftUI, SwiftData, HealthKit, CloudKit, StoreKit 2, on-device statistics",
              built="The whole iOS app: 13-step onboarding, four-step symptom logging, a wellness score, on-device trigger statistics (Welch t-tests and Pearson correlations), "
                    "symptom clustering, a severity forecast, Apple Health and weather context, iCloud sync, PDF and CSV reports to bring to a doctor, and subscriptions.",
              challenge="Making patterns trustworthy from one person&#8217;s month of data. Every trigger is tested for significance before it is shown, and all of it runs on the phone, "
                        "so health data never leaves the user&#8217;s own iCloud.",
              learned="A simple statistic people can check beats an impressive model they cannot. I trained a Core ML model, but kept it out of the scoring until it can learn from real data.",
              results="Live on the App Store (version 4.1), rated 4.4 from 8 ratings, with about $10K in annualized revenue."),
        entry("CropConnect", "Founder",
              "Done-for-you local produce sourcing for restaurants. We find and vet the farms and run delivery, so a kitchen can put named local farms on the menu and charge more for it.",
              [("https://cropconnect.dev", "cropconnect.dev"), ("https://github.com/keshavkrishnan08/crop-connect", "GitHub")],
              stack="Next.js, React, TypeScript, Tailwind CSS, Supabase (Postgres, auth), Leaflet, Playwright, Vercel",
              built="The site and the operator app: a margin model that prices a menu with local produce, a menu parser, farm ranking by crop match, reliability, distance, and price, "
                    "supply contracts with quality specs and service credits, a profit recovery tool, accounts, and the meeting request flow.",
              challenge="Keeping a client-heavy app consistent: a deterministic first render so the server and browser draw the same page, "
                        "and a debounced writer that never runs two saves at once and always keeps the newest state.",
              learned="The software was the easy half. The business is supply and trust, and a chef is persuaded by a margin calculation on their own menu, not by a feature list.",
              results="Live at cropconnect.dev. Still early: the farm network is a seed list of six Indianapolis-area farms, and payments are not wired in yet."),
        entry("VolunteerU", "Cofounder",
              "A free platform where students start volunteer organizations and log hours that their organizers verify.",
              [("https://volunteeruapp.com", "volunteeruapp.com"), ("https://github.com/keshavkrishnan08/VolunteerU", "GitHub")],
              stack="Next.js, React, Supabase (Postgres, auth), PostHog",
              built="Most of the app (76 of 99 commits): the screens, the organization workspace, listings, the local store, and cloud sync. "
                    "Aryav Das added the photo card redesign, the nonprofit map, the database migrations, and security fixes.",
              challenge="Never losing a volunteer&#8217;s hours: a durable sync outbox that retries with backoff and refuses to overwrite cloud data with a stale or empty copy.",
              learned="Sharing a codebase made me write code another person can change safely, with clear states for loading, empty, and failed.",
              results="Live at volunteeruapp.com. Organization verification is still manual, and the launch to real users is next."),
    ]),
])

page("research", "Research", "Keshav Krishnan's research: safe battery fast charging (IEEE IECON 2026), a published George Mason paper on the grid carbon of flexible computing loads, and a crop waste forecasting patent.", [
    group("Completed", [
        entry("Safe Fast Charging Robust to Battery Aging", "Sole author",
              "A safety filter that keeps lithium-ion fast charging within temperature and voltage limits as the battery ages, with no optimizer in the loop and no state-of-health estimate.",
              [("https://github.com/keshavkrishnan08/safe-charge", "GitHub")],
              stack="Python, NumPy, SciPy, OSQP baseline",
              built="The 36-line safety path (a fixed 18-step bisection on a reduced-order electro-thermal cell model), the cell model, executable safety tests, "
                    "reproduction scripts, the paper, and the response to reviewers.",
              challenge="Lithium plating could not be certified: above about 82% charge, even zero current no longer clears the plating margin. "
                        "I scoped the guarantee to temperature and voltage, said so in the paper, and reported the cycle-life benefit as not found when the experiments did not show one.",
              learned="Narrowing a claim until I could prove it made the paper stronger. The reviewers&#8217; questions were about limits, and stating them up front answered most of them.",
              results="Accepted at IEEE IECON 2026. Within temperature and voltage limits on all 156 aged-cell draws, and on 100 of 100 after recalibrating to a second chemistry, "
                      "at a median 56 microseconds per step; standard fast-charging protocols broke the limits in all 40 warm conditions tested. Simulation only, no hardware yet."),
        entry("The Carbon Effect of Flexible Computing Loads", "1st Author, Project Coordinator",
              "When do AI data centers and crypto miners, loads that can switch off at will, raise a grid&#8217;s carbon emissions, and when do they lower them? "
              "A four-person ASSIP team at George Mason University under Dr. Jiasun Li.",
              [("https://journals.gmu.edu/jssr/article/view/5665", "Paper"), ("https://doi.org/10.13021/jssr2026.5665", "DOI"),
               ("https://github.com/keshavkrishnan08/flexible-load-carbon", "Code"),
               ("https://github.com/keshavkrishnan08/bitcoin-mining-emissions", "Screening analysis")],
              stack="Python, NumPy, SciPy, closed-form analysis, numerical verification",
              built="The general carbon theory and the optimal contract (every file in role1, with 11 verification suites), and the integration of all four roles "
                    "into one repository with a single reproduction script. I coordinated the team&#8217;s weekly plans.",
              challenge="My theory said carbon can fall; a teammate&#8217;s solver said it never did. Reconciling them led to the surplus-only contract. "
                        "A self-audit also caught a sign error in two theorems, and an adversarial review downgraded two claims I had overstated.",
              learned="Checking every closed form numerically, and inviting reviewers to attack the theorems, caught errors that rereading never would.",
              results="Published in the Journal of Student-Scientists&#8217; Research (2026) and presented at the George Mason student conference. "
                      "Under run-whenever-it-pays dispatch a large flexible load raises emissions; running it only on renewable power that would otherwise be wasted is carbon-optimal."),
    ]),
    group("Patents", [
        entry("Crop Waste Forecasting", "Inventor",
              "Forecasts which corn, soybean, and wheat harvests will go unharvested, county by county, by following price shocks through the U.S. supply chain.",
              [("https://github.com/keshavkrishnan08/CasCrop", "GitHub")],
              stack="Python, PyTorch, scikit-learn, XGBoost, statsmodels, GeoPandas",
              built="The whole pipeline: loaders for USDA, NOAA, FRED, and Census data (638,622 county-month rows across 2,130 counties, 2015 to 2025), "
                    "graph diffusion features in which price drops travel a commodity graph and price rises a geographic one, a small neural network, significance tests, and the patent claims.",
              challenge="Full graph neural networks took over 12 hours on a CPU and did not beat simpler inputs, so I replaced them with precomputed diffusion features and a 13,703-parameter network.",
              learned="The model is rarely the bottleneck. Getting the graph and the labels right moved the result more than any architecture did.",
              results="AUC 0.935 against 0.917 for local features alone (p &lt; 0.001), and filed as a U.S. provisional patent with 26 claims. "
                      "On a split by time, local features still win (0.910 against 0.892), which is the next problem to solve."),
    ]),
])

page("projects", "Projects", "Keshav Krishnan's projects: ECHO, FIREWATCH, CROSSING, GridWatch, and more, each with what he built, the hard part, and results, plus GitHub stats.", [
    group("Selected projects", [
        entry("ECHO", "Wi-Fi sensing",
              "Finds people with Wi-Fi, no cameras. It turns the radio signals between ordinary Wi-Fi devices into a live 3D picture of where people are, "
              "and reports space no signal reaches as unknown instead of empty.",
              [("https://github.com/keshavkrishnan08/ECHOSPACE", "GitHub")],
              stack="TypeScript, Next.js, React Three Fiber, Web Workers, Python, FastAPI, C++20",
              built="All of it: a seeded radio channel simulator, a signal pipeline (phase cleanup, Hampel filtering), Bayesian radio tomography and a ridge regression floor model, "
                    "a Hungarian and Kalman tracker, a Next.js interface with nine scenes, a Python reference engine, a FastAPI service, and a C++20 signal library.",
              challenge="Making the Python port match the TypeScript engine bit for bit meant reproducing V8&#8217;s Math.hypot and JavaScript&#8217;s rounding in Python. "
                        "Counting unobserved space as occupied collapsed accuracy to an IoU of 0.023, so unknown space is now reported as unknown.",
              learned="An estimate is only useful with its uncertainty. Marking what the system cannot see made it more trustworthy than guessing everywhere.",
              results="On 1,240 held-out frames the floor model reaches an IoU of 0.41 (precision 0.52, recall 0.66), never marks an empty room as occupied across 318 empty frames, "
                      "and tells floors apart on stairs by height. All on simulated data so far; the hardware adapters are untested."),
        entry("FIREWATCH", "wildfire tracking",
              "Combines satellite, camera, weather, and terrain data into a forecast of where a wildfire will spread, and turns it into evacuation decisions a person approves.",
              [("https://keshavkrishnan08.github.io/firewatch/", "Live site"), ("https://github.com/keshavkrishnan08/firewatch", "GitHub")],
              stack="Python, PyTorch, OpenCV, DuckDB, FastAPI, GOES-18, HRRR, React, TypeScript, deck.gl, MapLibre",
              built="Data connectors for satellite fire detections, weather models, terrain, fuels, and roads; a time-versioned DuckDB store; smoke detection and camera self-calibration; "
                    "a 60-member physics spread ensemble corrected by a particle filter; an evacuation decision layer; two PyTorch models; and the operating board.",
              challenge="On real fires the ensemble came out too confident, so I added a fast-spread tail and leave-one-out calibration. "
                        "Every query is pinned to a point in time, and a test enforces that a forecast can never see future data.",
              learned="For a responder, calibration is the product: a forecast that knows when it is unsure beats a sharper one that does not.",
              results="On pre-registered replays of five real fires, perimeter accuracy improved on all five (IoU +0.01 to +0.13), evacuation calls scored 0.88 precision and 0.82 recall, "
                      "and one warning came 186 minutes early. Calibrated coverage reached 0.86 against a 0.90 target, so the uncertainty is still slightly too narrow."),
        entry("CROSSING", "pedestrian safety",
              "Watches ordinary street video and predicts which pedestrians a vehicle is about to hit, before anyone steps into the road.",
              [("https://crossing-pi.vercel.app", "Live site"), ("https://github.com/keshavkrishnan08/ProjectCROSSING", "GitHub")],
              stack="Python, YOLOv3, ONNX Runtime, OpenCV, Kalman filters, NumPy, scikit-learn, FastAPI",
              built="Detection, a ByteTrack-style tracker with Kalman filters, a world model that maps people onto the road in meters, a recurrent network for crossing intention "
                    "written from scratch in NumPy and gradient-checked, conflict geometry, a calibrated risk score, and privacy controls (face and plate blurring, role-based access, audit logs).",
              challenge="Boxes that overlap on screen can be meters apart in depth, so distance comes from box height and position. Parked cars jitter, "
                        "so a vehicle only counts as moving after its displacement is confirmed over several frames.",
              learned="Writing a network from scratch, with its gradients checked by hand, taught me more about training than any framework had.",
              results="In simulation: near-miss AUROC 0.951 against 0.868 for a time-to-collision baseline, calibration error 0.002, and crossing intent flagged 2.8 seconds early on average. "
                      "These numbers come from the simulator; the real-video demo uses the geometric score."),
        entry("GridWatch", "data centers and the power grid",
              "An interactive map of every data center planned or running in Indiana, set against the power grid, with every figure linked to the public filing it came from.",
              [("https://gridwatch-indiana.vercel.app", "Live map"), ("https://github.com/keshavkrishnan08/GridWatch", "GitHub")],
              stack="TypeScript, Vite, MapLibre GL, D3, Python, Overpass API, Vitest, Playwright",
              built="A hand-curated dataset with a source for every number, a Python pipeline that fetches, validates links, refreshes federal energy data, and watches cited sources for changes, "
                    "and a map with a 2020 to 2035 timeline, ZIP code lookup, household bill model, comment letter generator, and CSV export.",
              challenge="Getting the numbers right. Comparing my data with an advocacy group&#8217;s tracker showed that most megawatt figures that started in trackers disagreed with the filings, "
                        "which also caught two county errors of my own. Missing figures stay null, never zero.",
              learned="Provenance is a feature: tying every figure to its filing is what lets anyone trust, and correct, a public dataset.",
              results="Tracks 76 projects across 32 counties: 15,142 MW at full build-out, about 43% of Indiana&#8217;s peak demand, mapped against 205 plants and 1,237 transmission segments, "
                      "with 103 cited sources and 84 tests."),
    ]),
    github_stats(),
    group("More projects", [
        entry("Axon", "astrology for business",
              "Turns a birth date, time, and place into a natal chart, a numerology life path, and a Chinese zodiac sign, then writes a reading from them.",
              [("https://axonservices.dev", "Live site"), ("https://github.com/keshavkrishnan08/AgencySite", "GitHub")],
              stack="Next.js, TypeScript, astronomy-engine, Supabase, Stripe, Resend, language models",
              built="An astronomy engine for planet positions, the Ascendant, and houses, historical daylight saving conversion, a 30-day timing scorer, "
                    "language model readings with a written fallback, accounts with row-level security, payments with idempotent webhooks, and scheduled email.",
              challenge="The common reference frame drifts about 0.36 degrees every 25 years, enough to put a planet in the wrong sign near a boundary, "
                        "and birth times near daylight saving changes need a two-pass conversion.",
              results="Checked against its own definitions: the Ascendant lands on the horizon within a millionth of a degree across 336 cases. Live with paid plans."),
        entry("Dwillo", "home maintenance app",
              "A SwiftUI app for a home&#8217;s maintenance history. Log a repair once and it works out when the task is due again, reminds you, and scores how well the house is kept up.",
              [("https://keshavkrishnan08.github.io/Dwello/", "Website"), ("https://github.com/keshavkrishnan08/Dwello", "GitHub")],
              stack="Swift, SwiftUI, CloudKit, StoreKit 2",
              built="Onboarding and a paywall, five tabs, a scheduler with 31 rules, a home health score from 12 weighted features, a spend forecast, iCloud sync, reminders, and subscriptions.",
              challenge="Passing App Store review, which meant an iPad layout, an end-user license link, and removing PassKit."),
        entry("Drobe", "wardrobe app site",
              "The landing site for Drobe, an iOS app that turns photos of your clothes into a digital closet and suggests what to wear each day.",
              [("https://drobe-blush.vercel.app", "Live site"), ("https://github.com/keshavkrishnan08/Drobe", "GitHub")],
              stack="Next.js, React, TypeScript, Tailwind CSS, Framer Motion",
              built="The site, an iPhone mockup component in CSS, and the privacy and support pages."),
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
              "Captained Team 6842V Vicious Vortex and wrote the robot&#8217;s autonomy.",
              stack="C++, Monte Carlo localization, pure pursuit over B&#233;zier curves, vision sensing",
              built="The autonomy code in C++: Monte Carlo localization so the robot knows where it is on the field, pure-pursuit path following over B&#233;zier curves, "
                    "and vision sensing to find game objects.",
              results="Eight international placements, more than 20 awards, and the most wins in the world across the 2024 and 2025 seasons. "
                      "I also mentored the middle school team to a state title."),
        entry("Mock Trial", "Cofounder &amp; President",
              "Cofounded the school&#8217;s mock trial program and built it from the ground up.",
              built="The program itself, and the school&#8217;s first bipartisan roundtable, which brought four state and national officials in front of an audience of more than 50.",
              results="Grew to 140 members, reached districts, and I won an Outstanding Witness award."),
        entry("DECA", "International Career Development Conference qualifier",
              "Qualified for DECA&#8217;s International Career Development Conference, the international round of its business competitions."),
        entry("Speech and Debate", "NSDA District finalist",
              "Reached the finals at the National Speech and Debate Association district tournament."),
    ]),
])

page("work", "Work", "Keshav Krishnan's work experience: EP Industrial Coatings and McDonald's.", [
    group("Experience", [
        entry("EP Industrial Coatings", "Operations &amp; Engineering Intern (paid)",
              "Built a computer vision tool that turns a photo of a bearing, flange, or gearbox into a priced coating quote, and wrote the company&#8217;s standard operating procedures.",
              [("https://enviropeel-project.onrender.com", "Live demo"), ("https://github.com/keshavkrishnan08/Enviropeel-Project", "GitHub")],
              stack="Python, Flask, CLIP, ONNX Runtime, NumPy, Pillow",
              built="The quoting tool: a CLIP matcher that finds the closest past coating jobs, rust and paint detection from pixel color, sizes from typical dimensions, "
                    "pricing equations for five part types, and a Flask app. I also wrote five company-wide SOPs over a five-month term.",
              challenge="A photo has no scale, so sizes start from typical dimensions and are adjusted by the matched jobs. Later the demo ran out of memory on its server, "
                        "so I moved CLIP to ONNX Runtime with 8-bit weights: memory fell from 1.6 GB to about 360 MB, with every catalog result unchanged.",
              learned="A model is not shipped until it runs on the hardware people actually have; profiling memory taught me more than tuning accuracy.",
              results="Quote turnaround went from about two weeks to about five minutes."),
        entry("McDonald&#8217;s", "Crew Member",
              "Part of the restaurant crew, serving customers and keeping orders moving."),
    ]),
])

print("pages written")
