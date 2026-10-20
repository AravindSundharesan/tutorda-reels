"""Decode a 'B64START...B64END' tool-result file into a binary file. Usage: b64file.py RESULT.txt OUT"""
import sys, json, re, base64
raw = open(sys.argv[1]).read()
try: txt = "".join(x.get("text", "") for x in json.loads(raw))
except Exception: txt = raw
m = re.search(r"B64START([A-Za-z0-9+/=]+)B64END", txt); open(sys.argv[2], "wb").write(base64.b64decode(m.group(1))); print(sys.argv[2], len(base64.b64decode(m.group(1))))
