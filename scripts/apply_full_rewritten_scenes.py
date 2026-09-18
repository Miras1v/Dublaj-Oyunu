import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCENES_JSON = os.path.join(DATA_DIR, "scenes.json")
SCENES_JS = os.path.join(BASE_DIR, "js", "scenes.js")

sys.path.insert(0, BASE_DIR)

from scripts.build_perfect_scenes_part1 import PERFECT_SCENES as p1
from scripts.build_perfect_scenes_part2 import PERFECT_SCENES_2 as p2
from scripts.build_perfect_scenes_part3 import PERFECT_SCENES_3 as p3
from scripts.build_perfect_scenes_part4 import PERFECT_SCENES_4 as p4
from scripts.build_perfect_scenes_part5 import PERFECT_SCENES_5 as p5

all_rewritten = {}
all_rewritten.update(p1)
all_rewritten.update(p2)
all_rewritten.update(p3)
all_rewritten.update(p4)
all_rewritten.update(p5)

with open(SCENES_JSON, "r", encoding="utf-8") as f:
    orig_data = json.load(f)

scenes = orig_data["scenes"]

updated_count = 0
for s in scenes:
    sid = s["id"]
    if sid in all_rewritten:
        rw = all_rewritten[sid]
        s["title"] = rw["title"]
        s["description"] = rw["description"]
        s["characters"] = rw["characters"]
        
        # Format lines properly with line id
        new_lines = []
        valid_char_ids = set(c["id"] for c in rw["characters"])
        
        for idx, line in enumerate(rw["lines"], 1):
            cid = line["characterId"]
            if cid not in valid_char_ids:
                # Fallback to first character
                cid = rw["characters"][0]["id"]
            
            st = round(float(line["startTime"]), 2)
            et = round(float(line["endTime"]), 2)
            dur = round(et - st, 2)
            if dur <= 0:
                dur = 1.0
                et = round(st + 1.0, 2)
            
            new_lines.append({
                "id": f"{sid}_l{idx}",
                "characterId": cid,
                "startTime": st,
                "endTime": et,
                "duration": dur,
                "text": line["text"]
            })
            
        s["lines"] = new_lines
        updated_count += 1

print(f"Toplam {updated_count}/56 sahne sıfırdan yeniden yazıldı ve formatlandı.")

# 1. data/scenes.json kaydet
with open(SCENES_JSON, "w", encoding="utf-8") as f:
    json.dump(orig_data, f, ensure_ascii=False, indent=2)
print("data/scenes.json güncellendi.")

# 2. js/scenes.js kaydet
js_content = f"""// scenes.js - Miras Dublaj Oyunu Sahne Kütüphanesi
// 56 Sahne: Ground-Truth Whisper VAD + Vision Doğrulanmış ve Sıfırdan Kusursuz Yazılmış Sürüm

export const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};

const SCENES_DATA = SCENES;

if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ SCENES: SCENES_DATA, default: SCENES_DATA }};
}}
"""

with open(SCENES_JS, "w", encoding="utf-8") as f:
    f.write(js_content)
print("js/scenes.js güncellendi.")
