#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dublaj Oyunu - Otomatik Meme İçe Aktarıcı & Ses/Müzik Ayrıştırıcı (Demucs + Whisper)
1. Masaüstündeki memeyi okur.
2. Demucs yapay zekasıyla Vokal (İnsan Sesi) ve Enstrümantal (Müzik + Efektler) olarak ikiye böler.
3. Arka plan müziğini koruyarak temiz dublaj videosunu (_clean.mp4) ve orijinal videoyu (_orig.mp4) assets/videos/ klasörüne atar.
4. Temiz vokal kanalından Whisper ile replikleri ve tam saniye aralıklarını çıkarır.
5. Konuşmacı dönüşlerini otomatik tespit edip Karakter 1 ve Karakter 2 olarak sahneler veritabanına ekler.
"""

import os
import sys
import time
import json
import glob
import subprocess
import shutil

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import torch
from demucs.api import Separator, save_audio
import whisper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_VIDEOS_DIR = os.path.join(BASE_DIR, "assets", "videos")
SCENES_JSON_PATH = os.path.join(BASE_DIR, "data", "scenes.json")
SCENES_JS_PATH = os.path.join(BASE_DIR, "js", "scenes.js")
TEMP_DIR = os.path.join(BASE_DIR, "assets", "temp_processing")

os.makedirs(ASSETS_VIDEOS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Karakter Renk ve Avatar Şablonları
CHAR_STYLES = [
    {"name": "Karakter 1", "avatar": "🎤", "color": "#38bdf8"},
    {"name": "Karakter 2", "avatar": "🎭", "color": "#fbbf24"},
    {"name": "Karakter 3", "avatar": "🔥", "color": "#f87171"},
    {"name": "Karakter 4", "avatar": "😎", "color": "#a855f7"},
]

def get_video_duration(video_path):
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
        out = subprocess.check_output(cmd).decode().strip()
        return round(float(out), 2)
    except Exception:
        return 20.0

def process_single_meme(video_file, scene_id, title, desc="", separator=None, whisper_model=None):
    print(f"\n=======================================================")
    print(f"[+] İşleniyor: {os.path.basename(video_file)} -> {scene_id}")
    print(f"=======================================================")

    duration = get_video_duration(video_file)
    print(f"[*] Video Süresi: {duration}s")

    # 1. Ses Çıkar
    t0 = time.time()
    orig_wav = os.path.join(TEMP_DIR, f"{scene_id}_audio.wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_file, "-vn", "-ar", "44100", "-ac", "2", orig_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[1/5] Orijinal ses çıkarıldı ({time.time()-t0:.1f}s)")

    # 2. Demucs ile Ses & Müzik Ayrıştırma
    t1 = time.time()
    print("[2/5] Demucs (HTDemucs) ile Vokal ve Müzik ayrıştırılıyor...")
    if separator is None:
        separator = Separator(model="htdemucs", device="cpu", segment=7)
    
    _, separated = separator.separate_audio_file(orig_wav)
    vocals = separated["vocals"]
    instrumental = separated["drums"] + separated["bass"] + separated["other"]

    inst_wav = os.path.join(TEMP_DIR, f"{scene_id}_inst.wav")
    vocals_wav = os.path.join(TEMP_DIR, f"{scene_id}_vocals.wav")
    save_audio(instrumental, inst_wav, samplerate=separator.samplerate)
    save_audio(vocals, vocals_wav, samplerate=separator.samplerate)
    print(f"[2/5] Ayrıştırma tamamlandı! ({time.time()-t1:.1f}s)")

    # 3. Temiz Video ve Orijinal Video Hazırla
    t2 = time.time()
    print("[3/5] Temiz Dublaj Videosu remux ediliyor...")
    clean_video_filename = f"{scene_id}_clean.mp4"
    orig_video_filename = f"{scene_id}_orig.mp4"
    clean_video_path = os.path.join(ASSETS_VIDEOS_DIR, clean_video_filename)
    orig_video_path = os.path.join(ASSETS_VIDEOS_DIR, orig_video_filename)

    # Orijinal videoyu kopyala
    shutil.copyfile(video_file, orig_video_path)

    # Temiz enstrümantal sesli videoyu remux et
    subprocess.run([
        "ffmpeg", "-y", "-i", video_file, "-i", inst_wav,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0", clean_video_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[3/5] Temiz video oluşturuldu: {clean_video_filename} ({time.time()-t2:.1f}s)")

    # 4. Temiz Vokalleri Whisper ile Transkribe Et
    t3 = time.time()
    print("[4/5] Whisper ile replikler ve zaman kodları çıkarılıyor...")
    if whisper_model is None:
        whisper_model = whisper.load_model("base")
    
    trans_res = whisper_model.transcribe(vocals_wav, language="tr")
    raw_segments = trans_res.get("segments", [])
    print(f"[4/5] Whisper tamamlandı: {len(raw_segments)} replik bulundu ({time.time()-t3:.1f}s)")

    # 5. Konuşmacı Tespiti ve Replik Kümeleme
    lines = []
    characters_used = {}
    current_speaker_idx = 0

    for i, seg in enumerate(raw_segments):
        text = seg.get("text", "").strip()
        if not text or len(text) < 2:
            continue
        
        start = round(float(seg.get("start", 0)), 2)
        end = round(float(seg.get("end", start + 2.0)), 2)
        if end <= start:
            end = start + 2.0

        # Eğer önceki replikle arasında 0.8 saniyeden fazla boşluk varsa veya soru/ünlem varsa konuşmacı değişimi ihtimali
        if i > 0:
            prev_seg = raw_segments[i-1]
            prev_end = float(prev_seg.get("end", 0))
            prev_text = prev_seg.get("text", "").strip()
            
            # Konuşma sırası mantığı: Soru işareti veya 0.7s sessizlik varsa konuşmacı değiş
            if (start - prev_end >= 0.7) or prev_text.endswith("?") or text.endswith("?"):
                current_speaker_idx = 1 if current_speaker_idx == 0 else 0

        char_id = f"karakter_{current_speaker_idx + 1}"
        if char_id not in characters_used:
            style = CHAR_STYLES[current_speaker_idx % len(CHAR_STYLES)]
            characters_used[char_id] = {
                "id": char_id,
                "name": style["name"],
                "color": style["color"],
                "avatar": style["avatar"]
            }

        lines.append({
            "id": len(lines) + 1,
            "characterId": char_id,
            "startTime": start,
            "endTime": end,
            "text": text,
            "emotion": "Meme repliği"
        })

    # Eğer sadece 1 replik varsa veya tek konuşmacı çıktıysa
    if not lines:
        lines = [{
            "id": 1,
            "characterId": "karakter_1",
            "startTime": 0.5,
            "endTime": min(duration, 5.0),
            "text": "Meme repliği burada başlar!",
            "emotion": "Komik replik"
        }]
        characters_used["karakter_1"] = {
            "id": "karakter_1",
            "name": "Karakter 1",
            "color": "#38bdf8",
            "avatar": "🎤"
        }

    characters_list = list(characters_used.values())

    scene_data = {
        "id": scene_id,
        "title": title,
        "category": "meme",
        "categoryName": "Türk Meme Kültürü",
        "duration": duration,
        "videoSrc": f"assets/videos/{orig_video_filename}",
        "cleanVideoSrc": f"assets/videos/{clean_video_filename}",
        "difficulty": "Orta" if len(characters_list) > 1 else "Kolay",
        "description": desc or f"Meme: {title}",
        "characters": characters_list,
        "lines": lines
    }

    # 6. scenes.json ve scenes.js Güncelle
    save_scene_to_db(scene_data)
    print(f"[+] BAŞARILI! '{title}' sahnesi veritabanına eklendi.")
    return scene_data

def save_scene_to_db(scene_data):
    # scenes.json oku ve güncelle
    scenes = []
    if os.path.exists(SCENES_JSON_PATH):
        try:
            with open(SCENES_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                scenes = data.get("scenes", [])
        except Exception:
            scenes = []

    # Varsa güncelle, yoksa ekle
    existing_idx = next((i for i, s in enumerate(scenes) if s.get("id") == scene_data["id"]), None)
    if existing_idx is not None:
        scenes[existing_idx] = scene_data
    else:
        scenes.append(scene_data)

    payload = {
        "version": "2.3.0",
        "totalScenes": len(scenes),
        "scenes": scenes
    }
    with open(SCENES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # scenes.js dosyasına da senkronize et
    js_content = f"// Dublaj Oyunu - Sahne Veritabanı\nexport const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n"
    with open(SCENES_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

if __name__ == "__main__":
    meme_folder = r"C:\Users\mirac\Desktop\meme"
    if not os.path.exists(meme_folder):
        print(f"Hata: Meme klasörü bulunamadı: {meme_folder}")
        sys.exit(1)

    print("Yapay zeka modelleri yükleniyor (Demucs + Whisper)...")
    sep = Separator(model="htdemucs", device="cpu", segment=7)
    whisp = whisper.load_model("base")

    # Test olarak iki bilinen meme dosyasını aktar
    known_memes = [
        {
            "file": os.path.join(meme_folder, "0481ae9ebf5debac67e9f1d7277b53ff.mp4"),
            "id": "meme-kolpacino-saatli-bomba",
            "title": "Kolpaçino - Saatli Bomba",
            "desc": "Ganyotçu ile Sabri'nin efsanevi saatli bomba sahnesi!"
        },
        {
            "file": os.path.join(meme_folder, "1359f68984edc9274e4439be217a2647.mp4"),
            "id": "meme-sonuc-ne-soru-cevap",
            "title": "Röportaj - Soruya Soruyla Cevap Verme!",
            "desc": "Ee sonuç ne? Sana soruyorum! Ben sana soruyorum!"
        }
    ]

    for m in known_memes:
        if os.path.exists(m["file"]):
            process_single_meme(m["file"], m["id"], m["title"], m["desc"], separator=sep, whisper_model=whisp)

    print("\n[+] Tüm işlemler tamamlandı! Geçici dosyalar temizleniyor...")
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
