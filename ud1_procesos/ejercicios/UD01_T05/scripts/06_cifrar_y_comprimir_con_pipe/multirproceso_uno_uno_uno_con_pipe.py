# pipeline_pipe.py
from multiprocessing import Process, Pipe
from pathlib import Path
import gzip
import time

SENTINEL = b''

def reader(pipe_out, files):
    for p in files:
        data = p.read_bytes()
        pipe_out.send((p.name, data))
        print("Leído y enviado:", p.name)
    pipe_out.send((None, SENTINEL))  # indicar final
    pipe_out.close()

def xor_encrypt(data: bytes, key: int = 0x42) -> bytes:
    return bytes(b ^ key for b in data)

def cifrador(pipe_in, pipe_out):
    while True:
        name, data = pipe_in.recv()
        if name is None:
            pipe_out.send((None, SENTINEL))
            break
        enc = xor_encrypt(data)
        pipe_out.send((name, enc))
        print("Cifrado y enviado:", name)
    pipe_in.close()
    pipe_out.close()

def compresor(pipe_in, outdir: Path):
    while True:
        name, data = pipe_in.recv()
        if name is None:
            break
        out_path = outdir / (name + ".gz")
        with gzip.open(out_path, 'wb') as f:
            f.write(data)
        print("Comprimido y escrito:", out_path)
    pipe_in.close()

def main():
    files = list(Path("data").glob("*.txt"))
    Path("out").mkdir(exist_ok=True)
    t0 = time.perf_counter()
    r1, w1 = Pipe(duplex=False)  # reader -> cifrador
    r2, w2 = Pipe(duplex=False)  # cifrador -> compresor

    p_reader = Process(target=reader, args=(w1, files))
    p_cifrador = Process(target=cifrador, args=(r1, w2))
    p_compresor = Process(target=compresor, args=(r2, Path("out")))

    p_reader.start(); p_cifrador.start(); p_compresor.start()
    p_reader.join(); p_cifrador.join(); p_compresor.join()
    print("Tiempo total (pipeline Pipe):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
