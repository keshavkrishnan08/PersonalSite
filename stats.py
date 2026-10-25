"""Snapshot GitHub stats for the Projects page into stats.json.

Counts public repositories, Keshav's commits on each repository's default branch, and the
language mix across them. Needs an authenticated `gh` CLI and git. Run it, then `python3 build.py`;
the page shows the snapshot date, so the numbers never pose as live.
"""
import datetime
import json
import pathlib
import subprocess
import tempfile

OWNER = "keshavkrishnan08"
AUTHOR_NAMES = {"Keshav Krishnan", "keshavkrishnan08"}   # every identity Keshav has committed under
NOT_CODE = {"HTML", "CSS", "SCSS", "Jupyter Notebook", "TeX", "Makefile", "Dockerfile", "Shell",
            "Procfile", "Batchfile", "PowerShell", "Mako", "Jinja", "MDX"}
ROOT = pathlib.Path(__file__).resolve().parent


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def main():
    repos = json.loads(gh("repo", "list", OWNER, "--visibility", "public", "--limit", "200",
                          "--json", "name,isEmpty"))
    repos = [r["name"] for r in repos if not r["isEmpty"]]
    commits, languages = 0, {}
    with tempfile.TemporaryDirectory() as tmp:
        for name in repos:
            target = pathlib.Path(tmp) / f"{name}.git"
            subprocess.run(["git", "clone", "-q", "--bare", "--filter=blob:none",
                            f"https://github.com/{OWNER}/{name}.git", str(target)], check=True)
            authors = subprocess.run(["git", "-C", str(target), "log", "HEAD", "--format=%an"],
                                     check=True, capture_output=True, text=True).stdout.splitlines()
            commits += sum(a in AUTHOR_NAMES for a in authors)
            for lang, size in json.loads(gh("api", f"repos/{OWNER}/{name}/languages")).items():
                if lang not in NOT_CODE:
                    languages[lang] = languages.get(lang, 0) + size
    total = sum(languages.values()) or 1
    top = sorted(languages.items(), key=lambda kv: kv[1], reverse=True)
    stats = {
        "as_of": datetime.date.today().isoformat(),
        "public_repos": len(repos),
        "commits": commits,
        "languages": [{"name": k, "share": round(100 * v / total, 1)} for k, v in top[:8]],
        "language_count": len(languages),
    }
    (ROOT / "stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
