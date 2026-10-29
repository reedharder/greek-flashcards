"""Render audio clips in every voice. Run with the Piper venv: .venv-tts/bin/python build/tts.py jobs.json

jobs.json: [{"key": ..., "text": ..., "slow": bool}, ...]; writes anki/media/<voice>_<key>.mp3 for missing clips.

Voices:
  lessac  Piper en_US "lessac" (female), driven by espeak-ng "grc" phonemes, so reconstructed Attic
          (Piper's el_GR "rapunzelina" was tried: it babbles for seconds after short words)
  melina  macOS "Melina" (female), Modern Greek pronunciation of the monotonic spelling
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, "anki", "media")
VOICE_DIR = os.path.join(ROOT, "build", "voices")
HF = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/"
PIPER = {"lessac": "en/en_US/lessac/high/en_US-lessac-high"}
VOICES = ["lessac", "melina"]


def load_piper(path):
    base = os.path.join(VOICE_DIR, os.path.basename(path))
    os.makedirs(VOICE_DIR, exist_ok=True)
    for ext in (".onnx", ".onnx.json"):
        if not os.path.exists(base + ext):
            urllib.request.urlretrieve(HF + path + ext, base + ext)
    return PiperVoice.load(base + ".onnx")


VOWEL_START = re.compile(r"(^|[\s,])([aeiouyɛɔæɑʏ])")
EU_BEFORE_CONSONANT = re.compile(r"eʊ(?=[ˈˌ]?[^aeiouyɛɔæɑʏɪʊːˈˌ\s,.])")


def grc_phonemes(text):
    ipa = subprocess.run(["espeak-ng", "-q", "-v", "grc", "--ipa", text], capture_output=True, text=True, check=True).stdout
    ph = ", ".join(l.strip() for l in ipa.splitlines() if l.strip()) + "."
    # Piper all but drops an unstressed word-initial vowel (the augment of ἐπαίδευον): give it secondary stress
    ph = VOWEL_START.sub(r"\1ˌ\2", ph)
    # ευ before a consonant: Piper's ʊ smears into the next stop (-ευκ- sounded like -ευβ-); a w glide stays clean
    return EU_BEFORE_CONSONANT.sub("ew", ph)


def monotonic(text):
    """Polytonic -> monotonic for a Modern Greek voice: drop breathings and iota subscript, all accents -> tonos."""
    s = unicodedata.normalize("NFD", text)
    for mark in ("̓", "̔", "ͅ", "̄", "̆"):
        s = s.replace(mark, "")
    s = s.replace("̀", "́").replace("͂", "́")
    return unicodedata.normalize("NFC", s)


def to_mp3(wav, out):
    subprocess.run(["lame", "--quiet", "-m", "m", "-V", "7", wav, out], check=True)


def piper_clip(voice, text, slow, out):
    ids = voice.phonemes_to_ids(list(grc_phonemes(text)))
    a = voice.phoneme_ids_to_audio(ids, SynthesisConfig(length_scale=1.45 if slow else 1.1))
    a = (np.clip(a, -1, 1) * 32767).astype("int16")
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(voice.config.sample_rate); w.writeframes(a.tobytes())
        to_mp3(tmp.name, out)


def melina_clip(text, slow, out):
    with tempfile.TemporaryDirectory() as d:
        aiff, wav = os.path.join(d, "a.aiff"), os.path.join(d, "a.wav")
        subprocess.run(["say", "-v", "Melina", "-r", "110" if slow else "150", "-o", aiff, monotonic(text)], check=True)
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", aiff, wav], check=True)
        to_mp3(wav, out)


def main(jobs_path):
    jobs = json.load(open(jobs_path))
    os.makedirs(MEDIA, exist_ok=True)
    loaded = {}
    made = 0
    for v in VOICES:
        for j in jobs:
            out = os.path.join(MEDIA, f"{v}_{j['key']}.mp3")
            if os.path.exists(out):
                continue
            if v == "melina":
                melina_clip(j["text"], j["slow"], out)
            else:
                if v not in loaded:
                    loaded[v] = load_piper(PIPER[v])
                piper_clip(loaded[v], j["text"], j["slow"], out)
            made += 1
    print(f"tts: {made} new clips, {len(jobs)} per voice")


if __name__ == "__main__":
    main(sys.argv[1])
