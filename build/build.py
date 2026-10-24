"""Build Anki decks (.apkg), audio, and the study-app card bundle.

Usage: python3 build/build.py
Outputs:
  anki/*.apkg            one deck per week/task, plus Greek_All.apkg
  anki/media/*.mp3       audio in two voices (see tts.py)
  app/cards.json         card data for the study app
"""
import hashlib
import html
import json
import os
import re
import subprocess
import unicodedata

import genanki

from data import WEEKS, PARADIGMS, EXTRAS, ALPHABET, DIPHTHONGS, VOCAB, VERB_SLOTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANKI = os.path.join(ROOT, "anki")
MEDIA = os.path.join(ANKI, "media")
APP = os.path.join(ROOT, "app")
os.makedirs(MEDIA, exist_ok=True)
os.makedirs(APP, exist_ok=True)

GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def speakable(text):
    """Greek-only text for TTS: drop macrons/breves, Latin glosses, punctuation."""
    s = unicodedata.normalize("NFD", text)
    s = s.replace("̄", "").replace("̆", "")
    s = nfc(s)
    s = re.sub(r"\(([^)]*)\)", lambda m: m.group(1) if not re.search(r"[A-Za-z]", m.group(1)) and len(m.group(1)) <= 2 else " ", s)
    s = re.sub(r"\b(or|before|vowels|smooth|rough)\b", " ", s)
    s = re.sub(r"[A-Za-z.;:+\-—/]", " ", s)
    s = s.replace("᾿", "").replace("’", "")
    return re.sub(r"\s+", " ", s).strip(" ,")


_audio_jobs = {}   # key -> {"key", "text", "slow"}; rendered in every voice by tts.py
VOICES = ["lessac", "melina"]
ANKI_VOICE = "lessac"  # Anki cards carry one voice; the app lets you switch


def audio(text, slow=False):
    """Register text for TTS; return its voice-independent clip key, or None if there is no Greek."""
    say = speakable(text)
    if not GREEK.search(say):
        return None
    key = hashlib.sha1((say + ("|slow" if slow else "")).encode()).hexdigest()[:12]
    _audio_jobs[key] = {"key": key, "text": say, "slow": slow}
    return key


def render_audio():
    jobs = os.path.join(APP, "tts_jobs.json")
    json.dump(list(_audio_jobs.values()), open(jobs, "w"), ensure_ascii=False)
    py = os.path.join(ROOT, ".venv-tts", "bin", "python")
    subprocess.run([py, os.path.join(ROOT, "build", "tts.py"), jobs], check=True)
    os.remove(jobs)
    keep = {f"{v}_{k}.mp3" for v in VOICES for k in _audio_jobs}
    for fn in os.listdir(MEDIA):
        if fn.endswith(".mp3") and fn not in keep:
            os.remove(os.path.join(MEDIA, fn))


def g(s):
    return f'<span class="gk">{html.escape(nfc(s))}</span>'


# ---------------------------------------------------------------------------
# Card generation (one neutral format shared by Anki and the app)
# ---------------------------------------------------------------------------
cards_by_deck = {}   # deck_key -> {"meta":..., "cards":[...]}


def add_deck(key, week, kind, title, description):
    cards_by_deck[key] = {"key": key, "week": week, "kind": kind, "title": title,
                          "description": description, "cards": []}


def add(key, cid, front, back, front_audio=None, back_audio=None, tags=()):
    cards_by_deck[key]["cards"].append({
        "id": cid, "front": front, "back": back,
        "frontAudio": front_audio, "backAudio": back_audio, "tags": list(tags)})


def noun_table_html(p):
    rows = []
    for slot, form, end in zip(p["slots"], p["forms"], p["endings"]):
        rows.append(f"<tr><th>{slot}</th><td>{g(form)}</td><td class='end'>{g(end)}</td></tr>")
    return (f"<table class='para'><caption>{g(p['lemma'])} “{p['gloss']}” ({p['gender']})</caption>"
            + "".join(rows) + "</table>")


