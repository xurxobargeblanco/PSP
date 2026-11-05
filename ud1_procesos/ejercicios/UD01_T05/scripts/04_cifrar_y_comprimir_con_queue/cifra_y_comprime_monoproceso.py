# pipeline_single.py
# 16.89 segs
# 252.77 segs fernet 12 vueltas
import gzip
from pathlib import Path
import time
from cryptography.fernet import Fernet  # pip install cryptography

def encrypt_data(key, data: bytes) -> bytes:
    f = Fernet(key)
    enc = f.encrypt(data)
    for _ in range(10):
        enc = f.encrypt(enc)
    return f.encrypt(enc)

def compress_and_write(out_path: Path, data: bytes):
    with gzip.open(out_path, 'wb') as f:
        f.write(data)

def main():
    key = Fernet.generate_key()
    print("Clave de cifrado: ", key)
    files = list(Path("data").glob("*.txt"))
    t0 = time.perf_counter()
    for p in files:
        data = p.read_bytes()
        enc = encrypt_data(key, data)
        out = Path("out") / (p.name + ".gz")
        compress_and_write(out, enc)
        print("Procesado:", out)
    print("Tiempo total (secuencial):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
