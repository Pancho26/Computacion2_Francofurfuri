#python3 Inspector.py /etc/passwd

import os
import sys
import stat
import pwd
import grp
from datetime import datetime


def formatear_fecha(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def obtener_tipo_archivo(modo, ruta):
    if stat.S_ISREG(modo):
        return "archivo regular"
    elif stat.S_ISDIR(modo):
        return "directorio"
    elif stat.S_ISLNK(modo):
        destino = os.readlink(ruta)
        return f"enlace simbólico -> {destino}"
    elif stat.S_ISCHR(modo):
        return "dispositivo de caracteres"
    elif stat.S_ISBLK(modo):
        return "dispositivo de bloques"
    elif stat.S_ISFIFO(modo):
        return "FIFO / pipe"
    elif stat.S_ISSOCK(modo):
        return "socket"
    else:
        return "tipo desconocido"


def main():
    if len(sys.argv) != 2:
        print("Uso: python inspector.py <ruta>")
        sys.exit(1)

    ruta = sys.argv[1]

    if not os.path.exists(ruta) and not os.path.islink(ruta):
        print(f"Error: la ruta '{ruta}' no existe.")
        sys.exit(1)

    try:
        info = os.lstat(ruta)  # lstat para no seguir symlinks automáticamente

        tipo = obtener_tipo_archivo(info.st_mode, ruta)
        permisos_simbolicos = stat.filemode(info.st_mode)
        permisos_octales = oct(info.st_mode & 0o777)

        try:
            propietario = pwd.getpwuid(info.st_uid).pw_name
        except KeyError:
            propietario = str(info.st_uid)

        try:
            grupo = grp.getgrgid(info.st_gid).gr_name
        except KeyError:
            grupo = str(info.st_gid)

        print(f"Archivo: {ruta}")
        print(f"Tipo: {tipo}")
        print(f"Tamaño: {info.st_size} bytes")
        print(f"Permisos: {permisos_simbolicos} ({permisos_octales})")
        print(f"Propietario: {propietario} (uid: {info.st_uid})")
        print(f"Grupo: {grupo} (gid: {info.st_gid})")
        print(f"Inodo: {info.st_ino}")
        print(f"Enlaces duros: {info.st_nlink}")
        print(f"Último acceso: {formatear_fecha(info.st_atime)}")
        print(f"Última modificación: {formatear_fecha(info.st_mtime)}")
        print(f"Último cambio de estado: {formatear_fecha(info.st_ctime)}")

    except PermissionError:
        print(f"Error: no tenés permisos para acceder a '{ruta}'.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: la ruta '{ruta}' no existe.")
        sys.exit(1)
    except OSError as e:
        print(f"Error al inspeccionar la ruta: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()