# Ancient Greek flashcards

Anki decks and a browser study app for introductory Ancient Greek: noun and article paradigms, the παιδεύω indicative active, and vocabulary. Every Greek form has a synthesized audio clip.

- **Study app:** https://reedharder.github.io/greek-flashcards/ (spaced repetition with audio; progress is saved in your browser)
- **Anki decks:** [`docs/anki/`](docs/anki/). `Greek_All_Weeks.apkg` imports everything at once.

Paradigms follow Mastronarde, *Introduction to Attic Greek* (nouns, article) and Hansen & Quinn, *Greek: An Intensive Course* (verb); vocabulary cards cite their textbook list. Audio comes from espeak-ng's Ancient Greek (`grc`) voice, using reconstructed pronunciation.

## Rebuilding

```
pip install genanki && brew install espeak-ng lame
python3 build/build.py       # decks + audio -> anki/, card data -> app/cards.json
python3 build/build_app.py   # study site -> docs/
```
