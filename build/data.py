"""Card data for introductory Ancient Greek decks.

Paradigms follow Mastronarde (nouns, article) and Hansen & Quinn (παιδεύω);
vocabulary follows the textbook lists cited on each card.
"""

# ---------------------------------------------------------------------------
# Weeks: grouping and grammar topic only. Assignments live in course.py (private).
# ---------------------------------------------------------------------------
WEEKS = [
    {"id": "w1", "num": 1, "label": "Week 1", "topic": "Alphabet, pronunciation, accents"},
    {"id": "w2", "num": 2, "label": "Week 2", "topic": "Second (o-) declension"},
    {"id": "w3", "num": 3, "label": "Week 3", "topic": "The definite article"},
    {"id": "w4", "num": 4, "label": "Week 4", "topic": "First (a-) declension"},
    {"id": "w5", "num": 5, "label": "Week 5", "topic": "Indicative active: present, imperfect, future, aorist"},
    {"id": "w6", "num": 6, "label": "Week 6", "topic": "Review", "reuse": ["w5-paideuo", "w5-vocab"]},
    {"id": "w7", "num": 7, "label": "Week 7",
     "topic": "Perfect and pluperfect; subjunctive and optative; purpose clauses"},
    {"id": "w8", "num": 8, "label": "Week 8", "topic": "Review: Hansen & Quinn Units 1–3",
     "reuse": ["w2-paradigms", "w3-article", "w4-paradigms", "w5-paideuo", "w7-paideuo", "w4-vocab", "w5-vocab", "w7-vocab"]},
    {"id": "w10", "num": 10, "label": "Week 10",
     "topic": "First declension concluded; adjectives of the first and second declensions; conditions"},
]

# ---------------------------------------------------------------------------
# Paradigm tables. Each table: rows of (slot label, form); endings optional.
# Slot labels follow the source table's rows.
# ---------------------------------------------------------------------------
NOUN_SLOTS = ["nom. sg.", "gen. sg.", "dat. sg.", "acc. sg.", "voc. sg.",
              "nom./acc./voc. du.", "gen./dat. du.",
              "nom./voc. pl.", "gen. pl.", "dat. pl.", "acc. pl."]


# Hansen & Quinn leave out the dual
HQ_SLOTS = ["nom. sg.", "gen. sg.", "dat. sg.", "acc. sg.", "voc. sg.",
            "nom./voc. pl.", "gen. pl.", "dat. pl.", "acc. pl."]


def noun(lemma, gloss, gender, forms, endings, source, group, slots=NOUN_SLOTS):
    assert len(forms) == len(slots) and len(endings) == len(slots), lemma
    return {"kind": "noun", "lemma": lemma, "gloss": gloss, "gender": gender,
            "slots": slots, "forms": forms, "endings": endings,
            "source": source, "group": group}


def no_dual(endings):
    return endings[:5] + endings[7:]


def adjective(lemma, gloss, genders, columns, endings, source, group):
    """columns: one list of 9 forms (HQ_SLOTS) per gender; endings likewise."""
    assert len(genders) == len(columns) == len(endings), lemma
    assert all(len(c) == 9 for c in columns + endings), lemma
    return {"kind": "adjective", "lemma": lemma, "gloss": gloss, "slots": HQ_SLOTS, "genders": genders,
            "forms": [list(r) for r in zip(*columns)], "endings": [list(r) for r in zip(*endings)],
            "source": source, "group": group}


O_MF = ["-ος", "-ου", "-ῳ", "-ον", "-ε", "-ω", "-οιν", "-οι", "-ων", "-οις", "-ους"]
O_N = ["-ον", "-ου", "-ῳ", "-ον", "-ον", "-ω", "-οιν", "-ᾰ", "-ων", "-οις", "-ᾰ"]
M3 = "Mastronarde, Unit 3, ¶4"

A_LONG = ["-ᾱ", "-ᾱς", "-ᾳ", "-ᾱν", "-ᾱ", "-ᾱ", "-αιν", "-αι", "-ῶν", "-αις", "-ᾱς"]
ETA = ["-η", "-ης", "-ῃ", "-ην", "-η", "-ᾱ", "-αιν", "-αι", "-ῶν", "-αις", "-ᾱς"]
A_SHORT = ["-ᾰ", "-ᾱς", "-ᾳ", "-ᾰν", "-ᾰ", "-ᾱ", "-αιν", "-αι", "-ῶν", "-αις", "-ᾱς"]
A_SHORT_ETA = ["-ᾰ", "-ης", "-ῃ", "-ᾰν", "-ᾰ", "-ᾱ", "-αιν", "-αι", "-ῶν", "-αις", "-ᾱς"]
MASC_A = ["-ᾱς", "-ου", "-ᾳ", "-ᾱν", "-ᾱ", "-ᾱ", "-αιν", "-αι", "-ῶν", "-αις", "-ᾱς"]
MASC_ETA = ["-ης", "-ου", "-ῃ", "-ην", "-ᾰ", "-ᾱ", "-αιν", "-αι", "-ῶν", "-αις", "-ᾱς"]
M4 = "Mastronarde, Unit 4, §2"
ADJ_M = ["-ος", "-ου", "-ῳ", "-ον", "-ε", "-οι", "-ων", "-οις", "-ους"]
ADJ_F_ETA = ["-η", "-ης", "-ῃ", "-ην", "-η", "-αι", "-ων", "-αις", "-ᾱς"]
ADJ_F_A = ["-ᾱ", "-ᾱς", "-ᾳ", "-ᾱν", "-ᾱ", "-αι", "-ων", "-αις", "-ᾱς"]
ADJ_N = ["-ον", "-ου", "-ῳ", "-ον", "-ον", "-ᾰ", "-ων", "-οις", "-ᾰ"]
HQ37, HQ38 = "Hansen & Quinn, §37", "Hansen & Quinn, §38"
M6 = "Mastronarde, Unit 6"

