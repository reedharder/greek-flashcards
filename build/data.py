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
    {"id": "w6", "num": 6, "label": "Week 6", "topic": "Review"},
]

# ---------------------------------------------------------------------------
# Paradigm tables. Each table: rows of (slot label, form); endings optional.
# Slot labels follow the source table's rows.
# ---------------------------------------------------------------------------
NOUN_SLOTS = ["nom. sg.", "gen. sg.", "dat. sg.", "acc. sg.", "voc. sg.",
              "nom./acc./voc. du.", "gen./dat. du.",
              "nom./voc. pl.", "gen. pl.", "dat. pl.", "acc. pl."]


def noun(lemma, gloss, gender, forms, endings, source, group):
    assert len(forms) == 11 and len(endings) == 11, lemma
    return {"kind": "noun", "lemma": lemma, "gloss": gloss, "gender": gender,
            "slots": NOUN_SLOTS, "forms": forms, "endings": endings,
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
VERB_SLOTS = ["1st sg.", "2nd sg.", "3rd sg.", "1st pl.", "2nd pl.", "3rd pl."]

# Extra single cards for week 5 (infinitives, principal parts).
EXTRAS = {
    "w5": [
        ("παιδεύω: present infinitive active", "παιδεύειν", "to educate, to be educating (progressive/repeated aspect) — H&Q §26"),
        ("παιδεύω: aorist infinitive active", "παιδεῦσαι", "to educate (simple aspect) — H&Q §26"),
        ("παιδεύω: the six principal parts", "παιδεύω, παιδεύσω, ἐπαίδευσα, πεπαίδευκα, πεπαίδευμαι, ἐπαιδεύθην",
         "I present · II future · III aorist · IV perfect act. · V perfect mid./pass. · VI aorist passive — H&Q §19"),
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
}
