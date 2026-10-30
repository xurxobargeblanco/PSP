
import multiprocessing


def incrementar(contador, lock):

    for _ in range(100):
        lock.acquire()

        contador.value = contador.value + 1

        lock.release()


if __name__ == "__main__":

    contador = multiprocessing.Value('i', 0)

    lock = multiprocessing.Lock()

    p1 = multiprocessing.Process(
        target=incrementar,
        args=(contador, lock)
    )

    p2 = multiprocessing.Process(
        target=incrementar,
        args=(contador, lock)
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Valor final do contador:", contador.value)