import argparse
import secrets
import string
import sys

SIMBOLOS = "!@#$%&"


def generar_password(longitud, incluir_numeros=True, incluir_simbolos=True):
    caracteres = string.ascii_letters

    if incluir_numeros:
        caracteres += string.digits

    if incluir_simbolos:
        caracteres += SIMBOLOS

    if not caracteres:
        print("Error: No hay caracteres disponibles para generar la contraseña")
        sys.exit(1)

    return "".join(secrets.choice(caracteres) for _ in range(longitud))


def main():
    parser = argparse.ArgumentParser(
        description="Genera contraseñas aleatorias."
    )

    parser.add_argument(
        "-n", "--length",
        type=int,
        default=12,
        help="Longitud de la contraseña (default: 12)"
    )

    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Excluye símbolos especiales"
    )

    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="Excluye números"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Cantidad de contraseñas a generar (default: 1)"
    )

    args = parser.parse_args()

    if args.length <= 0:
        print("Error: La longitud debe ser mayor que 0")
        sys.exit(1)

    if args.count <= 0:
        print("Error: La cantidad debe ser mayor que 0")
        sys.exit(1)

    for _ in range(args.count):
        password = generar_password(
            args.length,
            incluir_numeros=not args.no_numbers,
            incluir_simbolos=not args.no_symbols
        )
        print(password)

    sys.exit(0)


if __name__ == "__main__":
    main()