"""Step 2: same 3 lines from Maya 2 Native voices and a Qwen3-TTS designed voice."""
import os, shutil, json, traceback
from gradio_client import Client
TEXT = ("JEE Main is less than twelve weeks away. Is your mock score stuck? "
        "A TutorDA mock shows exactly where your marks went: the wrong answers, the slow ones, and the lucky guesses. "
        "Your first mock is free. After that, it's ninety-nine rupees a month. About three rupees a day!")
OUT = "tts/spaces"; log = {}
def save(res, name):
    cands = res if isinstance(res, (list, tuple)) else [res]
    for c in cands:
        p = c.get("path") if isinstance(c, dict) else c
        if isinstance(p, str) and os.path.exists(p):
            ext = os.path.splitext(p)[1] or ".wav"; shutil.copy(p, f"{OUT}/{name}{ext}"); return f"{name}{ext}"
    return "no file: " + repr(res)[:300]
try:
    m = Client("maya-research/maya2-native-studio", verbose=False)
    for v in ["Charvi", "Jahnavi", "Kayal", "Nivedita", "Satvik"]:
        try: log[v] = save(m.predict(TEXT, "en", v, True, 7, False, api_name="/speak"), f"maya_{v}")
        except Exception as e: log[v] = "error " + repr(e)[:300]
except Exception as e: log["maya"] = "error " + repr(e)[:300]
try:
    q = Client("Qwen/Qwen3-TTS", verbose=False)
    desc = ("A young Indian woman in her late twenties, a friendly maths teacher, speaking English with a clear, natural Indian accent. "
            "Warm, energetic and encouraging, like explaining to one student; lively rise and fall in pitch, medium pace, crisp consonants.")
    log["qwen_design"] = save(q.predict(TEXT, "English", desc, api_name="/generate_voice_design"), "qwen_design_indian_teacher")
except Exception as e: log["qwen_design"] = "error " + repr(e)[:300]
json.dump(log, open(f"{OUT}/log.json", "w"), indent=1)
