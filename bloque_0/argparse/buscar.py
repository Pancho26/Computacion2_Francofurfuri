#python3 buscar.py import buscar.py

#hola .

import argparse
import sys
from pathlib import Path


def coincide(linea, patron, ignore_case=False):
    if ignore_case:
        return patron.lower() in linea.lower()
    return patron in linea


def procesar_lineas(lineas, patron, mostrar_numero, invertir, contar, prefijo=None, ignore_case=False):
    coincidencias = 0
    salida = []

    for numero, linea in enumerate(lineas, start=1):
        linea = linea.rstrip("\n")
        match = coincide(linea, patron, ignore_case)

        if invertir:
            match = not match

        if match:
            coincidencias += 1
            if not contar:
                partes = []

                if prefijo:
                    partes.append(prefijo)

                if mostrar_numero:
                    partes.append(str(numero))

                if partes:
                    salida.append(":".join(partes) + f": {linea}")
                else:
                    salida.append(linea)

    return coincidencias, salida


def leer_archivo(nombre):
    try:
        with open(nombre, "r", encoding="utf-8") as archivo:
            return archivo.readlines()
    except FileNotFoundError:
        print(f"Error: No se pudo leer '{nombre}'", file=sys.stderr)
        return None
    except PermissionError:
        print(f"Error: No se pudo leer '{nombre}'", file=sys.stderr)
        return None
    except OSError:
        print(f"Error: No se pudo leer '{nombre}'", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Busca un patrón en archivos o en la entrada estándar."
    )

    parser.add_argument(
        "patron",
        help="Patrón a buscar"
    )

    parser.add_argument(
        "archivos",
        nargs="*",
        help="Archivos donde buscar"
    )

    parser.add_argument(
        "-i", "--ignore-case",
        action="store_true",
        help="Ignora mayúsculas y minúsculas"
    )

    parser.add_argument(
        "-n", "--line-number",
        action="store_true",
        help="Muestra número de línea"
    )

    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="Muestra solo la cantidad de coincidencias"
    )

    parser.add_argument(
        "-v", "--invert",
        action="store_true",
        help="Muestra líneas que no coinciden"
    )

    args = parser.parse_args()

    total = 0
    hubo_error = False

    # Caso 1: hay archivos
    if args.archivos:
        multiples_archivos = len(args.archivos) > 1
        mostrar_numero = args.line_number or multiples_archivos

        for nombre in args.archivos:
            lineas = leer_archivo(nombre)
            if lineas is None:
                hubo_error = True
                continue

            coincidencias, salida = procesar_lineas(
                lineas=lineas,
                patron=args.patron,
                mostrar_numero=mostrar_numero,
                invertir=args.invert,
                contar=args.count,
                prefijo=nombre if multiples_archivos or not args.count else nombre,
                ignore_case=args.ignore_case
            )

            total += coincidencias

            if args.count:
                if multiples_archivos:
                    print(f"{nombre}: {coincidencias} coincidencias")
                else:
                    print(f"{coincidencias} coincidencias")
            else:
                for linea in salida:
                    print(linea)

        if args.count and len(args.archivos) > 1:
            print(f"Total: {total} coincidencias")

        sys.exit(1 if hubo_error else 0)

    # Caso 2: no hay archivos, leer stdin
    if not sys.stdin.isatty():
        lineas = sys.stdin.readlines()
        coincidencias, salida = procesar_lineas(
            lineas=lineas,
            patron=args.patron,
            mostrar_numero=args.line_number,
            invertir=args.invert,
            contar=args.count,
            prefijo=None,
            ignore_case=args.ignore_case
        )

        if args.count:
            print(f"{coincidencias} coincidencias")
        else:
            for linea in salida:
                print(linea)

        sys.exit(0)

    # Caso 3: no hay archivos ni stdin
    print("Error: Debe especificar al menos un archivo o usar entrada estándar", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()