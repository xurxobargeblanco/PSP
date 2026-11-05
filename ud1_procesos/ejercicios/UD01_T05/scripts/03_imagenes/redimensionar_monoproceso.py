# images_seq.py
# 27.33 segs
from PIL import Image
from pathlib import Path
import time

def resize_image(path):
    img = Image.open(path)
    img.thumbnail((300, 300))
    out = path.with_suffix(".webp")
    img.save(out, "WEBP")
    return out

def main():
    imgs = list(Path("images").glob("*.jpg"))
    t0 = time.perf_counter()
    for p in imgs:
        print("Procesando:", resize_image(p))
    print("Tiempo total (secuencial):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
