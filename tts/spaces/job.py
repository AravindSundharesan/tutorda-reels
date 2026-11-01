"""Charvi (Maya 2 Native): launch video script v2, one call per line, files fetched back from the Space."""
import json, urllib.request, os
from gradio_client import Client
L = ["JEE Main is less than twelve weeks away. Is your mock score stuck?",
     "Here's the problem. A score tells you how you did. Not why.",
     "A TutorDA mock shows exactly where your marks went: the wrong answers, the slow ones, and the lucky guesses.",
     "Stuck on a question? WhatsApp it. A real tutor explains it, step by step.",
     "Your first mock is free, and so is a week of doubt support. After that, it's ninety-nine rupees a month. About three rupees a day!",
     "Comment MOCK, and we'll send you the link."]
log = {}
m = Client("maya-research/maya2-native-studio", verbose=False)
for i, t in enumerate(L):
    try:
        r = m.predict(t, "en", "Charvi", True, 7, False, api_name="/speak")
        url = "https://maya-research-maya2-native-studio.hf.space" + r["audio_url"]
        urllib.request.urlretrieve(url, f"tts/spaces/charvi_launch_{i}.wav"); log[i] = r
    except Exception as e:
        log[i] = "error " + repr(e)[:300]
json.dump(log, open("tts/spaces/log_charvi.json", "w"), indent=1, default=str)
