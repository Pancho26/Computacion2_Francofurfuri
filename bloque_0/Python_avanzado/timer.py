import time


class Timer:
    def __init__(self, nombre=None):
        self.nombre = nombre
        self.inicio = None
        self.fin = None
        self.elapsed = 0

    def __enter__(self):
        self.inicio = time.time()
        self.elapsed = 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fin = time.time()
        self.elapsed = self.fin - self.inicio

        if self.nombre is not None:
            print(f"[Timer] {self.nombre}: {self.elapsed:.3f} segundos")


with Timer("Procesamiento de datos"):
    datos = [x**2 for x in range(1000000)]


with Timer() as t:
    time.sleep(0.5)

print(f"El bloque tardó {t.elapsed:.3f} segundos")


with Timer() as t:
    time.sleep(0.3)
    t.elapsed = time.time() - t.inicio
    print(f"Después del paso 1: {t.elapsed:.3f} segundos")

    time.sleep(0.2)
    t.elapsed = time.time() - t.inicio
    print(f"Después del paso 2: {t.elapsed:.3f} segundos")