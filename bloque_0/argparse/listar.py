#python3 listar.py .


import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Lista archivos de un directorio."
    )

    parser.add_argument(
        "directorio",
        nargs="?",
        default=".",
        help="Directorio a listar (default: actual)"
    )

    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Incluye archivos ocultos"
    )

    parser.add_argument(
        "--extension",
        help="Filtra por extensión, por ejemplo .py o .txt"
    )

    args = parser.parse_args()

    ruta = Path(args.directorio)

    if not ruta.exists():
        print(f"Error: El directorio '{args.directorio}' no existe")
        sys.exit(1)

    if not ruta.is_dir():
        print(f"Error: '{args.directorio}' no es un directorio")
        sys.exit(1)

    try:
        elementos = sorted(ruta.iterdir(), key=lambda x: x.name.lower())
    except PermissionError:
        print(f"Error: No se puede acceder a '{args.directorio}'")
        sys.exit(1)

    for elem in elementos:
        nombre = elem.name

        if not args.all and nombre.startswith("."):
            continue

        if args.extension and elem.is_file():
            if elem.suffix != args.extension:
                continue

        if args.extension and elem.is_dir():
            continue

        if elem.is_dir():
            print(f"{nombre}/")
        else:
            print(nombre)

    sys.exit(0)


if __name__ == "__main__":
    main()