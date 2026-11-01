"""Step 1: describe the API of candidate open-source TTS Spaces."""
import json, traceback
from gradio_client import Client
SPACES = ["Qwen/Qwen3-TTS", "Qwen/Qwen3-TTS-Voice-Design", "maya-research/maya2-native-studio", "ai4bharat/indic-parler-tts", "BreezeBlue/breeze-tts-2-demo"]
out = {}
for s in SPACES:
    try:
        c = Client(s, verbose=False); out[s] = c.view_api(return_format="dict", print_info=False)
    except Exception as e:
        out[s] = {"error": repr(e)[:500]}
json.dump(out, open("tts/spaces/api.json", "w"), indent=1, default=str)
