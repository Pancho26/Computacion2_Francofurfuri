import time
import random
from functools import wraps


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e
                    print(f"Intento {attempt}/{max_attempts} falló: {e}")

                    if attempt < max_attempts:
                        print(f"Esperando {delay}s...")
                        time.sleep(delay)

            # si llega acá → fallaron todos
            raise last_exception

        return wrapper
    return decorator


# ====== EJEMPLO DE USO ======

@retry(max_attempts=3, delay=1)
def conectar_servidor():
    if random.random() < 0.7:
        raise ConnectionError("Servidor no disponible")
    return "Conectado exitosamente"


if __name__ == "__main__":
    try:
        resultado = conectar_servidor()
        print(resultado)
    except ConnectionError:
        print("Falló después de 3 intentos")