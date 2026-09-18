import sys
import whisper

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

video_path = sys.argv[1]
print(f"Transcribing {video_path} with medium model...")
model = whisper.load_model("base")
result = model.transcribe(video_path, language="tr")

for s in result.get("segments", []):
    print(f"[{s['start']:.2f}-{s['end']:.2f}s] {s['text'].strip()}")