def build_noun_deck(key, nouns):
    for p in nouns:
        lem = p["lemma"]
        head = f"{g(lem)} <span class='meta'>({p['gender']}, “{p['gloss']}”)</span>"
        # production
        for slot, form, end in zip(p["slots"], p["forms"], p["endings"]):
            add(key, f"{key}-{lem}-{slot}",
                f"<div class='prompt'>{head}</div><div class='ask'>{slot}</div>",
                f"<div class='answer'>{g(form)}</div><div class='meta'>ending {g(end)} · {p['group']}</div>",
                back_audio=audio(form), tags=["produce", p["group"]])
        # parsing (one card per distinct form)
        seen = {}
        for slot, form in zip(p["slots"], p["forms"]):
            seen.setdefault(form, []).append(slot)
        for form, slots in seen.items():
            add(key, f"{key}-{lem}-parse-{form}",
                f"<div class='answer'>{g(form)}</div><div class='ask'>Parse: gender, number, case</div>",
                f"<div class='answer small'>{p['gender']} {' <i>or</i> '.join(slots)}</div>"
                f"<div class='meta'>of {g(lem)} “{p['gloss']}”</div>",
                front_audio=audio(form), tags=["parse", p["group"]])
        # recitation
        add(key, f"{key}-{lem}-recite",
            f"<div class='prompt'>Recite {head}</div><div class='ask'>singular → dual → plural · N G D A V</div>",
            noun_table_html(p) + f"<div class='meta'>{p['source']}</div>",
            back_audio=audio(", ".join(p["forms"]), slow=True), tags=["recite", p["group"]])


def build_article_deck(key, a):
    slots, gens, forms = a["slots"], a["genders"], a["forms"]
    seen = {}
    for slot, row in zip(slots, forms):
        for gen, form in zip(gens, row):
            add(key, f"{key}-{slot}-{gen}",
                f"<div class='prompt'>Definite article</div><div class='ask'>{gen} {slot}</div>",
                f"<div class='answer'>{g(form)}</div>", back_audio=audio(form), tags=["produce", "article"])
            seen.setdefault(form, []).append(f"{gen} {slot}")
    for form, labels in seen.items():
        add(key, f"{key}-parse-{form}",
            f"<div class='answer'>{g(form)}</div><div class='ask'>Parse the article: gender, number, case</div>",
            f"<div class='answer small'>{' <i>or</i> '.join(labels)}</div>",
            front_audio=audio(form), tags=["parse", "article"])
    rows = "".join(f"<tr><th>{s}</th>" + "".join(f"<td>{g(f)}</td>" for f in r) + "</tr>" for s, r in zip(slots, forms))
    table = (f"<table class='para'><caption>{g(a['lemma'])}</caption><tr><th></th>"
             + "".join(f"<th>{x}</th>" for x in gens) + "</tr>" + rows + "</table>")
    for i, gen in enumerate(gens):
        col = [r[i] for r in forms]
        add(key, f"{key}-recite-{gen}",
            f"<div class='prompt'>Recite the article: {gen}</div><div class='ask'>singular → dual → plural · N G D A</div>",
            table + f"<div class='meta'>{a['source']}</div>",
            back_audio=audio(", ".join(col), slow=True), tags=["recite", "article"])


NU_NOTE = "<br>(ν) = movable ν: added before a vowel or at a pause, often dropped before a consonant"


