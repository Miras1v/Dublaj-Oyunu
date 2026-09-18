import os
import sys
import json
import whisper

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCENES_JSON = os.path.join(DATA_DIR, "scenes.json")
OUT_JSON = os.path.join(DATA_DIR, "all_whisper_ground_truth.json")

with open(SCENES_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])
print(f"[*] Toplam {len(scenes)} sahne için Whisper word-level analizi başlıyor...")

model = whisper.load_model("small")

results = {}

for idx, s in enumerate(scenes, 1):
    sid = s["id"]
    orig_video = os.path.join(BASE_DIR, s.get("videoSrc", ""))
    
    if not os.path.exists(orig_video):
        continue
    
    print(f"[{idx}/{len(scenes)}] Çözümleniyor: {sid} ({s.get('title')})...")
    
    try:
        # word_timestamps=True ile milimetrik zamanlama
        trans = model.transcribe(orig_video, language="tr", word_timestamps=True)
        segments = []
        for seg in trans.get("segments", []):
            words = []
            for w in seg.get("words", []):
                words.append({
                    "word": w.get("word", "").strip(),
                    "start": round(w.get("start", 0), 2),
                    "end": round(w.get("end", 0), 2)
                })
            segments.append({
                "start": round(seg.get("start", 0), 2),
                "end": round(seg.get("end", 0), 2),
                "text": seg.get("text", "").strip(),
                "words": words
            })
        
        results[sid] = {
            "id": sid,
            "current_title": s.get("title"),
            "full_text": trans.get("text", "").strip(),
            "segments": segments
        }
    except Exception as e:
        print(f"[-] Hata {sid}: {e}")

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"[+] TÜM SAHNELERİN SES VE KELİME ZAMANLAMALARI BAŞARIYLA KAYDEDİLDİ: {OUT_JSON}")
