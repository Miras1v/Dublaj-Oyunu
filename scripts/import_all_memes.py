#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Dublaj Oyunu - Toplu Meme İçe Aktarıcı & Yapay Zeka Stem Ayrıştırıcı (Demucs + Whisper)
Tüm masaüstündeki meme klasörünü tarar:
- Zaten eklenenleri atlar.
- Her video için Demucs ile Müzik/Vokal ayrıştırır.
- Temiz dublaj videosunu (_clean.mp4) ve orijinal videoyu (_orig.mp4) assets/videos/ klasörüne yazar.
- Whisper ile replikleri ve zaman kodlarını çıkarır.
- Başlığı ve karakterleri akıllıca belirleyip data/scenes.json ve js/scenes.js dosyalarını günceller.
- Her videodan sonra anında diske kaydeder (kesilse bile kaldığı yerden devam edebilir).
"""

import os
import sys
import time
import json
import glob
import subprocess
import shutil
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import torch
from demucs.api import Separator, save_audio
import whisper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_VIDEOS_DIR = os.path.join(BASE_DIR, "assets", "videos")
SCENES_JSON_PATH = os.path.join(BASE_DIR, "data", "scenes.json")
SCENES_JS_PATH = os.path.join(BASE_DIR, "js", "scenes.js")
TEMP_DIR = os.path.join(BASE_DIR, "assets", "temp_batch")
MEME_FOLDER = r"C:\Users\mirac\Desktop\meme"

os.makedirs(ASSETS_VIDEOS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

CHAR_STYLES = [
    {"name": "Karakter 1", "avatar": "🎤", "color": "#38bdf8"},
    {"name": "Karakter 2", "avatar": "🎭", "color": "#fbbf24"},
    {"name": "Karakter 3", "avatar": "🔥", "color": "#f87171"},
    {"name": "Karakter 4", "avatar": "😎", "color": "#a855f7"},
]

def load_existing_scene_ids():
    if not os.path.exists(SCENES_JSON_PATH):
        return set()
    try:
        with open(SCENES_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(s.get("id") for s in data.get("scenes", []))
    except Exception:
        return set()

def get_video_duration(video_path):
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
        out = subprocess.check_output(cmd).decode().strip()
        return round(float(out), 2)
    except Exception:
        return 20.0

def generate_title_from_text(segments, fallback_name):
    for s in segments:
        text = s.get("text", "").strip()
        # Temizle
        cleaned = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ]', '', text).strip()
        words = cleaned.split()
        if len(words) >= 2:
            title_candidate = " ".join(words[:5]).capitalize()
            if len(title_candidate) >= 6:
                return f"Meme - {title_candidate}"
    return f"Meme - {fallback_name[:12]}"

def save_scene(scene_data):
    scenes = []
    if os.path.exists(SCENES_JSON_PATH):
        try:
            with open(SCENES_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                scenes = data.get("scenes", [])
        except Exception:
            scenes = []

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

    js_content = f"// Dublaj Oyunu - Sahne Veritabanı\nexport const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n"
    with open(SCENES_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

def main():
    if not os.path.exists(MEME_FOLDER):
        print(f"Hata: Klasör bulunamadı: {MEME_FOLDER}")
        return

    all_files = sorted(glob.glob(os.path.join(MEME_FOLDER, "*.mp4")))
    print(f"Toplam {len(all_files)} adet meme videosu bulundu.")

    existing_ids = load_existing_scene_ids()
    print(f"Mevcut kayıtlı sahne sayısı: {len(existing_ids)}")

    # İşlenecekleri filtrele
    to_process = []
    for f in all_files:
        base_name = os.path.splitext(os.path.basename(f))[0]
        # Bilinen veya id tabanlı eşleşme kontrolü
        candidate_id_1 = f"meme-{base_name}"
        if candidate_id_1 in existing_ids:
            continue
        # Kolpacino ve Sonuc Ne kontrolleri
        if "0481ae9ebf5debac67e9f1d7277b53ff" in base_name and "meme-kolpacino-saatli-bomba" in existing_ids:
            continue
        if "1359f68984edc9274e4439be217a2647" in base_name and "meme-sonuc-ne-soru-cevap" in existing_ids:
            continue
        to_process.append(f)

    print(f"İşlenecek yeni meme sayısı: {len(to_process)}")
    if not to_process:
        print("İşlenecek yeni video kalmadı, hepsi zaten eklenmiş!")
        return

    print("\n[+] Yapay Zeka Modelleri RAM'e yükleniyor (Demucs + Whisper)...")
    sep_start = time.time()
    separator = Separator(model="htdemucs", device="cpu", segment=7)
    whisper_model = whisper.load_model("base")
    print(f"[+] Modeller {time.time()-sep_start:.1f}s içinde yüklendi. İşlem başlıyor...\n")

    success_count = 0

    for idx, video_file in enumerate(to_process, 1):
        filename = os.path.basename(video_file)
        base_id = os.path.splitext(filename)[0]
        scene_id = f"meme-{base_id[:16]}"

        print(f"\n=======================================================")
        print(f"[{idx}/{len(to_process)}] İŞLENİYOR: {filename}")
        print(f"=======================================================")

        item_start = time.time()
        duration = get_video_duration(video_file)
        print(f"[*] Süre: {duration}s")

        temp_audio = os.path.join(TEMP_DIR, f"{base_id}_orig.wav")
        inst_wav = os.path.join(TEMP_DIR, f"{base_id}_inst.wav")
        vocals_wav = os.path.join(TEMP_DIR, f"{base_id}_vocals.wav")

        try:
            # 1. Ses Çıkar
            subprocess.run([
                "ffmpeg", "-y", "-i", video_file, "-vn", "-ar", "44100", "-ac", "2", temp_audio
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # 2. Demucs ile Ayrıştırma
            t_dem = time.time()
            _, separated = separator.separate_audio_file(temp_audio)
            vocals = separated["vocals"]
            instrumental = separated["drums"] + separated["bass"] + separated["other"]

            save_audio(instrumental, inst_wav, samplerate=separator.samplerate)
            save_audio(vocals, vocals_wav, samplerate=separator.samplerate)
            print(f"[*] Demucs ayrıştırma: {time.time()-t_dem:.1f}s")

            # 3. Clean Video Remux ve Orig Video Kopyalama
            clean_filename = f"{scene_id}_clean.mp4"
            orig_filename = f"{scene_id}_orig.mp4"
            clean_path = os.path.join(ASSETS_VIDEOS_DIR, clean_filename)
            orig_path = os.path.join(ASSETS_VIDEOS_DIR, orig_filename)

            shutil.copyfile(video_file, orig_path)

            subprocess.run([
                "ffmpeg", "-y", "-i", video_file, "-i", inst_wav,
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-map", "0:v:0", "-map", "1:a:0", clean_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # 4. Whisper Transkript
            t_whi = time.time()
            res = whisper_model.transcribe(vocals_wav, language="tr")
            segments = res.get("segments", [])
            print(f"[*] Whisper transkript: {len(segments)} parça ({time.time()-t_whi:.1f}s)")

            # 5. Konuşmacı Ayrımı & Replik Formatlama
            lines = []
            char_set = {}
            current_speaker_idx = 0

            for seg_i, seg in enumerate(segments):
                text = seg.get("text", "").strip()
                if not text or len(text) < 2:
                    continue
                start = round(float(seg.get("start", 0)), 2)
                end = round(float(seg.get("end", start + 2.0)), 2)
                if end <= start:
                    end = start + 2.0

                # Konuşmacı dönüş mantığı: boşluk >= 0.7s veya soru/ünlem
                if seg_i > 0:
                    prev_seg = segments[seg_i - 1]
                    prev_end = float(prev_seg.get("end", 0))
                    prev_text = prev_seg.get("text", "").strip()
                    if (start - prev_end >= 0.7) or prev_text.endswith("?") or text.endswith("?"):
                        current_speaker_idx = 1 if current_speaker_idx == 0 else 0

                char_id = f"karakter_{current_speaker_idx + 1}"
                if char_id not in char_set:
                    style = CHAR_STYLES[current_speaker_idx % len(CHAR_STYLES)]
                    char_set[char_id] = {
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

            if not lines:
                lines = [{
                    "id": 1,
                    "characterId": "karakter_1",
                    "startTime": 0.5,
                    "endTime": min(duration, 5.0),
                    "text": "Meme repliği",
                    "emotion": "Komik replik"
                }]
                char_set["karakter_1"] = {
                    "id": "karakter_1",
                    "name": "Karakter 1",
                    "color": "#38bdf8",
                    "avatar": "🎤"
                }

            # 6. Başlık ve Açıklama Üretimi
            title = generate_title_from_text(segments, base_id)
            characters_list = list(char_set.values())

            scene_entry = {
                "id": scene_id,
                "title": title,
                "category": "meme",
                "categoryName": "Türk Meme Kültürü",
                "duration": duration,
                "videoSrc": f"assets/videos/{orig_filename}",
                "cleanVideoSrc": f"assets/videos/{clean_filename}",
                "difficulty": "Orta" if len(characters_list) > 1 else "Kolay",
                "description": f"Popüler internet memesi: {title}",
                "characters": characters_list,
                "lines": lines
            }

            # Anında veritabanına kaydet
            save_scene(scene_entry)
            success_count += 1
            print(f"[✅ TAMAMLANDI] '{title}' ({len(lines)} replik, {len(characters_list)} karakter) - Toplam: {time.time()-item_start:.1f}s")

        except Exception as e:
            print(f"[❌ HATA] {filename} işlenirken hata oluştu: {e}")

        finally:
            # Geçici dosyaları anında temizle
            for p in [temp_audio, inst_wav, vocals_wav]:
                if os.path.exists(p):
                    try: os.remove(p)
                    except Exception: pass

    print(f"\n=======================================================")
    print(f"[+] TOPLU İŞLEM TAMAMLANDI! {success_count} yeni meme başarıyla oyuna eklendi.")
    print(f"=======================================================")
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

if __name__ == "__main__":
    main()
