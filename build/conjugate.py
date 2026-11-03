"""Conjugate a regular thematic (-ω) verb from its principal parts, using παιδεύω's paradigms as the template.

Finite forms take recessive accent; the aorist infinitive is accented on the penult (-σαι) and the perfect
infinitive on the penult (-έναι). Vowel length follows the spelling: η, ω, diphthongs, iota-subscript vowels
and α/ι/υ with a macron or circumflex are long. Final -αι/-οι count short except in the optative.
Only consonant-initial verbs are handled (syllabic augment ἐ-), which covers every verb so far.
"""
import re
import unicodedata

ACUTE, GRAVE, CIRCUM, MACRON, BREVE, SMOOTH, ROUGH, SUBSCRIPT = (
    "́", "̀", "͂", "̄", "̆", "̓", "̔", "ͅ")
VOWELS = set("αεηιουω")
DIPHTHONGS = {"αι", "ει", "οι", "υι", "αυ", "ευ", "ηυ", "ου"}


def nfd(s):
    return unicodedata.normalize("NFD", s)


def nfc(s):
    return unicodedata.normalize("NFC", s)


def strip_accents(s):
    """Drop acute/grave/circumflex but keep breathings, macrons, breves, iota subscript."""
    return nfc("".join(c for c in nfd(s) if c not in (ACUTE, GRAVE, CIRCUM)))


def clusters(s):
    out = []
    for ch in nfd(s):
        if out and unicodedata.combining(ch):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def syllables(word):
    """Vowel nuclei as (start, end, long) cluster indices, left to right."""
    cl = clusters(word)
    base = [c[0] for c in cl]
    nuclei, i = [], 0
    while i < len(cl):
        if base[i] in VOWELS:
            if i + 1 < len(cl) and base[i] + base[i + 1] in DIPHTHONGS and "̈" not in cl[i + 1]:
                nuclei.append([i, i + 1, True])
                i += 2
                continue
            marks = cl[i][1:]
            long_ = base[i] in "ηω" or SUBSCRIPT in marks or MACRON in marks or CIRCUM in marks
            nuclei.append([i, i, long_])
        i += 1
    return cl, nuclei


def place_accent(word, final_diphthong_long=False, fixed=None):
    """Accent a word. fixed = 'penult' forces the accent onto the penult (infinitives); else recessive."""
    cl, nuc = syllables(word)
    if not nuc:
        return word
    ult = nuc[-1]
    ult_long = ult[2]
    if ult[1] > ult[0] and "".join(c[0] for c in cl[ult[0]:ult[1] + 1]) in ("αι", "οι") \
            and ult[1] == len(cl) - 1 and not final_diphthong_long:
        ult_long = False   # final -αι / -οι count short (not in the optative)
    if fixed == "penult" or len(nuc) == 2 or (len(nuc) > 2 and ult_long):
        target = nuc[-2] if len(nuc) >= 2 else ult
    elif len(nuc) >= 3:
        target = nuc[-3]
    else:
        target = ult
    mark = ACUTE
    if len(nuc) >= 2 and target is nuc[-2] and target[2] and not ult_long:
        mark = CIRCUM   # long penult before a short ultima
    # the accent sits on the second vowel of a diphthong, on the vowel itself otherwise
    j = target[1]
    c = cl[j]
    # keep breathing before the accent mark, iota subscript after it
    head, rest = c[0], c[1:]
    breath = "".join(m for m in rest if m in (SMOOTH, ROUGH))
    others = "".join(m for m in rest if m not in (SMOOTH, ROUGH))
    length = "".join(m for m in others if m in (MACRON, BREVE))
    tail = "".join(m for m in others if m not in (MACRON, BREVE))
    if mark == CIRCUM:
        length = ""   # a circumflex already says the vowel is long
    cl[j] = head + length + breath + mark + tail
    return nfc("".join(cl))


def accent_form(form, optative=False, fixed=None):
    """Accent a form that may end in movable (ν)."""
    nu = form.endswith("(ν)")
    core = form[:-3] if nu else form
    out = place_accent(strip_accents(core), final_diphthong_long=optative, fixed=fixed)
    return out + ("(ν)" if nu else "")


