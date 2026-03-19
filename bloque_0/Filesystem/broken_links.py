#!/usr/bin/env python3

import os
import sys
import argparse


def buscar_enlaces_rotos(directorio):
    enlaces_rotos = []

    for raiz, dirs, archivos in os.walk(directorio):
        elementos = dirs + archivos

        for nombre in elementos:
            ruta = os.path.join(raiz, nombre)

            if os.path.islink(ruta) and not os.path.exists(ruta):
                enlaces_rotos.append(ruta)

    return enlaces_rotos


def main():
    parser = argparse.ArgumentParser(description="Detecta enlaces simbólicos rotos.")
    parser.add_argument("directorio", help="Directorio donde buscar")
    parser.add_argument("--delete", action="store_true", help="Ofrecer borrar enlaces rotos")
    parser.add_argument("--quiet", action="store_true", help="Mostrar solo el conteo")

    args = parser.parse_args()

    if not os.path.isdir(args.directorio):
        print(f"Error: '{args.directorio}' no es un directorio válido.")
        sys.exit(1)

    enlaces_rotos = buscar_enlaces_rotos(args.directorio)

    if args.quiet:
        print(len(enlaces_rotos))
        return

    print(f"Buscando enlaces simbólicos rotos en {args.directorio}...\n")

    if enlaces_rotos:
        print("Enlaces rotos encontrados:\n")

        for ruta in enlaces_rotos:
            try:
                destino = os.readlink(ruta)
            except OSError:
                destino = "destino desconocido"

            print(f"{ruta} -> {destino} (no existe)")

        print(f"\nTotal: {len(enlaces_rotos)} enlaces rotos")

        if args.delete:
            for ruta in enlaces_rotos:
                respuesta = input(f"¿Querés borrar '{ruta}'? [s/N]: ").strip().lower()

                if respuesta == "s":
                    try:
                        os.remove(ruta)
                        print("Borrado.")
                    except OSError as e:
                        print(f"No se pudo borrar: {e}")
                else:
                    print("Saltado.")
    else:
        print("No se encontraron enlaces simbólicos rotos.")


if __name__ == "__main__":
    main()