# images_pool.py
# 2.73 segs
from PIL import Image
from pathlib import Path
from multiprocessing import Pool, cpu_count
import time

def resize_image(path_str):
    path = Path(path_str)
    img = Image.open(path)
    img.thumbnail((300, 300))
    out = path.with_suffix(".webp")
    img.save(out, "WEBP")
    return str(out)

def main():
    imgs = [str(p) for p in Path("images").glob("*.jpg")]
    t0 = time.perf_counter()
    with Pool(processes=min(len(imgs), cpu_count())) as pool:
        for out in pool.imap_unordered(resize_image, imgs):
            print("Guardado:", out)
    print("Tiempo total (Pool):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
