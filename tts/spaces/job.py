"""Charvi (Maya 2 Native): whole Spot-the-mistake script in ONE request (split by silences later)."""
import json, urllib.request
from gradio_client import Client
TEXT = ("This answer comes out to minus two. But one over x squared is never negative. ... "
        "Can you spot the mistake? Pause now. ... "
        "Here it is: one over x squared blows up at x equals zero, right inside the limits. ... "
        "You can't use the formula across that break. This integral doesn't even exist. ... "
        "TutorDA trick: positive function, positive answer. Bottom hits zero inside the limits? Stop. ... "
        "Did you spot it? Comment FOUND or MISSED.")
log = {}
try:
    m = Client("maya-research/maya2-native-studio", verbose=False)
    r = m.predict(TEXT, "en", "Charvi", True, 7, False, api_name="/speak")
    urllib.request.urlretrieve("https://maya-research-maya2-native-studio.hf.space" + r["audio_url"], "tts/spaces/charvi_spot_full.wav"); log["spot"] = r
except Exception as e:
    log["spot"] = "error " + repr(e)[:400]
json.dump(log, open("tts/spaces/log_spot.json", "w"), indent=1, default=str)
