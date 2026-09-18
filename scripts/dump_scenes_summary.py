import json

with open(r"C:\Users\mirac\Desktop\Code\Dublaj-Oyunu\data\scenes.json", encoding="utf-8") as f:
    scenes = json.load(f)["scenes"]

with open(r"C:\Users\mirac\Desktop\Code\Dublaj-Oyunu\data\scenes_summary.txt", "w", encoding="utf-8") as out:
    for i, s in enumerate(scenes):
        out.write(f"=== {i+1:02d}. [{s['id']}] {s.get('title')} ({len(s.get('lines', []))} lines, {s.get('duration')}s) ===\n")
        out.write(f"Karakterler: {json.dumps(s.get('characters', []), ensure_ascii=False)}\n")
        for li, l in enumerate(s.get("lines", [])):
            out.write(f"  {li+1:02d}. [{l.get('startTime')}-{l.get('endTime')}s] {l.get('characterId')}: {l.get('text')}\n")
        out.write("\n")

print("Saved scenes_summary.txt successfully.")
