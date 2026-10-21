"""Bundle app/cards.json + anki/media into the study app.

Outputs:
  app/index.html             standalone page (open locally in a browser)
  app/artifact.html          same page without the document skeleton, for publishing
  docs/                      GitHub Pages site: the app plus downloadable .apkg files
"""
import base64
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "app", "cards.json")))

# Private course details (assignments, dates, notes) go only into the local and Claude builds.
try:
    sys.path.insert(0, os.path.join(ROOT, "build"))
    from course import WEEKS as COURSE_WEEKS, SUBTITLE as COURSE_SUBTITLE
except ImportError:
    COURSE_WEEKS, COURSE_SUBTITLE = [], None
private = json.loads(json.dumps(data))
extra = {w["id"]: w for w in COURSE_WEEKS}
for w in private["weeks"]:
    w.update(extra.get(w["id"], {}))

used = {c[k] for d in data["decks"] for c in d["cards"] for k in ("frontAudio", "backAudio") if c[k]}
audio = {fn: base64.b64encode(open(os.path.join(ROOT, "anki", "media", fn), "rb").read()).decode() for fn in sorted(used)}


def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


tpl = open(os.path.join(ROOT, "build", "app_template.html")).read().replace("__AUDIO__", js(audio))
page = tpl.replace("__DATA__", js(private)).replace(
    "__SUBTITLE__", COURSE_SUBTITLE or "Ancient Greek paradigms and vocabulary")
public_page = tpl.replace("__DATA__", js(data)).replace("__SUBTITLE__", "Ancient Greek paradigms and vocabulary")


def standalone(body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
            + body + "</body></html>")


open(os.path.join(ROOT, "app", "artifact.html"), "w").write(page.replace("__DECKBASE__", ""))
open(os.path.join(ROOT, "app", "index.html"), "w").write(standalone(page.replace("__DECKBASE__", "../anki/")))

# GitHub Pages site: docs/index.html with the .apkg files beside it
site = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(site, "anki"), exist_ok=True)
open(os.path.join(site, "index.html"), "w").write(standalone(public_page.replace("__DECKBASE__", "anki/")))
open(os.path.join(site, ".nojekyll"), "w").close()
for fn in os.listdir(os.path.join(ROOT, "anki")):
    if fn.endswith(".apkg"):
        shutil.copyfile(os.path.join(ROOT, "anki", fn), os.path.join(site, "anki", fn))

print("page bytes", len(page.encode()), "audio clips", len(audio))
