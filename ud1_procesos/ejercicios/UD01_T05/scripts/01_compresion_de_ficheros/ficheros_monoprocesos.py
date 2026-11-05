# compress_sequential.py
# Versión secuencial: procesa ficheros uno a uno.
# 1.43 segs

import gzip
import shutil
import time
from pathlib import Path

def compress_file(path: Path):
    dest = path.with_suffix(path.suffix + ".gz")
    with open(path, 'rb') as f_in, gzip.open(dest, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    return dest

def main():
    files = list(Path("data").glob("*.csv"))
    start = time.perf_counter()
    for f in files:
        out = compress_file(f)
        # print("Comprimido:", out)
    print("Tiempo total (secuencial):", time.perf_counter() - start)

if __name__ == "__main__":
    main()
