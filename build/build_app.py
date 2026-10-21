"""Bundle app/cards.json + anki/media into the study app (cards, review sheets, audio in each voice).

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



def clip_keys(x):
    """Every audio key referenced by cards and review sheets."""
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ("frontAudio", "backAudio", "audio", "recite") and isinstance(v, str):
                yield v
            elif k == "recite" and isinstance(v, list):
                yield from (r for r in v if r)
            else:
                yield from clip_keys(v)
    elif isinstance(x, list):
        for v in x:
            yield from clip_keys(v)


MEDIA = os.path.join(ROOT, "anki", "media")
used = sorted(set(clip_keys(data)))
voices = data["voices"]
# The Claude artifact can't serve loose files, so it embeds every clip; the other builds link to mp3 files.
embedded = {v: {k: base64.b64encode(open(os.path.join(MEDIA, f"{v}_{k}.mp3"), "rb").read()).decode() for k in used}
            for v in voices}


def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


tpl = open(os.path.join(ROOT, "build", "app_template.html")).read()
page = tpl.replace("__DATA__", js(private)).replace(
    "__SUBTITLE__", COURSE_SUBTITLE or "Ancient Greek paradigms and vocabulary")
public_page = tpl.replace("__DATA__", js(data)).replace("__SUBTITLE__", "Ancient Greek paradigms and vocabulary")


def with_audio(p, base):
    return p.replace("__AUDIO__", "{}" if base else js(embedded)).replace("__AUDIOBASE__", base)


def standalone(body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
            + body + "</body></html>")


artifact = with_audio(page, "").replace("__DECKBASE__", "")
open(os.path.join(ROOT, "app", "artifact.html"), "w").write(artifact)
open(os.path.join(ROOT, "app", "index.html"), "w").write(
    standalone(with_audio(page, "../anki/media/").replace("__DECKBASE__", "../anki/")))

# GitHub Pages site: docs/index.html with the .apkg files beside it
site = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(site, "anki"), exist_ok=True)
open(os.path.join(site, "index.html"), "w").write(
    standalone(with_audio(public_page, "audio/").replace("__DECKBASE__", "anki/")))
shutil.rmtree(os.path.join(site, "audio"), ignore_errors=True)
os.makedirs(os.path.join(site, "audio"))
for v in voices:
    for k in used:
        shutil.copyfile(os.path.join(MEDIA, f"{v}_{k}.mp3"), os.path.join(site, "audio", f"{v}_{k}.mp3"))
open(os.path.join(site, ".nojekyll"), "w").close()
for fn in os.listdir(os.path.join(ROOT, "anki")):
    if fn.endswith(".apkg"):
        shutil.copyfile(os.path.join(ROOT, "anki", fn), os.path.join(site, "anki", fn))

print("artifact bytes", len(artifact.encode()), "clips per voice", len(used), "voices", voices)
