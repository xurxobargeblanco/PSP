# audio_pool.py
# 12 segs
from pydub import AudioSegment
from pathlib import Path
from multiprocessing import Pool, cpu_count
import time

def normalize_and_export(path_str):
    path = Path(path_str)
    audio = AudioSegment.from_wav(path)
    normalized = audio.normalize()
    out = path.with_suffix(".mp3")
    normalized.export(out, format="mp3")
    return str(out)

def main():
    files = [str(p) for p in Path("audios").glob("*.wav")]
    t0 = time.perf_counter()
    with Pool(processes=min(len(files), cpu_count())) as pool:
        for out in pool.imap_unordered(normalize_and_export, files):
            print("Procesado:", out)
    print("Tiempo total (Pool):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
