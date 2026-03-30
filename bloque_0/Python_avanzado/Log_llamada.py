from functools import wraps
from datetime import datetime

def log_llamada(func):
    @wraps(func)
    def envoltura(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        argumentos = []

        for arg in args:
            argumentos.append(repr(arg))

        for clave, valor in kwargs.items():
            argumentos.append(f"{clave}={repr(valor)}")

        argumentos_texto = ", ".join(argumentos)

        print(f"[{timestamp}] Llamando a {func.__name__}({argumentos_texto})")

        resultado = func(*args, **kwargs)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {func.__name__} retornó {repr(resultado)}")

        return resultado

    return envoltura


@log_llamada
def sumar(a, b):
    return a + b


@log_llamada
def saludar(nombre, entusiasta=False):
    sufijo = "!" if entusiasta else "."
    return f"Hola, {nombre}{sufijo}"


resultado = sumar(3, 5)
saludar("Ana", entusiasta=True)