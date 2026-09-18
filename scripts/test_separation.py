import os
import sys
import time
import torch
import torchaudio
from demucs.api import Separator, save_audio
import whisper

input_video = r"C:\Users\mirac\Desktop\meme\0481ae9ebf5debac67e9f1d7277b53ff.mp4"
temp_dir = r"C:\Users\mirac\Documents\MiracOS\🏰 300-Projects\Dublaj-Oyunu\assets\temp_test"
os.makedirs(temp_dir, exist_ok=True)

print("1. Extracting audio from video...")
t0 = time.time()
temp_audio = os.path.join(temp_dir, "original_audio.wav")
os.system(f'ffmpeg -y -i "{input_video}" -vn -ar 44100 -ac 2 "{temp_audio}" >nul 2>&1')
print(f"Audio extracted in {time.time()-t0:.2f}s")

print("2. Running Demucs stem separation (htdemucs)...")
t1 = time.time()
separator = Separator(model="htdemucs", device="cpu", segment=7)
origin, separated = separator.separate_audio_file(temp_audio)
print(f"Separated stems: {list(separated.keys())} in {time.time()-t1:.2f}s")

print("3. Saving instrumental and vocals...")
vocals = separated["vocals"]
instrumental = separated["drums"] + separated["bass"] + separated["other"]

inst_path = os.path.join(temp_dir, "instrumental.wav")
vocals_path = os.path.join(temp_dir, "vocals.wav")
save_audio(instrumental, inst_path, samplerate=separator.samplerate)
save_audio(vocals, vocals_path, samplerate=separator.samplerate)
print(f"Saved instrumental to {inst_path}")
print(f"Saved vocals to {vocals_path}")

print("4. Transcribing vocals with Whisper...")
t2 = time.time()
whisper_model = whisper.load_model("base")
transcription = whisper_model.transcribe(vocals_path, language="tr")
print(f"Transcription completed in {time.time()-t2:.2f}s")
print("Transcribed lines:")
for s in transcription.get("segments", []):
    print(f"  [{s['start']:.1f}s - {s['end']:.1f}s]: {s['text']}")
