#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Dublaj Oyunu - Baştan Sona Otomatik Transkript ve Sahne Yenileyici
Engine: faster-whisper (large-v3-turbo) + VAD Filter + Akıllı Konuşmacı Ayrımı
Tüm sahneleri baştan sona işler, halüsinasyonları ve hatalı metinleri temizler.
"""

import os
import sys
import json
import re
import time
import subprocess
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENES_JSON_PATH = os.path.join(BASE_DIR, "data", "scenes.json")
SCENES_JS_PATH = os.path.join(BASE_DIR, "js", "scenes.js")
VIDEOS_DIR = os.path.join(BASE_DIR, "assets", "videos")

# Korunacak, elle doğrulanmış kült sahneler
PROTECTED_SCENE_IDS = {
    "meme-artist-ne-arar",
    "meme-cikar-telefonunu",
    "kv-pala-oluler",
    "sifir-bir-cio",
    "sifir-bir-yahya-cezaevi",
    "meme-kolpacino-saatli-bomba",
    "meme-sonuc-ne-soru-cevap"
}

CHAR_STYLES = [
    {"name": "Karakter 1", "avatar": "🎤", "color": "#38bdf8"},
    {"name": "Karakter 2", "avatar": "🎭", "color": "#fbbf24"},
    {"name": "Karakter 3", "avatar": "🔥", "color": "#f87171"},
    {"name": "Karakter 4", "avatar": "😎", "color": "#a855f7"},
]

HALLUCINATIONS = [
    "izlediğiniz için", "abone ol", "beğenmeyi unutmayın",
    "altyazı", "çeviri", "subtitle", "www.", "http",
    "sesli betimleme derneği", "betimlemesi trt tarafından"
]

def clean_repetition(text):
    """Whisper'ın arka arkaya aynı kelimeleri tekrar etmesini önler."""
    words = text.split()
    if len(words) < 4:
        return text
    
    # 1'li, 2'li, 3'lü döngüleri temizle
    for n in [1, 2, 3]:
        cleaned = []
        i = 0
        while i < len(words):
            pattern = words[i:i+n]
            # sonraki blok da aynı mı?
            repeats = 0
            while i + (repeats + 1) * n <= len(words) and words[i + repeats*n : i + (repeats+1)*n] == pattern:
                repeats += 1
            if repeats > 2: # 3'ten fazla tekrar ediyorsa tekilleştir
                cleaned.extend(pattern)
                i += repeats * n
            else:
                cleaned.append(words[i])
                i += 1
        words = cleaned
    return " ".join(words)

def clean_text(text):
    t = text.strip()
    t = re.sub(r'\s+', ' ', t)
    # Çince / Kiril / Korece karakter temizliği (sadece Latin, Türkçe ve noktalama)
    cleaned = re.sub(r'[^\w\s\.,!\?\'"\-ğüşıöçĞÜŞİÖÇ]', '', t)
    cleaned = clean_repetition(cleaned)
    return cleaned.strip()

def is_hallucination(text):
    t = text.lower()
    for h in HALLUCINATIONS:
        if h in t:
            return True
    return False