PARADIGMS = {
    "w2": [
        noun("ὁδός", "road", "f.",
             ["ὁδός", "ὁδοῦ", "ὁδῷ", "ὁδόν", "ὁδέ", "ὁδώ", "ὁδοῖν", "ὁδοί", "ὁδῶν", "ὁδοῖς", "ὁδούς"],
             O_MF, M3 + "(a)", "o-declension masc./fem."),
        noun("λόγος", "word", "m.",
             ["λόγος", "λόγου", "λόγῳ", "λόγον", "λόγε", "λόγω", "λόγοιν", "λόγοι", "λόγων", "λόγοις", "λόγους"],
             O_MF, M3 + "(a)", "o-declension masc./fem."),
        noun("ἄνθρωπος", "human being", "m.",
             ["ἄνθρωπος", "ἀνθρώπου", "ἀνθρώπῳ", "ἄνθρωπον", "ἄνθρωπε", "ἀνθρώπω", "ἀνθρώποιν",
              "ἄνθρωποι", "ἀνθρώπων", "ἀνθρώποις", "ἀνθρώπους"],
             O_MF, M3 + "(a)", "o-declension masc./fem."),
        noun("ἔργον", "work", "n.",
             ["ἔργον", "ἔργου", "ἔργῳ", "ἔργον", "ἔργον", "ἔργω", "ἔργοιν", "ἔργα", "ἔργων", "ἔργοις", "ἔργα"],
             O_N, M3 + "(b)", "o-declension neuter"),
        noun("δῶρον", "gift", "n.",
             ["δῶρον", "δώρου", "δώρῳ", "δῶρον", "δῶρον", "δώρω", "δώροιν", "δῶρα", "δώρων", "δώροις", "δῶρα"],
             O_N, M3 + "(b)", "o-declension neuter"),
    ],
    "w3": [
        {"kind": "article", "lemma": "ὁ, ἡ, τό", "gloss": "the (definite article)",
         "source": "Mastronarde, Unit 4, ¶6",
         "slots": ["nom. sg.", "gen. sg.", "dat. sg.", "acc. sg.", "nom./acc. du.", "gen./dat. du.",
                   "nom. pl.", "gen. pl.", "dat. pl.", "acc. pl."],
         "genders": ["masc.", "fem.", "neut."],
         "forms": [  # rows x [m, f, n]
             ["ὁ", "ἡ", "τό"], ["τοῦ", "τῆς", "τοῦ"], ["τῷ", "τῇ", "τῷ"], ["τόν", "τήν", "τό"],
             ["τώ", "τώ", "τώ"], ["τοῖν", "τοῖν", "τοῖν"],
             ["οἱ", "αἱ", "τά"], ["τῶν", "τῶν", "τῶν"], ["τοῖς", "ταῖς", "τοῖς"], ["τούς", "τάς", "τά"]],
         },
    ],
    "w4": [
        noun("θεά", "goddess", "f.",
             ["θεά", "θεᾶς", "θεᾷ", "θεάν", "θεά", "θεά", "θεαῖν", "θεαί", "θεῶν", "θεαῖς", "θεάς"],
             A_LONG, M4 + "(a), alpha subgroup (stem in ε, ι, ρ)", "1st decl. long α"),
        noun("παιδεία", "education", "f.",
             ["παιδεία", "παιδείας", "παιδείᾳ", "παιδείαν", "παιδεία", "παιδεία", "παιδείαιν",
              "παιδεῖαι", "παιδειῶν", "παιδείαις", "παιδείας"],
             A_LONG, M4 + "(a), alpha subgroup (stem in ε, ι, ρ)", "1st decl. long α"),
        noun("χώρα", "land", "f.",
             ["χώρα", "χώρας", "χώρᾳ", "χώραν", "χώρα", "χώρα", "χώραιν", "χῶραι", "χωρῶν", "χώραις", "χώρας"],
             A_LONG, M4 + "(a), alpha subgroup (stem in ε, ι, ρ)", "1st decl. long α"),
        noun("γνώμη", "opinion", "f.",
             ["γνώμη", "γνώμης", "γνώμῃ", "γνώμην", "γνώμη", "γνώμα", "γνώμαιν", "γνῶμαι", "γνωμῶν", "γνώμαις", "γνώμας"],
             ETA, M4 + "(b), eta subgroup (any other stem)", "1st decl. η"),
        noun("φυγή", "flight", "f.",
             ["φυγή", "φυγῆς", "φυγῇ", "φυγήν", "φυγή", "φυγά", "φυγαῖν", "φυγαί", "φυγῶν", "φυγαῖς", "φυγάς"],
             ETA, M4 + "(b), eta subgroup (any other stem)", "1st decl. η"),
        noun("ὑγίεια", "health", "f.",
             ["ὑγίεια", "ὑγιείας", "ὑγιείᾳ", "ὑγίειαν", "ὑγίεια", "ὑγιεία", "ὑγιείαιν",
              "ὑγίειαι", "ὑγιειῶν", "ὑγιείαις", "ὑγιείας"],
             A_SHORT, M6 + ", §1(a), short α, alpha subgroup (stem in ε, ι, ρ)", "1st decl. short α"),
        noun("πεῖρα", "trial, attempt", "f.",
             ["πεῖρα", "πείρας", "πείρᾳ", "πεῖραν", "πεῖρα", "πείρα", "πείραιν", "πεῖραι", "πειρῶν", "πείραις", "πείρας"],
             A_SHORT, M6 + ", §1(a), short α, alpha subgroup (stem in ε, ι, ρ)", "1st decl. short α"),
        noun("θάλαττα", "sea", "f.",
             ["θάλαττα", "θαλάττης", "θαλάττῃ", "θάλατταν", "θάλαττα", "θαλάττα", "θαλάτταιν",
              "θάλατται", "θαλαττῶν", "θαλάτταις", "θαλάττας"],
             A_SHORT_ETA, M6 + ", §1(b), short α, eta subgroup", "1st decl. short α"),
        noun("γλῶττα", "tongue", "f.",
             ["γλῶττα", "γλώττης", "γλώττῃ", "γλῶτταν", "γλῶττα", "γλώττα", "γλώτταιν",
              "γλῶτται", "γλωττῶν", "γλώτταις", "γλώττας"],
             A_SHORT_ETA, M6 + ", §1(b), short α, eta subgroup", "1st decl. short α"),
        noun("νεανίας", "young man", "m.",
             ["νεανίας", "νεανίου", "νεανίᾳ", "νεανίαν", "νεανία", "νεανία", "νεανίαιν",
              "νεανίαι", "νεανιῶν", "νεανίαις", "νεανίας"],
             MASC_A, M6 + ", §2(a), masculine", "1st decl. masculine"),
        noun("στρατιώτης", "soldier", "m.",
             ["στρατιώτης", "στρατιώτου", "στρατιώτῃ", "στρατιώτην", "στρατιῶτα", "στρατιώτα", "στρατιώταιν",
              "στρατιῶται", "στρατιωτῶν", "στρατιώταις", "στρατιώτας"],
             MASC_ETA, M6 + ", §2(b), masculine", "1st decl. masculine"),
        noun("κριτής", "judge", "m.",
             ["κριτής", "κριτοῦ", "κριτῇ", "κριτήν", "κριτά", "κριτά", "κριταῖν", "κριταί", "κριτῶν", "κριταῖς", "κριτάς"],
             MASC_ETA, M6 + ", §2(b), masculine", "1st decl. masculine"),
    ],
    "w5": [
        {"kind": "verb", "lemma": "παιδεύω", "tense": "present", "label": "present indicative active",
         "source": "Hansen & Quinn, §20", "stem": "παιδευ- (from Principal Part I)",
         "forms": ["παιδεύω", "παιδεύεις", "παιδεύει", "παιδεύομεν", "παιδεύετε", "παιδεύουσι(ν)"],
         "endings": ["-ω", "-εις", "-ει", "-ομεν", "-ετε", "-ουσι(ν)"],
         "trans": ["I am educating, I educate", "you (sg.) are educating, you educate",
                   "he/she/it is educating, educates", "we are educating, we educate",
                   "you (pl.) are educating, you educate", "they are educating, they educate"]},
        {"kind": "verb", "lemma": "παιδεύω", "tense": "imperfect", "label": "imperfect indicative active",
         "source": "Hansen & Quinn, §21", "stem": "ἐπαιδευ- (augment + present stem)",
         "forms": ["ἐπαίδευον", "ἐπαίδευες", "ἐπαίδευε(ν)", "ἐπαιδεύομεν", "ἐπαιδεύετε", "ἐπαίδευον"],
         "endings": ["-ον", "-ες", "-ε(ν)", "-ομεν", "-ετε", "-ον"],
         "trans": ["I was educating, used to educate", "you (sg.) were educating, used to educate",
                   "he/she/it was educating, used to educate", "we were educating, used to educate",
                   "you (pl.) were educating, used to educate", "they were educating, used to educate"]},
        {"kind": "verb", "lemma": "παιδεύω", "tense": "future", "label": "future indicative active",
         "source": "Hansen & Quinn, §22", "stem": "παιδευσ- (from Principal Part II)",
         "forms": ["παιδεύσω", "παιδεύσεις", "παιδεύσει", "παιδεύσομεν", "παιδεύσετε", "παιδεύσουσι(ν)"],
         "endings": ["-ω", "-εις", "-ει", "-ομεν", "-ετε", "-ουσι(ν)"],
         "trans": ["I shall educate / be educating", "you (sg.) will educate", "he/she/it will educate",
                   "we shall educate", "you (pl.) will educate", "they will educate"]},
        {"kind": "verb", "lemma": "παιδεύω", "tense": "aorist", "label": "aorist indicative active",
         "source": "Hansen & Quinn, §23", "stem": "ἐπαιδευσ- (from Principal Part III)",
         "forms": ["ἐπαίδευσα", "ἐπαίδευσας", "ἐπαίδευσε(ν)", "ἐπαιδεύσαμεν", "ἐπαιδεύσατε", "ἐπαίδευσαν"],
         "endings": ["-α", "-ας", "-ε(ν)", "-αμεν", "-ατε", "-αν"],
         "trans": ["I educated", "you (sg.) educated", "he/she/it educated",
                   "we educated", "you (pl.) educated", "they educated"]},
    ],
}
# Week 7: Hansen & Quinn Unit 3. "prefix"/"sign" name what the review sheet marks inside the stem
# (augment, reduplication; tense sign). Alternative forms are separated by " / ".
# Subjunctives and optatives have no "trans": H&Q gives no paradigm translation (§31).
PARADIGMS["w7"] = [
    {"kind": "verb", "lemma": "παιδεύω", "tense": "perfect", "label": "perfect indicative active", "group": "indicative",
     "source": "Hansen & Quinn, §28", "stem": "πεπαιδευκ- (from Principal Part IV)", "prefix": "πε", "sign": "κ",
     "forms": ["πεπαίδευκα", "πεπαίδευκας", "πεπαίδευκε(ν)", "πεπαιδεύκαμεν", "πεπαιδεύκατε", "πεπαιδεύκᾱσι(ν)"],
     "endings": ["-α", "-ας", "-ε(ν)", "-αμεν", "-ατε", "-ᾱσι(ν)"],
     "trans": ["I have educated", "you (sg.) have educated", "he/she/it has educated",
               "we have educated", "you (pl.) have educated", "they have educated"]},
    {"kind": "verb", "lemma": "παιδεύω", "tense": "pluperfect", "label": "pluperfect indicative active", "group": "indicative",
     "source": "Hansen & Quinn, §29", "stem": "ἐπεπαιδευκ- (augment + perfect active stem)", "prefix": "ἐπε", "sign": "κ",
     "forms": ["ἐπεπαιδεύκη", "ἐπεπαιδεύκης", "ἐπεπαιδεύκει(ν)", "ἐπεπαιδεύκεμεν", "ἐπεπαιδεύκετε", "ἐπεπαιδεύκεσαν"],
     "endings": ["-η", "-ης", "-ει(ν)", "-εμεν", "-ετε", "-εσαν"],
     "trans": ["I had educated", "you (sg.) had educated", "he/she/it had educated",
               "we had educated", "you (pl.) had educated", "they had educated"]},
    {"kind": "verb", "lemma": "παιδεύω", "tense": "present subjunctive", "label": "present subjunctive active",
     "group": "subjunctive & optative", "source": "Hansen & Quinn, §31", "stem": "παιδευ- (present tense stem)",
     "forms": ["παιδεύω", "παιδεύῃς", "παιδεύῃ", "παιδεύωμεν", "παιδεύητε", "παιδεύωσι(ν)"],
     "endings": ["-ω", "-ῃς", "-ῃ", "-ωμεν", "-ητε", "-ωσι(ν)"]},
    {"kind": "verb", "lemma": "παιδεύω", "tense": "aorist subjunctive", "label": "aorist subjunctive active",
     "group": "subjunctive & optative", "source": "Hansen & Quinn, §32", "stem": "παιδευσ- (unaugmented aorist stem)", "sign": "σ",
     "forms": ["παιδεύσω", "παιδεύσῃς", "παιδεύσῃ", "παιδεύσωμεν", "παιδεύσητε", "παιδεύσωσι(ν)"],
     "endings": ["-ω", "-ῃς", "-ῃ", "-ωμεν", "-ητε", "-ωσι(ν)"]},
    {"kind": "verb", "lemma": "παιδεύω", "tense": "present optative", "label": "present optative active",
     "group": "subjunctive & optative", "source": "Hansen & Quinn, §33", "stem": "παιδευ- (present tense stem)",
     "forms": ["παιδεύοιμι", "παιδεύοις", "παιδεύοι", "παιδεύοιμεν", "παιδεύοιτε", "παιδεύοιεν"],
     "endings": ["-οιμι", "-οις", "-οι", "-οιμεν", "-οιτε", "-οιεν"]},
    {"kind": "verb", "lemma": "παιδεύω", "tense": "aorist optative", "label": "aorist optative active",
     "group": "subjunctive & optative", "source": "Hansen & Quinn, §34", "stem": "παιδευσ- (unaugmented aorist stem)", "sign": "σ",
     "forms": ["παιδεύσαιμι", "παιδεύσαις / παιδεύσειας", "παιδεύσαι / παιδεύσειε(ν)", "παιδεύσαιμεν", "παιδεύσαιτε",
               "παιδεύσαιεν / παιδεύσειαν"],
     "endings": ["-αιμι", "-αις / -ειας", "-αι / -ειε(ν)", "-αιμεν", "-αιτε", "-αιεν / -ειαν"]},
]

