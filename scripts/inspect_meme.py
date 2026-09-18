import os
import sys
import whisper

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

video_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\mirac\Desktop\meme\1359f68984edc9274e4439be217a2647.mp4"
model = whisper.load_model("base")
res = model.transcribe(video_path, language="tr")

print(f"FILE: {os.path.basename(video_path)}")
print(f"FULL TEXT: {res.get('text', '').strip()}")
for s in res.get("segments", []):
    start = s['start']
    end = s['end']
    text = s['text'].strip()
    print(f"  [{start:.2f}s - {end:.2f}s]: {text}")
