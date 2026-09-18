import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import whisper

vocals_path = "assets/temp_test/vocals.wav"
print("Transcribing separated vocals with Whisper...")
t0 = time.time()
whisper_model = whisper.load_model("base")
transcription = whisper_model.transcribe(vocals_path, language="tr")
print(f"Transcription done in {time.time()-t0:.2f}s:")
for s in transcription.get("segments", []):
    print(f"  [{s['start']:.2f}s - {s['end']:.2f}s]: {s['text']}")