def smart_title_from_lines(lines, fallback_title):
    # En uzun veya en vurucu replikten başlık üret
    candidates = [l["text"] for l in lines if len(l["text"]) > 6 and not is_hallucination(l["text"])]
    if not candidates:
        return fallback_title
    
    # Kült kalıpları tanıyalım
    joined = " ".join(candidates).lower()
    if "benim adım cafer" in joined:
        return "Meme - Benim Adım Cafer (Alayınıza Gider)"
    if "kemalizm" in joined or "çıkar göster" in joined or "döneksin" in joined:
        return "Meme - Doğu Perinçek vs Ertuğrul Kürkçü (Çıkar Göster)"
    if "zırh" in joined or "milyarder" in joined or "kahraman" in joined:
        return "Meme - Yenilmezler: Zırhını Çıkarırsan Ne Kalır?"
    if "keloğlan" in joined or "huysuz" in joined or "uzun" in joined:
        return "Meme - Keloğlan: Huysuz ve Uzun İksir Peşinde"
    if "ümit usta" in joined or "kuru" in joined:
        return "Meme - Ümit Usta: Kuru Fasulye Kalmadı"
    if "kerpeten ali" in joined or "araba" in joined:
        return "Meme - Ezel: Kerpeten Ali Sanayide"
    if "koca toteme çorba" in joined or "çorba" in joined and "totem" in joined:
        return "Meme - Toteme Çorba Yazmışlar"
    if "çoluk çocuğun elinde" in joined or "orman" in joined or "tayfun" in joined:
        return "Meme - Kolpaçino: Orman ve Çoluk Çocuk"
    if "za warudo" in joined or "dio" in joined or "jotaro" in joined or "saniye geçti" in joined:
        return "Meme - JoJo: Zamanı Durdurma (Za Warudo)"
    if "recep" in joined and "ali" in joined and "sistem" in joined:
        return "Meme - Technopat: Sistem Toplama Parodisi"
    if "hüsnü" in joined or "arka sokaklar" in joined:
        return "Meme - Arka Sokaklar: Komiser Hüsnü Çoban"

    first_line = candidates[0]
    words = first_line.split()
    if len(words) >= 3:
        clean_words = [w for w in words[:6] if not w.endswith("?")]
        if clean_words:
            cand = " ".join(clean_words).capitalize()
            # Noktalama temizle
            cand = re.sub(r'[\.,!\'"]', '', cand)
            if len(cand) >= 8:
                return f"Meme - {cand}"
                
    return fallback_title

