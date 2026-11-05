# audio_seq.py
# Requiere: pip install pydub  y ffmpeg en PATH
#57 segs
#29 segs sin ahorro de energía
from pydub import AudioSegment
from pathlib import Path
import time

def normalize_and_export(path: Path):
    audio = AudioSegment.from_wav(path)
    normalized = audio.normalize()
    out = path.with_suffix(".mp3")
    normalized.export(out, format="mp3")
    return out

def main():
    files = list(Path("audios").glob("*.wav"))
    t0 = time.perf_counter()
    for f in files:
        out = normalize_and_export(f)
        print("Procesado:", out)
    print("Tiempo total (secuencial):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
