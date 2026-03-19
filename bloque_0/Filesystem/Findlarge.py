#python3 Findlarge.py /var/log --min-size 1M --type f

import os
import sys
import argparse


def parsear_tamano(texto):
    texto = texto.strip().upper()

    if texto[-1] in ["K", "M", "G"]:
        numero = float(texto[:-1])
        sufijo = texto[-1]

        if sufijo == "K":
            return int(numero * 1024)
        elif sufijo == "M":
            return int(numero * 1024 * 1024)
        elif sufijo == "G":
            return int(numero * 1024 * 1024 * 1024)
    else:
        return int(texto)


def tamano_legible(bytes_):
    if bytes_ >= 1024 * 1024 * 1024:
        return f"{bytes_ / (1024 * 1024 * 1024):.1f} GB"
    elif bytes_ >= 1024 * 1024:
        return f"{bytes_ / (1024 * 1024):.1f} MB"
    elif bytes_ >= 1024:
        return f"{bytes_ / 1024:.1f} KB"
    else:
        return f"{bytes_} B"


def obtener_tamano_directorio(ruta):
    total = 0
    for raiz, dirs, archivos in os.walk(ruta):
        for nombre in archivos:
            ruta_archivo = os.path.join(raiz, nombre)
            try:
                total += os.path.getsize(ruta_archivo)
            except OSError:
                pass
    return total


def buscar_elementos(directorio, min_size, tipo):
    resultados = []

    for raiz, dirs, archivos in os.walk(directorio):
        if tipo in [None, "f"]:
            for nombre in archivos:
                ruta = os.path.join(raiz, nombre)
                try:
                    tam = os.path.getsize(ruta)
                    if tam >= min_size:
                        resultados.append((ruta, tam))
                except OSError:
                    pass

        if tipo in [None, "d"]:
            for nombre in dirs:
                ruta = os.path.join(raiz, nombre)
                try:
                    tam = obtener_tamano_directorio(ruta)
                    if tam >= min_size:
                        resultados.append((ruta, tam))
                except OSError:
                    pass

    return resultados


def main():
    parser = argparse.ArgumentParser(description="Busca archivos o directorios grandes.")
    parser.add_argument("directorio", help="Directorio donde buscar")
    parser.add_argument("--min-size", default="0", help="Tamaño mínimo: por ejemplo 100K, 2M, 1G")
    parser.add_argument("--type", choices=["f", "d"], help="f = archivos, d = directorios")
    parser.add_argument("--top", type=int, help="Mostrar solo los N más grandes")

    args = parser.parse_args()

    if not os.path.isdir(args.directorio):
        print(f"Error: '{args.directorio}' no es un directorio válido.")
        sys.exit(1)

    try:
        min_size = parsear_tamano(args.min_size)
    except ValueError:
        print("Error: tamaño inválido en --min-size. Usá valores como 100K, 2M o 1G.")
        sys.exit(1)

    resultados = buscar_elementos(args.directorio, min_size, args.type)

    resultados.sort(key=lambda x: x[1], reverse=True)

    if args.top:
        resultados = resultados[:args.top]
        print(f"Los {len(resultados)} elementos más grandes:")

    total_archivos = len(resultados)
    total_bytes = sum(tam for _, tam in resultados)

    for i, (ruta, tam) in enumerate(resultados, start=1):
        if args.top:
            print(f"{i}. {ruta} ({tamano_legible(tam)})")
        else:
            print(f"{ruta} ({tamano_legible(tam)})")

    print(f"Total: {total_archivos} elementos, {tamano_legible(total_bytes)}")


if __name__ == "__main__":
    main()