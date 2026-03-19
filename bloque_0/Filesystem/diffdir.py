#python3 diffdir.py dir1 dir2

import os
import sys


def listar_archivos(directorio):
    return set(os.listdir(directorio))


def info_archivo(ruta):
    try:
        stat = os.stat(ruta)
        return stat.st_size, stat.st_mtime
    except OSError:
        return None, None


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 diffdir.py <dir1> <dir2>")
        sys.exit(1)

    dir1 = sys.argv[1]
    dir2 = sys.argv[2]

    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        print("Error: ambos argumentos deben ser directorios.")
        sys.exit(1)

    print(f"Comparando {dir1} con {dir2}...\n")

    archivos1 = listar_archivos(dir1)
    archivos2 = listar_archivos(dir2)

    solo_en_1 = archivos1 - archivos2
    solo_en_2 = archivos2 - archivos1
    en_ambos = archivos1 & archivos2

    print("Solo en dir1:")
    for f in solo_en_1:
        print(f"  {f}")
    print()

    print("Solo en dir2:")
    for f in solo_en_2:
        print(f"  {f}")
    print()

    modificados_size = []
    modificados_fecha = []
    identicos = 0

    for f in en_ambos:
        ruta1 = os.path.join(dir1, f)
        ruta2 = os.path.join(dir2, f)

        size1, time1 = info_archivo(ruta1)
        size2, time2 = info_archivo(ruta2)

        if size1 != size2:
            modificados_size.append((f, size1, size2))
        elif time1 != time2:
            modificados_fecha.append((f, time1, time2))
        else:
            identicos += 1

    print("Modificados (tamaño diferente):")
    for f, s1, s2 in modificados_size:
        print(f"  {f} ({s1} -> {s2} bytes)")
    print()

    print("Modificados (fecha diferente):")
    for f, t1, t2 in modificados_fecha:
        print(f"  {f}")
    print()

    print(f"Idénticos: {identicos} archivos")


if __name__ == "__main__":
    main()