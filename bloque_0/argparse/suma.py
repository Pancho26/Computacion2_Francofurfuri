import sys


def main():
    total = 0.0

    for arg in sys.argv[1:]:
        try:
            total += float(arg)
        except ValueError:
            print(f"Error: '{arg}' no es un número válido")
            sys.exit(1)

    if total.is_integer():
        print(f"Suma: {int(total)}")
    else:
        print(f"Suma: {total}")

    sys.exit(0)


if __name__ == "__main__":
    main()