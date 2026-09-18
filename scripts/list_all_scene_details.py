import json

with open(r"C:\Users\mirac\Desktop\Code\Dublaj-Oyunu\data\scenes.json", encoding="utf-8") as f:
    scenes = json.load(f)["scenes"]

for i, s in enumerate(scenes):
    c_names = [c["name"] for c in s.get("characters", [])]
    l_chars = set(l.get("characterId") for l in s.get("lines", []))
    print(f"{i+1:02d}. [{s['id']}] {s.get('title')} | Karakterler: {c_names} | Süre: {s.get('duration')}s | Replik: {len(s.get('lines', []))}")