PARADIGMS["w10"] = [
        noun("θάλαττα", "sea", "f.",
             ["θάλαττα", "θαλάττης", "θαλάττῃ", "θάλατταν", "θάλαττα", "θάλατται", "θαλαττῶν", "θαλάτταις", "θαλάττας"],
             no_dual(A_SHORT_ETA), HQ37 + ".1, short α (other stems)", "1st decl. short α", HQ_SLOTS),
        noun("μοῦσα", "muse", "f.",
             ["μοῦσα", "μούσης", "μούσῃ", "μοῦσαν", "μοῦσα", "μοῦσαι", "μουσῶν", "μούσαις", "μούσας"],
             no_dual(A_SHORT_ETA), HQ37 + ".1, short α (other stems)", "1st decl. short α", HQ_SLOTS),
        noun("γέφυρα", "bridge", "f.",
             ["γέφυρα", "γεφύρας", "γεφύρᾳ", "γέφυραν", "γέφυρα", "γέφυραι", "γεφυρῶν", "γεφύραις", "γεφύρας"],
             no_dual(A_SHORT), HQ37 + ".1, short α (stem in ε, ι, ρ)", "1st decl. short α", HQ_SLOTS),
        noun("μοῖρα", "fate", "f.",
             ["μοῖρα", "μοίρας", "μοίρᾳ", "μοῖραν", "μοῖρα", "μοῖραι", "μοιρῶν", "μοίραις", "μοίρας"],
             no_dual(A_SHORT), HQ37 + ".1, short α (stem in ε, ι, ρ)", "1st decl. short α", HQ_SLOTS),
        noun("πολίτης", "citizen", "m.",
             ["πολίτης", "πολίτου", "πολίτῃ", "πολίτην", "πολῖτα", "πολῖται", "πολιτῶν", "πολίταις", "πολίτας"],
             no_dual(MASC_ETA), HQ37 + ".2, masculine in -ης", "1st decl. masculine", HQ_SLOTS),
        noun("ποιητής", "poet", "m.",
             ["ποιητής", "ποιητοῦ", "ποιητῇ", "ποιητήν", "ποιητά", "ποιηταί", "ποιητῶν", "ποιηταῖς", "ποιητάς"],
             no_dual(MASC_ETA), HQ37 + ".2, masculine in -ης", "1st decl. masculine", HQ_SLOTS),
        noun("νεανίας", "young man", "m.",
             ["νεανίας", "νεανίου", "νεανίᾳ", "νεανίαν", "νεανία", "νεανίαι", "νεανιῶν", "νεανίαις", "νεανίας"],
             no_dual(MASC_A), HQ37 + ".2, masculine in -ᾱς (stem in ε, ι, ρ)", "1st decl. masculine", HQ_SLOTS),
        adjective("ἀγαθός, ἀγαθή, ἀγαθόν", "good", ["masc.", "fem.", "neut."],
                  [["ἀγαθός", "ἀγαθοῦ", "ἀγαθῷ", "ἀγαθόν", "ἀγαθέ", "ἀγαθοί", "ἀγαθῶν", "ἀγαθοῖς", "ἀγαθούς"],
                   ["ἀγαθή", "ἀγαθῆς", "ἀγαθῇ", "ἀγαθήν", "ἀγαθή", "ἀγαθαί", "ἀγαθῶν", "ἀγαθαῖς", "ἀγαθάς"],
                   ["ἀγαθόν", "ἀγαθοῦ", "ἀγαθῷ", "ἀγαθόν", "ἀγαθόν", "ἀγαθά", "ἀγαθῶν", "ἀγαθοῖς", "ἀγαθά"]],
                  [ADJ_M, ADJ_F_ETA, ADJ_N], HQ38 + ".1, three endings", "adjective, three endings (fem. η)"),
        adjective("ἄξιος, ἀξία, ἄξιον", "worthy", ["masc.", "fem.", "neut."],
                  [["ἄξιος", "ἀξίου", "ἀξίῳ", "ἄξιον", "ἄξιε", "ἄξιοι", "ἀξίων", "ἀξίοις", "ἀξίους"],
                   ["ἀξία", "ἀξίας", "ἀξίᾳ", "ἀξίαν", "ἀξία", "ἄξιαι", "ἀξίων", "ἀξίαις", "ἀξίας"],
                   ["ἄξιον", "ἀξίου", "ἀξίῳ", "ἄξιον", "ἄξιον", "ἄξια", "ἀξίων", "ἀξίοις", "ἄξια"]],
                  [ADJ_M, ADJ_F_A, ADJ_N], HQ38 + ".1, three endings, stem in ε, ι, ρ",
                  "adjective, three endings (fem. ᾱ)"),
        adjective("ἄδικος, ἄδικον", "unjust", ["masc./fem.", "neut."],
                  [["ἄδικος", "ἀδίκου", "ἀδίκῳ", "ἄδικον", "ἄδικε", "ἄδικοι", "ἀδίκων", "ἀδίκοις", "ἀδίκους"],
                   ["ἄδικον", "ἀδίκου", "ἀδίκῳ", "ἄδικον", "ἄδικον", "ἄδικα", "ἀδίκων", "ἀδίκοις", "ἄδικα"]],
                  [ADJ_M, ADJ_N], HQ38 + ".2, two endings", "adjective, two endings"),
]

