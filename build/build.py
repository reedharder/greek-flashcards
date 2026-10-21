"""Build Anki decks (.apkg), audio, and the study-app card bundle.

Usage: python3 build/build.py
Outputs:
  anki/*.apkg            one deck per week/task, plus Greek_All.apkg
  anki/media/*.mp3       espeak-ng "grc" (reconstructed Ancient Greek) audio
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


_audio_cache = {}


def audio(text, slow=False):
    """Render text to mp3 (cached by content); return filename or None."""
    say = speakable(text)
    if not GREEK.search(say):
        return None
    key = hashlib.sha1((say + ("|slow" if slow else "")).encode()).hexdigest()[:12]
    fn = f"grc_{key}.mp3"
    path = os.path.join(MEDIA, fn)
    if not os.path.exists(path):
        wav = path[:-4] + ".wav"
        subprocess.run(["espeak-ng", "-v", "grc", "-s", "115" if slow else "135", "-g", "6", "-w", wav, say], check=True)
        subprocess.run(["lame", "--quiet", "-V", "6", "--resample", "22.05", wav, path], check=True)
        os.remove(wav)
    _audio_cache[fn] = say
    return fn


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


def build_verb_deck(key, verbs, extras):
    seen = {}
    for v in verbs:
        for slot, form, end, tr in zip(VERB_SLOTS, v["forms"], v["endings"], v["trans"]):
            add(key, f"{key}-{v['tense']}-{slot}",
                f"<div class='prompt'>{g(v['lemma'])} · {v['label']}</div><div class='ask'>{slot}</div>",
                f"<div class='answer'>{g(form)}</div><div class='meta'>“{tr}” · ending {g(end)}</div>",
                back_audio=audio(form), tags=["produce", v["tense"]])
            seen.setdefault(form, []).append((f"{slot} {v['label']}", tr))
    for form, labels in seen.items():
        add(key, f"{key}-parse-{form}",
            f"<div class='answer'>{g(form)}</div><div class='ask'>Parse: person, number, tense, mood, voice — and translate</div>",
            "<div class='answer small'>" + " <i>or</i><br>".join(f"{l} — “{t}”" for l, t in labels) + "</div>",
            front_audio=audio(form), tags=["parse"])
    for v in verbs:
        rows = "".join(f"<tr><th>{s}</th><td>{g(f)}</td><td class='end'>{g(e)}</td></tr>"
                       for s, f, e in zip(VERB_SLOTS, v["forms"], v["endings"]))
        add(key, f"{key}-recite-{v['tense']}",
            f"<div class='prompt'>Recite {g(v['lemma'])}: {v['label']}</div><div class='ask'>1 2 3 singular → 1 2 3 plural</div>",
            f"<table class='para'><caption>{v['label']} · stem {g(v['stem'])}</caption>{rows}</table>"
            f"<div class='meta'>{v['source']}</div>",
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


def sound(fn):
    return f"[sound:{fn}]" if fn else ""


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
        media.update(x for x in (c["frontAudio"], c["backAudio"]) if x)
    fn = f"Greek_W{w['num']}_{kind}.apkg"
    genanki.Package(deck, media_files=[os.path.join(MEDIA, m) for m in sorted(media)]).write_to_file(os.path.join(ANKI, fn))
    d["apkg"] = fn
    d["ankiName"] = name
    all_decks.append(deck)
    all_media |= media
    print(f"{fn}: {len(d['cards'])} cards, {len(media)} audio")

genanki.Package(all_decks, media_files=[os.path.join(MEDIA, m) for m in sorted(all_media)]).write_to_file(
    os.path.join(ANKI, "Greek_All_Weeks.apkg"))

json.dump({"weeks": WEEKS, "decks": list(cards_by_deck.values())},
          open(os.path.join(APP, "cards.json"), "w"), ensure_ascii=False, indent=1)
print("total cards", sum(len(d["cards"]) for d in cards_by_deck.values()), "audio files", len(all_media))