def save_all_scenes(scenes):
    payload = {
        "version": "2.4.0",
        "totalScenes": len(scenes),
        "scenes": scenes
    }
    with open(SCENES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    js_content = f"// Dublaj Oyunu - Sahne Veritabanı (Otomatik Yenilenmiş)\nexport const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n"
    with open(SCENES_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

def main():
    print("================================================================")
    print("🚀 DUBLAJ OYUNU - TAM OTOMATİK TRANSKRİPT YENİLEME MOTORU")
    print("Model: faster-whisper-large-v3-turbo (VAD Filter + int8)")
    print("================================================================\n")

    if not os.path.exists(SCENES_JSON_PATH):
        print("Hata: scenes.json bulunamadı!")
        return

    with open(SCENES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    scenes = data.get("scenes", [])
    total_scenes = len(scenes)
    print(f"[*] Toplam sahne sayısı: {total_scenes}")

    print("[*] Whisper Turbo modeli yükleniyor...")
    t_load = time.time()
    model = WhisperModel("turbo", device="cpu", compute_type="int8")
    print(f"[+] Model RAM'e yüklendi ({time.time()-t_load:.1f}s). Başlanıyor...\n")

    updated_count = 0
    skipped_count = 0

    for idx, scene in enumerate(scenes, 1):
        scene_id = scene.get("id")
        current_title = scene.get("title", "")
        duration = scene.get("duration", 20.0)

        # 1. Korunan ilk 7 sahneyi atla
        if scene_id in PROTECTED_SCENE_IDS:
            print(f"[{idx}/{total_scenes}] 🛡️ KORUNDU: {scene_id} ({current_title})")
            skipped_count += 1
            continue

        # 2. Video dosyasını bul
        video_rel = scene.get("videoSrc", "")
        video_path = os.path.join(BASE_DIR, video_rel.replace("/", os.sep))
        if not os.path.exists(video_path):
            # Alternatif olarak orig dene
            alt_path = os.path.join(VIDEOS_DIR, f"{scene_id}_orig.mp4")
            if os.path.exists(alt_path):
                video_path = alt_path
            else:
                print(f"[{idx}/{total_scenes}] ⚠️ Video bulunamadı, atlanıyor: {video_path}")
                skipped_count += 1
                continue

        t0 = time.time()
        print(f"[{idx}/{total_scenes}] ⏳ İŞLENİYOR: {scene_id} ({duration:.1f}s)...")

        try:
            # 3. faster-whisper ile VAD ve beam_size ile transkripsiyon
            segments, info = model.transcribe(
                video_path,
                language="tr",
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
                condition_on_previous_text=False,
                temperature=0.0
            )
            
            raw_segments = list(segments)

            # 4. Segmentleri işle ve replikleri oluştur
            new_lines = []
            char_set = {}
            current_speaker_idx = 0
            prev_end = 0.0

            # Mevcut sahnede özel karakter isimleri varsa onları koru
            existing_chars = scene.get("characters", [])
            custom_char_names = {}
            if existing_chars and len(existing_chars) >= 2:
                for ci, c in enumerate(existing_chars):
                    cname = c.get("name", "")
                    if "Karakter" not in cname:
                        custom_char_names[f"karakter_{ci+1}"] = c

            for seg in raw_segments:
                text = clean_text(seg.text)
                if not text or len(text) < 2 or is_hallucination(text):
                    continue

                start = round(float(seg.start), 2)
                end = round(float(seg.end), 2)

                # Mantıksal süre güvencesi
                if end <= start:
                    end = start + 1.5
                if end - start < 0.6:
                    end = start + 1.0

                # Konuşmacı değişimi: 0.6s'den uzun duraklama veya soru işareti
                if prev_end > 0:
                    gap = start - prev_end
                    if gap >= 0.65 or text.endswith("?") or (len(new_lines) > 0 and new_lines[-1]["text"].endswith("?")):
                        current_speaker_idx = 1 if current_speaker_idx == 0 else 0

                char_id = f"karakter_{current_speaker_idx + 1}"
                
                if char_id not in char_set:
                    if char_id in custom_char_names:
                        char_set[char_id] = custom_char_names[char_id]
                    else:
                        style = CHAR_STYLES[current_speaker_idx % len(CHAR_STYLES)]
                        char_set[char_id] = {
                            "id": char_id,
                            "name": style["name"],
                            "color": style["color"],
                            "avatar": style["avatar"]
                        }

                new_lines.append({
                    "id": len(new_lines) + 1,
                    "characterId": char_id,
                    "startTime": start,
                    "endTime": end,
                    "text": text,
                    "emotion": "Meme repliği"
                })
                prev_end = end

            # Eğer hiç satır kalmadıysa güvenli fallback
            if not new_lines:
                new_lines = [{
                    "id": 1,
                    "characterId": "karakter_1",
                    "startTime": 0.5,
                    "endTime": min(duration, 4.0),
                    "text": "Meme repliği",
                    "emotion": "Komik replik"
                }]
                char_set["karakter_1"] = {
                    "id": "karakter_1",
                    "name": "Karakter 1",
                    "color": "#38bdf8",
                    "avatar": "🎤"
                }

            # 5. Yeni akıllı başlık üretimi
            new_title = smart_title_from_lines(new_lines, current_title)

            # 6. Sahne güncellemesi
            scene["title"] = new_title
            scene["characters"] = list(char_set.values())
            scene["lines"] = new_lines
            scene["difficulty"] = "Orta" if len(char_set) > 1 else "Kolay"
            scene["description"] = f"Popüler internet memesi: {new_title}"

            # 7. Anında diske yaz (kesilse bile kayıtlı kalsın)
            save_all_scenes(scenes)
            updated_count += 1

            elapsed = time.time() - t0
            print(f"[{idx}/{total_scenes}] ✅ TAMAMLANDI ({elapsed:.1f}s): {new_title} ({len(new_lines)} replik, {len(char_set)} karakter)")

        except Exception as e:
            print(f"[{idx}/{total_scenes}] ❌ HATA: {scene_id} işlenirken: {e}")

    print("\n================================================================")
    print(f"🎉 İŞLEM BAŞARIYLA TAMAMLANDI!")
    print(f"Toplam Güncellenen Sahne: {updated_count}")
    print(f"Korunan / Atlanan Sahne: {skipped_count}")
    print(f"Veritabanı: {SCENES_JSON_PATH} ve {SCENES_JS_PATH}")
    print("================================================================")

if __name__ == "__main__":
    main()