VERB_SLOTS = ["1st sg.", "2nd sg.", "3rd sg.", "1st pl.", "2nd pl.", "3rd pl."]

# Extra single cards for week 5 (infinitives, principal parts).
EXTRAS = {
    "w5": [
        ("παιδεύω: present infinitive active", "παιδεύειν", "to educate, to be educating (progressive/repeated aspect) — H&Q §26"),
        ("παιδεύω: aorist infinitive active", "παιδεῦσαι", "to educate (simple aspect) — H&Q §26"),
        ("παιδεύω: the six principal parts", "παιδεύω, παιδεύσω, ἐπαίδευσα, πεπαίδευκα, πεπαίδευμαι, ἐπαιδεύθην",
         "I present · II future · III aorist · IV perfect act. · V perfect mid./pass. · VI aorist passive — H&Q §19"),
    ],
    "w7": [
        ("παιδεύω: perfect infinitive active", "πεπαιδευκέναι",
         "to have educated (completed aspect); always accented on the penult — H&Q §30"),
    ],
}

# ---------------------------------------------------------------------------
# Alphabet (Week 1 supplement). (capital, lower, name, translit, sound)
# ---------------------------------------------------------------------------
ALPHABET = [
    ("Α", "α", "ἄλφα", "a", "a as in father (long) or idea (short)"),
    ("Β", "β", "βῆτα", "b", "b"),
    ("Γ", "γ", "γάμμα", "g", "hard g as in go; before κ, γ, χ, ξ = ng"),
    ("Δ", "δ", "δέλτα", "d", "d"),
    ("Ε", "ε", "ἒ ψιλόν", "e", "short e as in pet"),
    ("Ζ", "ζ", "ζῆτα", "z", "zd as in wisdom (or dz)"),
    ("Η", "η", "ἦτα", "ē", "long open e as in French tête"),
    ("Θ", "θ", "θῆτα", "th", "aspirated t, as in top (later th as in thin)"),
    ("Ι", "ι", "ἰῶτα", "i", "i as in machine (long) or sit (short)"),
    ("Κ", "κ", "κάππα", "k", "k"),
    ("Λ", "λ", "λάμβδα", "l", "l"),
    ("Μ", "μ", "μῦ", "m", "m"),
    ("Ν", "ν", "νῦ", "n", "n"),
    ("Ξ", "ξ", "ξῖ", "x", "ks as in axe"),
    ("Ο", "ο", "ὂ μικρόν", "o", "short o as in pot"),
    ("Π", "π", "πῖ", "p", "p"),
    ("Ρ", "ρ", "ῥῶ", "r", "trilled r; initial ρ has rough breathing (ῥ)"),
    ("Σ", "σ, ς", "σίγμα", "s", "s as in sing; ς is used at the end of a word"),
    ("Τ", "τ", "ταῦ", "t", "t"),
    ("Υ", "υ", "ὖ ψιλόν", "y / u", "French u or German ü"),
    ("Φ", "φ", "φῖ", "ph", "aspirated p, as in pot (later f)"),
    ("Χ", "χ", "χῖ", "ch", "aspirated k, as in cat (later German ach)"),
    ("Ψ", "ψ", "ψῖ", "ps", "ps as in lapse"),
    ("Ω", "ω", "ὦ μέγα", "ō", "long open o as in saw"),
]
DIPHTHONGS = [
    ("αι", "ai as in aisle"), ("ει", "ei as in eight"), ("οι", "oi as in oil"),
    ("υι", "ui as in French huit"), ("αυ", "au as in how"), ("ευ", "e + u, as in feud said quickly"),
    ("ηυ", "ē + u"), ("ου", "oo as in food"),
    ("ᾳ, ῃ, ῳ", "iota subscript: long ᾱ, η, ω + ι (iota usually not pronounced)"),
    ("῾ (rough breathing)", "h before an initial vowel: ἁ = ha"),
    ("᾿ (smooth breathing)", "no h: ἀ = a"),
    ("ά ὰ ᾶ (acute, grave, circumflex)", "pitch accents: rising, lowered, rising-falling"),
]

