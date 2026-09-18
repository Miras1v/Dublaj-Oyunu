import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/scenes.json', encoding='utf-8') as f:
    data = json.load(f)

scenes = data.get('scenes', [])
print(f"Toplam sahne: {len(scenes)}\n")

for i, s in enumerate(scenes):
    chars = s.get('characters', [])
    c_str = ', '.join(f"{c.get('id')} ({c.get('name')})" for c in chars)
    lines = s.get('lines', [])
    print(f"=== {i+1:02d}. [{s['id']}] {s.get('title')} ({len(lines)} replik, {s.get('duration')}s) ===")
    print(f"Karakterler: {c_str}")
    for l in lines:
        cid = l.get('characterId', 'Bilinmeyen')
        t = l.get('text', '')
        st = l.get('startTime', 0)
        et = l.get('endTime', 0)
        print(f"  [{st}-{et}s] {cid}: {t}")
    print()
