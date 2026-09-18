import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

with open(r"C:\Users\mirac\Desktop\Code\Dublaj-Oyunu\data\scenes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", [])
print(f"Total scenes: {len(scenes)}")

issues = []

for idx, scene in enumerate(scenes):
    s_id = scene.get("id")
    title = scene.get("title")
    duration = scene.get("duration", 0)
    lines = scene.get("lines", [])
    
    scene_issues = []
    
    # Check lines
    if not lines:
        scene_issues.append("Hiç replik yok!")
    
    prev_end = 0
    for li, line in enumerate(lines):
        text = line.get("text", "").strip()
        start = line.get("startTime", 0)
        end = line.get("endTime", 0)
        
        if not text or text == "Meme repliği":
            scene_issues.append(f"Hat [li={li}]: Boş veya varsayılan metin ('{text}')")
        
        if end <= start:
            scene_issues.append(f"Hat [li={li}]: Süre hatası (start={start} >= end={end})")
            
        if start > duration + 1.0 or end > duration + 2.0:
            scene_issues.append(f"Hat [li={li}]: Video süresini aşıyor (start={start}, end={end}, dur={duration})")
            
        # Check repetitive text or hallucination patterns (like Whisper loops)
        words = text.split()
        if len(words) > 4:
            # check if repeated word sequences
            for wlen in [1, 2, 3]:
                for wi in range(len(words) - 2*wlen + 1):
                    seq1 = words[wi:wi+wlen]
                    seq2 = words[wi+wlen:wi+2*wlen]
                    if seq1 == seq2 and len(seq1) >= 2:
                        scene_issues.append(f"Hat [li={li}]: Tekrar eden kalıp tespit edildi: '{' '.join(seq1)}' ({text})")
                        break
                        
        # Obvious Whisper hallucinations
        hallucination_indicators = ["altyazı", "izlediğiniz için", "abone ol", "beğenmeyi unutmayın", "www.", ".com", "albayrak", "amara", "subtitle", "çeviri"]
        for ind in hallucination_indicators:
            if ind in text.lower():
                scene_issues.append(f"Hat [li={li}]: Halüsinasyon şüphesi: '{ind}' in '{text}'")

    print(f"[{idx+1}/{len(scenes)}] {s_id} | {title} | {duration}s | lines: {len(lines)}")
    for l in lines:
        print(f"   [{l.get('startTime')}-{l.get('endTime')}s] {l.get('characterId')}: {l.get('text')}")
    if scene_issues:
        print(f"   ⚠️ SORUNLAR: {scene_issues}")
        issues.append((s_id, title, scene_issues))

print(f"\nToplam sorunlu sahne sayısı: {len(issues)}")