# ---------------------------------------------------------------------------
# Vocabulary. (headword, english, pos/notes, source)
# ---------------------------------------------------------------------------
VOCAB = {
    "w2": [
        # Mastronarde Unit 3 (pp. 30–31) and Mollin & Williamson Lesson 2 (pp. 12–13)
        ("ἄγγελος, ἀγγέλου, ὁ", "messenger, herald", "noun", "Mastronarde U3"),
        ("ἀδελφός, ἀδελφοῦ, ὁ", "brother", "noun; voc. ἄδελφε", "Mastronarde U3"),
        ("ἄνεμος, ἀνέμου, ὁ", "wind", "noun", "Mastronarde U3"),
        ("ἄνθρωπος, ἀνθρώπου, ὁ", "human being, man (occasionally fem., woman)", "noun", "Mastronarde U3; M&W L2"),
        ("βίος, βίου, ὁ", "life, manner of living, livelihood", "noun", "Mastronarde U3"),
        ("διδάσκαλος, διδασκάλου, ὁ", "teacher; trainer of a chorus, producer of a play", "noun", "Mastronarde U3"),
        ("ἥλιος, ἡλίου, ὁ", "sun", "noun", "Mastronarde U3"),
        ("θάνατος, θανάτου, ὁ", "death", "noun", "Mastronarde U3; M&W L2"),
        ("θεός, θεοῦ, ὁ or ἡ", "god, divinity; goddess", "noun; no classical voc. sg.", "Mastronarde U3; M&W L2"),
        ("ἵππος, ἵππου, ὁ or ἡ", "horse; (fem.) mare", "noun", "Mastronarde U3"),
        ("λόγος, λόγου, ὁ", "word, speech, tale, story; account, reckoning; reason", "noun", "Mastronarde U3; M&W L2"),
        ("νόμος, νόμου, ὁ", "custom, convention; law", "noun", "Mastronarde U3; M&W L2"),
        ("οἶκος, οἴκου, ὁ", "house, home, dwelling; household", "noun", "Mastronarde U3; M&W L2"),
        ("πόλεμος, πολέμου, ὁ", "war", "noun", "Mastronarde U3"),
        ("στρατηγός, στρατηγοῦ, ὁ", "general", "noun", "Mastronarde U3"),
        ("στρατός, στρατοῦ, ὁ", "army, host", "noun", "Mastronarde U3"),
        ("φόβος, φόβου, ὁ", "fear", "noun", "Mastronarde U3"),
        ("ἰᾱτρός, ἰᾱτροῦ, ὁ", "healer, physician", "noun", "M&W L2"),
        ("πλοῦτος, πλούτου, ὁ", "wealth", "noun", "M&W L2"),
        ("φίλος, φίλου, ὁ", "friend", "noun", "M&W L2"),
        ("χρόνος, χρόνου, ὁ", "time", "noun", "M&W L2"),
        ("χρῡσός, χρῡσοῦ, ὁ", "gold", "noun", "M&W L2"),
        ("νόσος, νόσου, ἡ", "sickness, disease", "noun", "Mastronarde U3"),
        ("ὁδός, ὁδοῦ, ἡ", "road, path, way; journey", "noun", "Mastronarde U3; M&W L2"),
        ("ψῆφος, ψήφου, ἡ", "pebble (for reckoning, games, voting); vote", "noun", "Mastronarde U3"),
        ("βιβλίον, βιβλίου, τό", "book", "noun", "Mastronarde U3"),
        ("δῶρον, δώρου, τό", "gift; (political/judicial) bribe", "noun", "Mastronarde U3; M&W L2"),
        ("ἔργον, ἔργου, τό", "work, action, deed", "noun", "Mastronarde U3; M&W L2"),
        ("μέτρον, μέτρου, τό", "measure, size, distance; moderate amount, proportion", "noun", "Mastronarde U3"),
        ("παιδίον, παιδίου, τό", "child", "noun", "Mastronarde U3"),
        ("τέκνον, τέκνου, τό", "child, offspring", "noun", "M&W L2"),
        ("ἀπό (ἀπ᾿, ἀφ᾿)", "(+ gen.) away from, from", "preposition", "Mastronarde U3"),
        ("ἐκ (ἐξ before vowels)", "(+ gen.) out of, forth from; as a result of", "preposition", "Mastronarde U3; M&W L2"),
        ("ἐν", "(+ dat.) in, within, on, at, among", "preposition", "Mastronarde U3; M&W L2"),
        ("εἰς or ἐς", "(+ acc.) into, to, toward; with respect to", "preposition", "Mastronarde U3; M&W L2"),
        ("σύν", "(+ dat.) together with, with", "preposition", "Mastronarde U3"),
        ("ὑπό", "(+ gen. of agent) by", "preposition", "M&W L2"),
        ("ἀλλά", "but, but rather", "conjunction", "Mastronarde U3"),
        ("καί", "and; (adv.) even, also, too", "conjunction / adverb", "Mastronarde U3"),
        ("οὐ (οὐκ, οὐχ)", "not", "adverb; οὐκ before smooth breathing, οὐχ before rough", "Mastronarde U3; M&W L2"),
        ("ἀεί", "always", "adverb", "M&W L2"),
    ],
    "w4": [
        # Hansen & Quinn, Unit 1 Vocabulary, p. 31
        ("ἀγορᾱ́, ἀγορᾶς, ἡ", "market place", "noun", "H&Q U1"),
        ("ἀδελφός, ἀδελφοῦ, ὁ", "brother", "noun; voc. ἄδελφε", "H&Q U1"),
        ("ἄνθρωπος, ἀνθρώπου, ὁ", "man, human being", "noun", "H&Q U1"),
        ("βιβλίον, βιβλίου, τό", "book", "noun", "H&Q U1"),
        ("δῶρον, δώρου, τό", "gift; bribe (especially in pl.)", "noun", "H&Q U1"),
        ("εἰς", "(+ acc.) into, to; for (purpose)", "preposition", "H&Q U1"),
        ("ἐκ, ἐξ", "(+ gen.) from, out of", "preposition", "H&Q U1"),
        ("ἐν", "(+ dat.) in", "preposition", "H&Q U1"),
        ("ἔργον, ἔργου, τό", "work, deed", "noun", "H&Q U1"),
        ("θεός, θεοῦ, ὁ or ἡ", "god, goddess", "noun", "H&Q U1"),
        ("καί", "(conj.) and; (adv.) even, also", "conjunction / adverb", "H&Q U1"),
        ("καί . . . καί", "both . . . and", "conjunctions", "H&Q U1"),
        ("λόγος, λόγου, ὁ", "word, speech, story", "noun", "H&Q U1"),
        ("μάχη, μάχης, ἡ", "battle", "noun", "H&Q U1"),
        ("νῆσος, νήσου, ἡ", "island", "noun", "H&Q U1"),
        ("ὁ, ἡ, τό", "the; often shows possession", "definite article", "H&Q U1"),
        ("ὁδός, ὁδοῦ, ἡ", "road", "noun", "H&Q U1"),
        ("οἰκίᾱ, οἰκίᾱς, ἡ", "house", "noun", "H&Q U1"),
        ("Ὅμηρος, Ὁμήρου, ὁ", "Homer (epic poet)", "noun", "H&Q U1"),
        ("παιδεύει", "educates, teaches", "verb (3rd sg.)", "H&Q U1"),
        ("πέμπει", "sends", "verb (3rd sg.)", "H&Q U1"),
        ("τέχνη, τέχνης, ἡ", "art, skill, craft", "noun", "H&Q U1"),
        ("χώρᾱ, χώρᾱς, ἡ", "land, country", "noun", "H&Q U1"),
        ("ψῡχή, ψῡχῆς, ἡ", "soul", "noun", "H&Q U1"),
        ("ὦ", "O! (used with the vocative)", "interjection", "H&Q U1"),
    ],
    "w5": [
        # Hansen & Quinn, Unit 2 Vocabulary, p. 53
        ("ἄγγελος, ἀγγέλου, ὁ", "messenger", "noun", "H&Q U2"),
        ("ἀπό", "(+ gen.) from, away from", "preposition", "H&Q U2"),
        ("ἆρα", "introduces a question (not translated)", "particle", "H&Q U2"),
        ("γάρ", "for (explanatory)", "postpositive conjunction", "H&Q U2"),
        ("δέ", "but; and", "postpositive conjunction", "H&Q U2"),
        ("ἕξ", "six", "indeclinable numeral", "H&Q U2"),
        ("εὖ", "well", "adverb", "H&Q U2"),
        ("ζῷον, ζῴου, τό", "animal", "noun", "H&Q U2"),
        ("ἤ", "or", "conjunction", "H&Q U2"),
        ("ἤ . . . ἤ", "either . . . or", "conjunctions", "H&Q U2"),
        ("κελεύω, κελεύσω, ἐκέλευσα, κεκέλευκα, κεκέλευσμαι, ἐκελεύσθην", "order, command", "verb (+ acc. of person + infinitive)", "H&Q U2"),
        ("λῡ́ω, λῡ́σω, ἔλῡσα, λέλυκα, λέλυμαι, ἐλύθην", "unbind, free, release; dissolve; destroy", "verb", "H&Q U2"),
        ("μέν . . . δέ", "on the one hand . . . on the other hand", "postpositive conjunctions", "H&Q U2"),
        ("νῦν", "now", "adverb", "H&Q U2"),
        ("ξένος, ξένου, ὁ", "guest-friend, host, stranger, foreigner", "noun", "H&Q U2"),
        ("οὐ, οὐκ, οὐχ", "not", "adverb", "H&Q U2"),
        ("παιδεύω, παιδεύσω, ἐπαίδευσα, πεπαίδευκα, πεπαίδευμαι, ἐπαιδεύθην", "educate, teach", "verb", "H&Q U2"),
        ("παρά", "(+ gen.) from (the side of); (+ dat.) at (the side of), at the house of; (+ acc.) to (the side of), beside; contrary to", "preposition", "H&Q U2"),
        ("πέμπω, πέμψω, ἔπεμψα, πέπομφα, πέπεμμαι, ἐπέμφθην", "send", "verb", "H&Q U2"),
        ("πέντε", "five", "indeclinable numeral", "H&Q U2"),
        ("πόλεμος, πολέμου, ὁ", "war", "noun", "H&Q U2"),
        ("πρό", "(+ gen.) before; in front of", "preposition", "H&Q U2"),
        ("στέφανος, στεφάνου, ὁ", "crown, wreath", "noun", "H&Q U2"),
        ("φίλος, φίλου, ὁ", "friend", "noun", "H&Q U2"),
        ("φιλίᾱ, φιλίᾱς, ἡ", "friendship", "noun", "H&Q U2"),
        ("χρῡσός, χρῡσοῦ, ὁ", "gold", "noun", "H&Q U2"),
    ],
    "w7": [
        # Hansen & Quinn, Unit 3 Vocabulary, p. 71 (notes pp. 72–73)
        ("ἆθλον, ἄθλου, τό", "prize", "noun", "H&Q U3"),
        ("ἀλλά", "but (stronger contrast than δέ; begins its clause)", "conjunction", "H&Q U3"),
        ("ἀντί", "(+ gen.) instead of", "preposition", "H&Q U3"),
        ("ἀρετή, ἀρετῆς, ἡ", "excellence, virtue", "noun", "H&Q U3"),
        ("βουλή, βουλῆς, ἡ", "will; council", "noun", "H&Q U3"),
        ("γράφω, γράψω, ἔγραψα, γέγραφα, γέγραμμαι, ἐγράφην", "write, draw", "verb; PP VI has no -θ-", "H&Q U3"),
        ("δή", "in fact, of course", "postpositive particle", "H&Q U3"),
        ("δῆμος, δήμου, ὁ", "the people", "noun", "H&Q U3"),
        ("δημοκρατίᾱ, δημοκρατίᾱς, ἡ", "democracy", "noun", "H&Q U3"),
        ("διά", "(+ gen.) through; (+ acc.) on account of", "preposition", "H&Q U3"),
        ("εἰρήνη, εἰρήνης, ἡ", "peace", "noun", "H&Q U3"),
        ("ἐκκλησίᾱ, ἐκκλησίᾱς, ἡ", "assembly", "noun", "H&Q U3"),
        ("ἐπεί", "after, when, since", "conjunction (temporal or causal)", "H&Q U3"),
        ("ἐπειδή", "after, when, since", "conjunction (ἐπεί + δή)", "H&Q U3"),
        ("θῡ́ω, θῡ́σω, ἔθῡσα, τέθυκα, τέθυμαι, ἐτύθην", "sacrifice", "verb", "H&Q U3"),
        ("θυσίᾱ, θυσίᾱς, ἡ", "sacrifice", "noun", "H&Q U3"),
        ("ἵνα", "in order that", "conjunction (purpose clauses)", "H&Q U3"),
        ("μή", "not (negates purpose clauses)", "adverb", "H&Q U3"),
        ("νῑ́κη, νῑ́κης, ἡ", "victory", "noun", "H&Q U3"),
        ("ὅπως", "in order that", "conjunction (purpose clauses)", "H&Q U3"),
        ("ὀφθαλμός, ὀφθαλμοῦ, ὁ", "eye", "noun", "H&Q U3"),
        ("παύω, παύσω, ἔπαυσα, πέπαυκα, πέπαυμαι, ἐπαύθην", "make stop, stop", "verb", "H&Q U3"),
        ("περί", "(+ gen.) concerning, about; (+ dat.) around; (+ acc.) around, concerning", "preposition", "H&Q U3"),
        ("φυλάττω, φυλάξω, ἐφύλαξα, πεφύλαχα, πεφύλαγμαι, ἐφυλάχθην", "guard", "verb; aspirated perfect", "H&Q U3"),
        ("ὡς", "in order that", "conjunction (purpose clauses)", "H&Q U3"),
    ],
    "w10": [
        # Hansen & Quinn, Unit 4 Vocabulary, pp. 99–100 (notes pp. 100–103)
        ("ἀγαθός, ἀγαθή, ἀγαθόν", "good (morally good; serviceable)", "adjective", "H&Q U4"),
        ("ἄν", "used in some conditional sentences (not translated; never first in its clause)", "particle", "H&Q U4"),
        ("ἄξιος, ἀξίᾱ, ἄξιον", "worthy, worth (+ gen.)", "adjective", "H&Q U4"),
        ("ἀνάξιος, ἀνάξιον", "unworthy (+ gen.)", "adjective, two endings (alpha privative)", "H&Q U4"),
        ("ἀρχή, ἀρχῆς, ἡ", "beginning; rule, empire", "noun", "H&Q U4"),
        ("γέφῡρα, γεφῡ́ρᾱς, ἡ", "bridge", "noun", "H&Q U4"),
        ("διδάσκω, διδάξω, ἐδίδαξα, δεδίδαχα, δεδίδαγμαι, ἐδιδάχθην", "teach", "verb", "H&Q U4"),
        ("δίκη, δίκης, ἡ", "justice; lawsuit", "noun", "H&Q U4"),
        ("ἄδικος, ἄδικον", "unjust", "adjective, two endings (alpha privative)", "H&Q U4"),
        ("δίκαιος, δικαίᾱ, δίκαιον", "just", "adjective", "H&Q U4"),
        ("ἐθέλω, ἐθελήσω, ἠθέλησα, ἠθέληκα, —, —", "be willing, wish (+ infinitive); οὐκ ἐθέλω: refuse",
         "verb; ἐ- belongs to the stem; augment lengthens it to ἠ- (imperf. ἤθελον)", "H&Q U4"),
        ("εἰ", "if", "particle (proclitic)", "H&Q U4"),
        ("ἐάν", "if (= εἰ + ἄν)", "particle", "H&Q U4"),
        ("ἡμέρᾱ, ἡμέρᾱς, ἡ", "day", "noun", "H&Q U4"),
        ("θάλαττα, θαλάττης, ἡ", "sea", "noun", "H&Q U4"),
        ("θάπτω, θάψω, ἔθαψα, —, τέθαμμαι, ἐτάφην", "bury", "verb", "H&Q U4"),
        ("καίτοι", "and further, and yet", "particle (accent is an exception)", "H&Q U4"),
        ("κακός, κακή, κακόν", "bad, evil", "adjective", "H&Q U4"),
        ("καλός, καλή, καλόν", "beautiful, noble, good", "adjective", "H&Q U4"),
        ("μετά", "(+ gen.) with; (+ acc.) after", "preposition", "H&Q U4"),
        ("μοῖρα, μοίρᾱς, ἡ", "fate", "noun", "H&Q U4"),
        ("μοῦσα, μούσης, ἡ", "muse", "noun", "H&Q U4"),
        ("νεᾱνίᾱς, νεᾱνίου, ὁ", "young man", "noun", "H&Q U4"),
        ("ὅπλον, ὅπλου, τό", "tool; (pl.) weapons", "noun", "H&Q U4"),
        ("ὁπλῑ́της, ὁπλῑ́του, ὁ", "hoplite, heavy-armed foot-soldier", "noun", "H&Q U4"),
        ("πάλαι", "long ago", "adverb (also attributive: οἱ πάλαι ἄνθρωποι, men of old)", "H&Q U4"),
        ("ποιητής, ποιητοῦ, ὁ", "poet, author", "noun", "H&Q U4"),
        ("πολῑ́της, πολῑ́του, ὁ", "citizen", "noun", "H&Q U4"),
        ("στρατιώτης, στρατιώτου, ὁ", "soldier", "noun", "H&Q U4"),
        ("σύν", "(+ dat.) with", "preposition", "H&Q U4"),
        ("τάττω, τάξω, ἔταξα, τέταχα, τέταγμαι, ἐτάχθην", "draw up in order, station, appoint", "verb", "H&Q U4"),
        ("φίλος, φίλη, φίλον", "dear, beloved, one's own", "adjective", "H&Q U4"),
    ],
}