def build_verb_deck(key, verbs, extras):
    seen = {}
    for v in verbs:
        trans = v.get("trans") or [""] * len(VERB_SLOTS)   # subjunctive/optative: no paradigm translation
        for slot, form, end, tr in zip(VERB_SLOTS, v["forms"], v["endings"], trans):
            add(key, f"{key}-{v['tense']}-{slot}",
                f"<div class='prompt'>{g(v['lemma'])} · {v['label']}</div><div class='ask'>{slot}</div>",
                f"<div class='answer'>{g(form)}</div><div class='meta'>{f'“{tr}” · ' if tr else ''}ending {g(end)}{NU_NOTE if '(ν)' in form else ''}</div>",
                back_audio=audio(form), tags=["produce", v["tense"]])
            seen.setdefault(form, []).append((f"{slot} {v['label']}", tr))
    for form, labels in seen.items():
        translate = " — and translate" if any(t for _, t in labels) else ""
        add(key, f"{key}-parse-{form}",
            f"<div class='answer'>{g(form)}</div><div class='ask'>Parse: person, number, tense, mood, voice{translate}</div>",
            "<div class='answer small'>" + " <i>or</i><br>".join(f"{l} — “{t}”" if t else l for l, t in labels) + "</div>",
            front_audio=audio(form), tags=["parse"])
    for v in verbs:
        rows = "".join(f"<tr><th>{s}</th><td>{g(f)}</td><td class='end'>{g(e)}</td></tr>"
                       for s, f, e in zip(VERB_SLOTS, v["forms"], v["endings"]))
        add(key, f"{key}-recite-{v['tense']}",
            f"<div class='prompt'>Recite {g(v['lemma'])}: {v['label']}</div><div class='ask'>1 2 3 singular → 1 2 3 plural</div>",
            f"<table class='para'><caption>{v['label']} · stem {g(v['stem'])}</caption>{rows}</table>"
            f"<div class='meta'>{v['source']}{NU_NOTE if any('(ν)' in f for f in v['forms']) else ''}</div>",
            back_audio=audio(", ".join(v["forms"]), slow=True), tags=["recite", v["tense"]])
    for i, (prompt, ans, note) in enumerate(extras):
        add(key, f"{key}-extra-{i}", f"<div class='prompt'>{g(prompt)}</div>",
            f"<div class='answer'>{g(ans)}</div><div class='meta'>{note}</div>",
            back_audio=audio(ans), tags=["infinitive" if "infinitive" in prompt else "principal-parts"])


def build_vocab_deck(key, entries):
    for head, eng, pos, src in entries:
        a = audio(head)
        add(key, f"{key}-{head}-ge",
            f"<div class='answer'>{g(head)}</div><div class='ask'>Meaning?</div>",
            f"<div class='answer small'>{html.escape(eng)}</div><div class='meta'>{html.escape(pos)} · {src}</div>",
            front_audio=a, tags=["greek-to-english"])
        add(key, f"{key}-{head}-eg",
            f"<div class='prompt'>{html.escape(eng)}</div><div class='ask'>Greek? ({html.escape(pos)})</div>",
            f"<div class='answer'>{g(head)}</div><div class='meta'>{src}</div>",
            back_audio=a, tags=["english-to-greek"])


def build_alphabet_deck(key):
    for cap, low, name, tr, sound in ALPHABET:
        add(key, f"{key}-{name}",
            f"<div class='answer'>{g(cap + ' ' + low)}</div><div class='ask'>Name and sound?</div>",
            f"<div class='answer small'>{g(name)} · <b>{tr}</b></div><div class='meta'>{sound}</div>",
            back_audio=audio(name), tags=["letter"])
        add(key, f"{key}-{name}-rev",
            f"<div class='prompt'>Write the letter: <b>{tr}</b> — {sound}</div>",
            f"<div class='answer'>{g(cap + ' ' + low)}</div><div class='meta'>{g(name)}</div>",
            back_audio=audio(name), tags=["letter-reverse"])
    for sym, sound in DIPHTHONGS:
        a = audio(sym) if len(speakable(sym)) <= 3 else None
        add(key, f"{key}-{sym}", f"<div class='answer'>{g(sym)}</div><div class='ask'>Pronunciation?</div>",
            f"<div class='answer small'>{html.escape(sound)}</div>", back_audio=a, tags=["diphthong-mark"])


# ---------------------------------------------------------------------------
week = {w["id"]: w for w in WEEKS}

add_deck("w1-alphabet", "w1", "memorize", "Alphabet & pronunciation",
         "24 letters with names and sounds, diphthongs, breathings, accents")
build_alphabet_deck("w1-alphabet")

add_deck("w2-paradigms", "w2", "memorize", "Second declension: ὁδός, λόγος, ἄνθρωπος, ἔργον, δῶρον",
         "Mastronarde Unit 3 ¶4(a)–(b)")