def stems(parts):
    """Tense stems from the first four principal parts."""
    p1, p2, p3, p4 = (strip_accents(p) for p in parts[:4])
    present = p1[:-1]                      # -ω
    future = p2[:-1]                       # -ω
    aorist_aug = p3[:-1]                   # -α
    aorist = nfc(nfd(aorist_aug)[2:]) if nfd(aorist_aug).startswith("ε" + SMOOTH) else aorist_aug
    perfect = p4[:-1]                      # -α
    return {"present": present, "future": future, "aorist": aorist, "aorist_aug": aorist_aug, "perfect": perfect}


def augment(stem):
    return "ἐ" + stem


def conjugate(parts, template, template_infs, english):
    """Build verb tables shaped like `template` (παιδεύω's) for the verb with these principal parts."""
    st = stems(parts)
    lemma = nfc(parts[0])
    tense_sign = st["future"][-1] if st["future"][-1] in "σψξ" else None
    redup = st["perfect"][:2]
    perf_sign = "κ" if st["perfect"].endswith("κ") else None
    out = []
    for v in template:
        tense, *mood = v["tense"].split()
        mood = mood[0] if mood else "indicative"
        if tense == "present":
            stem, prefix, sign = st["present"], None, None
        elif tense == "imperfect":
            stem, prefix, sign = augment(st["present"]), "ἐ", None
        elif tense == "future":
            stem, prefix, sign = st["future"], None, tense_sign
        elif tense == "aorist":
            stem, prefix, sign = (st["aorist_aug"], "ἐ", tense_sign) if mood == "indicative" else (st["aorist"], None, tense_sign)
        elif tense == "perfect":
            stem, prefix, sign = st["perfect"], redup, perf_sign
        elif tense == "pluperfect":
            stem, prefix, sign = augment(st["perfect"]), "ἐ" + redup, perf_sign
        else:
            raise ValueError(tense)
        forms = []
        for end in v["endings"]:
            alts = [stem + e.strip().lstrip("-") for e in end.split(" / ")]
            forms.append(" / ".join(accent_form(f, optative=(mood == "optative")) for f in alts))
        new = dict(v, lemma=lemma, forms=forms, prefix=prefix, sign=sign,
                   stem=re.sub(r"^\S+", nfc(stem) + "-", v["stem"], count=1))
        if v.get("trans"):
            new["trans"] = english_trans(tense, english)
        out.append(new)
    infs = []
    for tense, form, note in template_infs:
        if tense == "present":
            f = accent_form(st["present"] + "ειν")
            n = f"to {english['base']}, to be {english['ing']} (progressive/repeated aspect)"
        elif tense == "aorist":
            f = accent_form(st["aorist"] + "αι", fixed="penult")
            n = f"to {english['base']} (simple aspect)"
        else:
            f = accent_form(st["perfect"] + "έναι", fixed="penult")
            n = f"to have {english['pp']} (completed aspect); always accented on the penult"
        infs.append((tense, f, n))
    return out, infs


def english_trans(tense, e):
    b, s3, past, pp, ing = e["base"], e["s3"], e["past"], e["pp"], e["ing"]
    persons = ["I", "you (sg.)", "he/she/it", "we", "you (pl.)", "they"]
    be_now = ["am", "are", "is", "are", "are", "are"]
    be_past = ["was", "were", "was", "were", "were", "were"]
    have = ["have", "have", "has", "have", "have", "have"]
    out = []
    for i, p in enumerate(persons):
        if tense == "present":
            out.append(f"{p} {be_now[i]} {ing}, {s3 if i == 2 else b}" if i != 2 else f"{p} is {ing}, {s3}")
        elif tense == "imperfect":
            out.append(f"{p} {be_past[i]} {ing}, used to {b}")
        elif tense == "future":
            out.append(f"{p} {'shall' if i in (0, 3) else 'will'} {b}")
        elif tense == "aorist":
            out.append(f"{p} {past}")
        elif tense == "perfect":
            out.append(f"{p} {have[i]} {pp}")
        elif tense == "pluperfect":
            out.append(f"{p} had {pp}")
    return out