# ---------------------------------------------------------------------------
# Formation rules for the all-verbs review sheet (in our words; patterns from H&Q Units 2–3).
# The sheet also computes overlaps from the paradigms above: identical forms, accent-only pairs, shared endings.
# ---------------------------------------------------------------------------
VERB_NOTES = [
    "The augment ἐ- appears only in the indicative of the past (secondary) tenses: imperfect, aorist, pluperfect. "
    "Subjunctive, optative and infinitive never take it, so the aorist subjunctive παιδεύσω has no ἐ- although ἐπαίδευσα does.",
    "σ marks the future and the whole aorist system; κ (with reduplication πε-) marks the perfect active system: "
    "perfect, pluperfect, perfect infinitive.",
    "ψ and ξ hide the σ: a stem in π, β, φ + σ gives ψ (πέμψω, γράψω); a stem in κ, γ, χ or ττ + σ gives ξ (φυλάξω).",
    "Not every perfect has κ: πέπομφα (πέμπω) and πεφύλαχα (φυλάττω) are aspirated perfects, and γέγραφα keeps "
    "the stem's φ. Reduplication repeats the first consonant with ε; an aspirate is repeated unaspirated: "
    "θύω → τέθυκα, φυλάττω → πεφύλαχα.",
    "Subjunctive = the indicative's thematic vowel lengthened (ο → ω, ε → η, ει → ῃ): παιδεύομεν → παιδεύωμεν, "
    "παιδεύει → παιδεύῃ. Present and aorist subjunctive share every ending; only the σ of the stem tells them apart.",
    "Optative = a vowel + ι before the endings -μι, -ς, (none), -μεν, -τε, -εν: οι in the present, αι in the aorist.",
    "There is no future subjunctive: παιδεύσω is future indicative or aorist subjunctive, and context decides.",
    "One letter apart: παιδεύει / παιδεύῃ, παιδεύσει / παιδεύσῃ, παιδεύετε / παιδεύητε (indicative / subjunctive).",
    "Sequence of moods: after a primary main verb (present, future, perfect) a purpose clause takes the subjunctive; "
    "after a secondary one (imperfect, aorist, pluperfect) it takes the optative.",
]


