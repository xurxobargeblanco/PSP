import gzip
import time
from cryptography.fernet import Fernet
from pathlib import Path

# 135.25 s

# Genera una clave Fernet (en práctica, debería guardarse y compartirse)
key = Fernet.generate_key()
fernet = Fernet(key)

# Directorio con ficheros de entrada
INPUT_DIR = Path("data")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

def process_file(path):
    """Lee, cifra 10 veces y comprime un fichero"""
    with open(path, "rb") as f:
        data = f.read()
    # CPU-bound: 10 vueltas de cifrado
    for _ in range(10):
        data = fernet.encrypt(data)
    # I/O-bound: compresión + escritura
    compressed = gzip.compress(data)
    out_path = OUTPUT_DIR / f"{path.stem}.gz"
    with open(out_path, "wb") as f:
        f.write(compressed)

if __name__ == "__main__":
    files = list(INPUT_DIR.glob("*.txt"))
    t0 = time.perf_counter()
    for f in files:
        process_file(f)
    t1 = time.perf_counter()
    print(f"Procesados {len(files)} ficheros en {t1 - t0:.2f} s (monoproceso)")