build_noun_deck("w2-paradigms", PARADIGMS["w2"])
add_deck("w2-vocab", "w2", "vocab", "Vocabulary: Mastronarde Unit 3 + Mollin & Williamson Lesson 2",
         "Mastronarde Unit 3 pp. 30–31; Mollin & Williamson Lesson 2 pp. 12–13")
build_vocab_deck("w2-vocab", VOCAB["w2"])

add_deck("w3-article", "w3", "memorize", "The definite article ὁ, ἡ, τό", "Mastronarde Unit 4 ¶6")
build_article_deck("w3-article", PARADIGMS["w3"][0])

add_deck("w4-paradigms", "w4", "memorize", "First declension: 10 model nouns",
         "Mastronarde Unit 4 §2(a)–(b), Unit 6 §§1–2")
build_noun_deck("w4-paradigms", PARADIGMS["w4"])
add_deck("w4-vocab", "w4", "vocab", "Vocabulary: Hansen & Quinn Unit 1", "Hansen & Quinn p. 31")
build_vocab_deck("w4-vocab", VOCAB["w4"])

add_deck("w5-paideuo", "w5", "memorize", "παιδεύω: present, imperfect, future, aorist indicative active",
         "H&Q Unit 2 §§20–23, plus infinitives (§26) and principal parts")
build_verb_deck("w5-paideuo", PARADIGMS["w5"], EXTRAS["w5"])
add_deck("w5-vocab", "w5", "vocab", "Vocabulary: Hansen & Quinn Unit 2", "Hansen & Quinn p. 53")
build_vocab_deck("w5-vocab", VOCAB["w5"])

add_deck("w7-paideuo", "w7", "memorize", "παιδεύω: perfect, pluperfect; subjunctive and optative active",
         "H&Q Unit 3 §§28–34, plus the perfect infinitive (§30)")
build_verb_deck("w7-paideuo", PARADIGMS["w7"], EXTRAS["w7"])
add_deck("w7-vocab", "w7", "vocab", "Vocabulary: Hansen & Quinn Unit 3", "Hansen & Quinn pp. 71–73")
build_vocab_deck("w7-vocab", VOCAB["w7"])


# ---------------------------------------------------------------------------
# Review sheets: the week's tables (forms split stem | ending) and vocab lists
# ---------------------------------------------------------------------------
def clusters(s):
    out = []
    for ch in unicodedata.normalize("NFD", s):
        if out and unicodedata.combining(ch):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def split_form(form, ending):
    """(stem, ending) with the ending matched on bare letters, so accents and breathings may differ."""
    fc, ec = clusters(form), clusters(ending.lstrip("-"))
    bare = lambda cs: [c[0].lower() for c in cs]
    n = len(ec)
    if n and bare(fc[-n:]) == bare(ec):
        return nfc("".join(fc[:-n])), nfc("".join(fc[-n:]))
    return nfc(form), ""


def form_cell(form, ending=""):
    if " / " in form:   # alternative forms, e.g. παιδεύσαις / παιδεύσειας
        ends = ending.split(" / ") if ending else [""] * len(form.split(" / "))
        return {"alts": [form_cell(f, e) for f, e in zip(form.split(" / "), ends)], "audio": audio(form)}
    stem, end = split_form(form, ending) if ending else (nfc(form), "")
    return {"stem": stem, "end": end, "audio": audio(form)}


def mark_stem(c, prefix, sign):
    """Pull the augment/reduplication prefix and the tense sign out of the stem so the sheet can colour them."""
    for cell in c.get("alts", [c]):
        if prefix and cell["stem"].startswith(prefix):
            cell["aug"], cell["stem"] = prefix, cell["stem"][len(prefix):]
        if sign and cell["stem"].endswith(sign):
            cell["sign"], cell["stem"] = sign, cell["stem"][:-len(sign)]
    return c