# English forms for generated paradigms of the other vocabulary verbs (base, 3rd sg., past, past participle, -ing)
VERB_ENGLISH = {
    "παιδεύω": ("educate", "educates", "educated", "educated", "educating"),
    "κελεύω": ("order", "orders", "ordered", "ordered", "ordering"),
    "λῡ́ω": ("free", "frees", "freed", "freed", "freeing"),
    "πέμπω": ("send", "sends", "sent", "sent", "sending"),
    "γράφω": ("write", "writes", "wrote", "written", "writing"),
    "θῡ́ω": ("sacrifice", "sacrifices", "sacrificed", "sacrificed", "sacrificing"),
    "παύω": ("stop", "stops", "stopped", "stopped", "stopping"),
    "φυλάττω": ("guard", "guards", "guarded", "guarded", "guarding"),
}


# ---------------------------------------------------------------------------
# Accent rules: our summary of Hansen & Quinn, Introduction §§10–12 and the accent notes in Units 1–3.
# Each item: (rule, [example words]); examples are words from these decks, shown with audio.
# ---------------------------------------------------------------------------
ACCENT_PATTERNS = [   # H&Q §10, "Possibilities of accent": schematic, rule, example
    ("a · p · ú  + pause", "Acute on the ultima only before a pause (end of sentence, comma, semicolon).", "ὁδός"),
    ("a · p · ù  + word", "Before another word with no pause, an acute on the ultima becomes grave.", "τὸν λόγον"),
    ("a · ṕ · u", "Acute on the penult is allowed whatever the ultima, except as in the last row.", "ἀνθρώπου"),
    ("á · p · ŭ", "Acute on the antepenult only when the ultima is short.", "ἄνθρωπος"),
    ("a · p · ῦ", "Circumflex on the ultima: only over a long vowel or diphthong.", "ὁδοῦ"),
    ("a · p̄̃ · ŭ", "An accented long penult before a short ultima MUST be circumflex; a circumflex on the penult is "
                  "never possible before a long ultima.", "δῶρον"),
]

