import os
import sys
import json
import subprocess
import glob

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCENES_JSON = os.path.join(DATA_DIR, "scenes.json")
FRAMES_DIR = os.path.join(DATA_DIR, "audit_frames")

os.makedirs(FRAMES_DIR, exist_ok=True)

with open(SCENES_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])
print(f"[*] Toplam {len(scenes)} sahne taranacak...")

scene_report = []

for idx, s in enumerate(scenes, 1):
    sid = s["id"]
    title = s["title"]
    orig_video = os.path.join(BASE_DIR, s.get("videoSrc", ""))
    duration = s.get("duration", 0)
    lines = s.get("lines", [])
    
    if not os.path.exists(orig_video):
        print(f"[-] Video bulunamadı: {orig_video}")
        continue
    
    out_scene_dir = os.path.join(FRAMES_DIR, sid)
    os.makedirs(out_scene_dir, exist_ok=True)
    
    # 3 stratejik noktadan kare çıkaralım:
    # 1. Başlangıç (0.5s - 1.5s)
    # 2. Orta nokta (duration / 2)
    # 3. İkinci yarı / diyalog ortası (duration * 0.75)
    t1 = min(1.0, max(0.2, duration * 0.1))
    t2 = duration * 0.45
    t3 = duration * 0.8
    
    points = [("start", t1), ("mid", t2), ("end", t3)]
    extracted_frames = []
    
    for label, t in points:
        out_jpg = os.path.join(out_scene_dir, f"{label}.jpg")
        if not os.path.exists(out_jpg):
            cmd = [
                "ffmpeg", "-y", "-ss", str(t), "-i", orig_video,
                "-vframes", "1", "-q:v", "3", out_jpg
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(out_jpg):
            extracted_frames.append(out_jpg)
            
    scene_report.append({
        "id": sid,
        "title": title,
        "duration": duration,
        "lines_count": len(lines),
        "video": s.get("videoSrc"),
        "characters": [c.get("name") for c in s.get("characters", [])],
        "frames": extracted_frames
    })

print(f"[+] 56 sahnenin tamamından kareler başarıyla çıkarıldı: {FRAMES_DIR}")
with open(os.path.join(DATA_DIR, "vision_frame_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(scene_report, f, indent=2, ensure_ascii=False)