def noun_review(nouns):
    groups = {}   # one table per ending set, so the endings column fits every word in it
    for p in nouns:
        groups.setdefault((p["group"], tuple(p["endings"])), []).append(p)
    out = []
    for (group, ends), ps in groups.items():
        # tell same-named tables apart by the first case where their endings differ
        others = [e for g, e in groups if g == group and e != ends]
        diff = next((i for i in range(len(ends)) if any(o[i] != ends[i] for o in others)), None)
        title = group if diff is None else f"{group} ({ps[0]['slots'][diff]} {ends[diff]})"
        out.append({"type": "noun", "title": title, "source": ps[0]["source"],
                    "slots": ps[0]["slots"], "endings": ps[0]["endings"],
                    "words": [{"lemma": p["lemma"], "gloss": p["gloss"], "gender": p["gender"],
                               "recite": audio(", ".join(p["forms"]), slow=True),
                               "forms": [form_cell(f, e) for f, e in zip(p["forms"], p["endings"])]} for p in ps]})
    return out


def article_review(a):
    return [{"type": "article", "title": "The definite article " + a["lemma"], "source": a["source"],
             "slots": a["slots"], "genders": a["genders"],
             "recite": [audio(", ".join(r[i] for r in a["forms"]), slow=True) for i in range(len(a["genders"]))],
             "rows": [[form_cell(f) for f in r] for r in a["forms"]]}]


def verb_review(verbs, extras, title="indicative active"):
    groups = {}   # one table per group (e.g. indicative vs. subjunctive & optative)
    for v in verbs:
        groups.setdefault(v.get("group", title), []).append(v)
    tables = []
    for group, vs in groups.items():
        tenses = []
        for v in vs:
            # Week 5 tenses imply their marks; later tables name them explicitly
            prefix = v.get("prefix", "ἐ" if v["tense"] in ("imperfect", "aorist") else None)
            sign = v.get("sign", "σ" if v["tense"] in ("future", "aorist") else None)
            cells = [mark_stem(form_cell(f, e), prefix, sign) for f, e in zip(v["forms"], v["endings"])]
            tenses.append({"tense": v["tense"], "label": v["label"], "stem": v["stem"], "source": v["source"],
                           "recite": audio(", ".join(v["forms"]), slow=True), "forms": cells, "trans": v.get("trans")})
        tables.append({"type": "verb", "title": f"{vs[0]['lemma']}: {group}", "lemma": vs[0]["lemma"],
                       "slots": VERB_SLOTS, "tenses": tenses, "extras": []})
    tables[0]["extras"] = [{"label": p, "greek": a, "note": n, "audio": audio(a)} for p, a, n in extras]
    return tables


def alphabet_review():
    return [{"type": "alphabet", "title": "Alphabet",
             "letters": [{"cap": c, "low": l, "name": n, "tr": t, "sound": snd, "audio": audio(n)}
                         for c, l, n, t, snd in ALPHABET],
             "marks": [{"sym": sym, "sound": snd} for sym, snd in DIPHTHONGS]}]


def vocab_review(entries, title):
    return {"type": "vocab", "title": title,
            "entries": [{"head": nfc(h), "eng": e, "pos": p, "src": src, "audio": audio(h)} for h, e, p, src in entries]}


REVIEW = {
    "w1": {"tables": alphabet_review(), "vocab": []},
    "w2": {"tables": noun_review(PARADIGMS["w2"]),
           "vocab": [vocab_review(VOCAB["w2"], "Mastronarde Unit 3 + Mollin & Williamson Lesson 2")]},
    "w3": {"tables": article_review(PARADIGMS["w3"][0]), "vocab": []},
    "w4": {"tables": noun_review(PARADIGMS["w4"]), "vocab": [vocab_review(VOCAB["w4"], "Hansen & Quinn Unit 1")]},
    "w5": {"tables": verb_review(PARADIGMS["w5"], EXTRAS["w5"]),
           "vocab": [vocab_review(VOCAB["w5"], "Hansen & Quinn Unit 2")]},
}
# Week 6 is review: everything from Weeks 2–5
REVIEW["w7"] = {"tables": verb_review(PARADIGMS["w7"], EXTRAS["w7"]),
                "vocab": [vocab_review(VOCAB["w7"], "Hansen & Quinn Unit 3")]}