ACCENT_RULES = [
    {"title": "Where an accent can go", "source": "Hansen & Quinn §10", "items": [
        ("Three accents: acute ´ (pitch rises), grave ` (pitch lowered), circumflex ῀ (rise and fall on one syllable). "
         "The accent is part of a word's spelling: learn it with the word.", []),
        ("Only the last three syllables can carry it: the ultima (last), the penult (next to last) and the antepenult "
         "(third from the end).", []),
        ("It is written over the vowel, or over the second letter of a diphthong. A breathing comes before an acute "
         "or grave, and under a circumflex.", ["ἄνθρωπος", "οἶκος", "ἦτα"]),
        ("Circumflex: only over a long vowel or diphthong, only on the ultima or penult. Grave: only on the ultima, "
         "replacing an acute there when another word follows without a pause.", ["θεῶν", "τὸν λόγον"]),
    ]},
    {"title": "Long or short?", "source": "Hansen & Quinn §§10, 14–15, 33–34", "items": [
        ("Long: η, ω, every diphthong, and α, ι, υ when marked with a macron (ᾱ ῑ ῡ) or carrying a circumflex. "
         "Short: ε, ο, and unmarked α, ι, υ.", ["χώρᾱ", "δρᾶμα"]),
        ("Final -αι and -οι count as SHORT for accent, so a long accented penult before them takes a circumflex.",
         ["χῶραι", "ἄνθρωποι", "νῆσοι"]),
        ("Exception: in the optative, final -οι and -αι count as LONG.", ["παιδεύοι", "παιδεύσαι"]),
    ]},
    {"title": "Recessive accent: verbs", "source": "Hansen & Quinn §11", "items": [
        ("Most verb forms push the accent as far from the end as the rules allow.", []),
        ("Three or more syllables: short ultima → acute on the antepenult; long ultima → acute on the penult.",
         ["ἐπαίδευον", "παιδεύει", "πεπαίδευκα", "ἔπαυσα"]),
        ("Two syllables: the accent is on the penult. Short penult → acute; long penult → circumflex before a short "
         "ultima, acute before a long one.", ["πέμπω", "παύω"]),
        ("Infinitives so far break the pattern: the aorist active infinitive is accented on the penult (so παιδεῦσαι, "
         "unlike the optative παιδεύσαι), and the perfect active infinitive always on the penult.",
         ["παιδεῦσαι", "πεπαιδευκέναι"]),
    ]},
    {"title": "Persistent accent: nouns", "source": "Hansen & Quinn §§12, 14–15", "items": [
        ("A noun's accent is given by the nominative singular and tries to stay on that syllable in every form. "
         "When the rules force a change, it changes kind first (circumflex → acute), then position.", []),
        ("Changes kind: a long penult keeps the accent but must turn acute before a long ultima.",
         ["νῆσος", "νήσου", "δῶρον", "δώρου"]),
        ("Changes position: an antepenult accent moves to the penult when the ultima turns long.",
         ["ἄνθρωπος", "ἀνθρώπου", "θάλαττα", "θαλάττης"]),
        ("First declension: the genitive plural is always -ῶν, whatever the nominative's accent.",
         ["τεχνῶν", "χωρῶν", "θαλαττῶν"]),
        ("First and second declension: a noun with an acute on the ultima in the nominative takes a circumflex in the "
         "genitive and dative, singular and plural.", ["ὁδός", "ὁδοῦ", "ὁδῷ", "φυγή", "φυγῆς", "θεᾶς"]),
        ("The vocative ἄδελφε (from ἀδελφός) is an exception to learn separately.", ["ἄδελφε"]),
    ]},
    {"title": "Words with no accent", "source": "Hansen & Quinn §16; Unit 3 vocabulary notes", "items": [
        ("Proclitics have no accent and are pronounced with the following word: the article forms ὁ, ἡ, οἱ, αἱ, and "
         "the negative οὐ (οὐκ, οὐχ). μή is not a proclitic.", ["ὁ λόγος", "οὐ πέμπει"]),
    ]},
]
