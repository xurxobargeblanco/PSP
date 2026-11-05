# compress_pool.py
# 1.42 segs
import gzip
import shutil
import time
from pathlib import Path
from multiprocessing import Pool, cpu_count

def compress_file(path_str):
    path = Path(path_str)
    dest = path.with_suffix(path.suffix + ".gz")
    with open(path, 'rb') as f_in, gzip.open(dest, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    return str(dest)

def main():
    files = [str(p) for p in Path("data").glob("*.csv")]
    start = time.perf_counter()
    # Ajusta processes=min(len(files), cpu_count())
    with Pool(processes=min(len(files), cpu_count())) as pool:
        for out in pool.imap_unordered(compress_file, files):
            # print("Comprimido:", out)
            pass
    print("Tiempo total (Pool):", time.perf_counter() - start)

if __name__ == "__main__":
    main()