REVIEW["w6"] = {"tables": [t for w in ("w2", "w3", "w4", "w5") for t in REVIEW[w]["tables"]],
                "vocab": [v for w in ("w2", "w4", "w5") for v in REVIEW[w]["vocab"]]}

# ---------------------------------------------------------------------------
# Anki packaging
# ---------------------------------------------------------------------------
CSS = """
.card { font-family: "Gentium Plus", "GFS Didot", "Noto Serif", "Palatino", serif; font-size: 22px;
        text-align: center; color: #1d1b16; background: #fbf8f1; padding: 12px; }
.nightMode.card, .night_mode .card { color: #ece6d8; background: #1f1d19; }
.gk { font-family: "Gentium Plus", "GFS Didot", "Noto Serif", "Palatino", serif; }
.prompt { font-size: 24px; margin-bottom: 8px; }
.ask { font-size: 16px; color: #8a6d3b; letter-spacing: .04em; text-transform: uppercase; }
.answer { font-size: 38px; margin: 10px 0; }
.answer.small { font-size: 24px; }
.meta { font-size: 15px; color: #777; margin-top: 6px; }
table.para { margin: 8px auto; border-collapse: collapse; font-size: 22px; }
table.para caption { font-size: 18px; padding-bottom: 6px; }
table.para th { font-weight: normal; font-style: italic; color: #8a6d3b; text-align: right; padding: 2px 14px 2px 0; font-size: 16px; }
table.para td { padding: 2px 10px; text-align: left; }
table.para td.end { color: #888; }
"""

MODEL = genanki.Model(
    1607392319, "Ancient Greek card",
    fields=[{"name": "Key"}, {"name": "Front"}, {"name": "Back"}, {"name": "FrontAudio"}, {"name": "BackAudio"}],
    templates=[{
        "name": "Card",
        "qfmt": "{{Front}}<div class='audio'>{{FrontAudio}}</div>",
        "afmt": "{{Front}}<div class='audio'>{{FrontAudio}}</div><hr id=answer>{{Back}}<div class='audio'>{{BackAudio}}</div>",
    }],
    css=CSS, sort_field_index=0)


def stable_id(s):
    return int(hashlib.sha1(s.encode()).hexdigest()[:10], 16)


class Note(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def anki_file(key):
    return f"{ANKI_VOICE}_{key}.mp3"


def sound(key):
    return f"[sound:{anki_file(key)}]" if key else ""




render_audio()
all_decks, all_media = [], set()
for key, d in cards_by_deck.items():
    w = week[d["week"]]
    kind = "Memorize" if d["kind"] == "memorize" else "Vocab"
    name = f"Ancient Greek::Week {w['num']}::{kind} — {d['title']}"
    deck = genanki.Deck(stable_id(name), name, description=d["description"])
    media = set()
    for c in d["cards"]:
        deck.add_note(Note(model=MODEL, fields=[c["id"], c["front"], c["back"], sound(c["frontAudio"]), sound(c["backAudio"])],
                           tags=[t.replace(" ", "_").replace(".", "") for t in c["tags"]] + [f"week{w['num']}"]))
        media.update(anki_file(x) for x in (c["frontAudio"], c["backAudio"]) if x)
    fn = f"Greek_W{w['num']}_{kind}.apkg"
    genanki.Package(deck, media_files=[os.path.join(MEDIA, m) for m in sorted(media)]).write_to_file(os.path.join(ANKI, fn))
    d["apkg"] = fn
    d["ankiName"] = name
    all_decks.append(deck)
    all_media |= media
    print(f"{fn}: {len(d['cards'])} cards, {len(media)} audio")

genanki.Package(all_decks, media_files=[os.path.join(MEDIA, m) for m in sorted(all_media)]).write_to_file(
    os.path.join(ANKI, "Greek_All_Weeks.apkg"))

json.dump({"weeks": WEEKS, "decks": list(cards_by_deck.values()), "review": REVIEW, "voices": VOICES},
          open(os.path.join(APP, "cards.json"), "w"), ensure_ascii=False, indent=1)
print("total cards", sum(len(d["cards"]) for d in cards_by_deck.values()), "audio files", len(all_media))
