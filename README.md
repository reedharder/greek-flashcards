# Ancient Greek flashcards

Anki decks and a browser study app for introductory Ancient Greek: noun and article paradigms, the παιδεύω indicative active, and vocabulary. Every Greek form has a synthesized audio clip.

- **Study app:** https://reedharder.github.io/greek-flashcards/ (spaced repetition with audio; progress is saved in your browser). Each week also has a review sheet: the paradigm tables with endings highlighted (augment and tense sign σ marked), tap-to-hear forms, an optional hide-forms self-test, and the vocabulary list.
- **Anki decks:** [`docs/anki/`](docs/anki/). `Greek_All_Weeks.apkg` imports everything at once.

Paradigms follow Mastronarde, *Introduction to Attic Greek* (nouns, article) and Hansen & Quinn, *Greek: An Intensive Course* (verb); vocabulary cards cite their textbook list. Audio comes in two female voices, switchable in the app:

- **Ancient (reconstructed):** espeak-ng's Ancient Greek (`grc`) phonemes spoken by the Piper neural voice `en_US-lessac-high`. The Anki decks use this voice.
- **Modern Greek:** macOS's Melina voice reading the monotonic spelling. This is Modern pronunciation (β = v, η/ι/υ/οι = ee), useful for comparison only.

## Rebuilding

```
pip install genanki && brew install espeak-ng lame
python3 -m venv .venv-tts && .venv-tts/bin/pip install piper-tts   # Piper; the voice model downloads on first run
python3 build/build.py       # decks + audio -> anki/, card data + review sheets -> app/cards.json
python3 build/build_app.py   # study site -> docs/
```

The Modern Greek voice needs macOS (`say -v Melina`).
