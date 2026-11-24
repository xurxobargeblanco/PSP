
import threading

class Factorial(threading.Thread):

    def __init__(self, n):
        super().__init__()
        self.n = n


