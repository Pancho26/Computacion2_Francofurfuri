#python3 tareas.py --add "Estudiar"
#python3 tareas.py --list





import argparse
import json
import sys
from pathlib import Path

ARCHIVO_TAREAS = Path.home() / ".tareas.json"


def cargar_tareas():
    if not ARCHIVO_TAREAS.exists():
        return []

    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        print("Error: No se pudieron cargar las tareas")
        sys.exit(1)


def guardar_tareas(tareas):
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as archivo:
            json.dump(tareas, archivo, indent=4, ensure_ascii=False)
    except OSError:
        print("Error: No se pudieron guardar las tareas")
        sys.exit(1)


def siguiente_id(tareas):
    if not tareas:
        return 1
    return max(tarea["id"] for tarea in tareas) + 1


def buscar_tarea_por_id(tareas, tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            return tarea
    return None


def comando_add(args):
    tareas = cargar_tareas()

    tarea = {
        "id": siguiente_id(tareas),
        "descripcion": args.descripcion,
        "completada": False,
        "priority": args.priority
    }

    tareas.append(tarea)
    guardar_tareas(tareas)

    if args.priority:
        print(f"Tarea #{tarea['id']} agregada (prioridad: {args.priority})")
    else:
        print(f"Tarea #{tarea['id']} agregada")


def comando_list(args):
    tareas = cargar_tareas()
    resultado = []

    for tarea in tareas:
        if args.pending and tarea["completada"]:
            continue

        if args.done and not tarea["completada"]:
            continue

        if args.priority and tarea["priority"] != args.priority:
            continue

        resultado.append(tarea)

    for tarea in resultado:
        estado = "x" if tarea["completada"] else " "
        prioridad = f" [{tarea['priority'].upper()}]" if tarea["priority"] else ""
        print(f"#{tarea['id']} [{estado}] {tarea['descripcion']}{prioridad}")


def comando_done(args):
    tareas = cargar_tareas()
    tarea = buscar_tarea_por_id(tareas, args.id)

    if tarea is None:
        print(f"Error: No existe la tarea #{args.id}")
        sys.exit(1)

    tarea["completada"] = True
    guardar_tareas(tareas)
    print(f"Tarea #{args.id} completada")


def comando_remove(args):
    tareas = cargar_tareas()
    tarea = buscar_tarea_por_id(tareas, args.id)

    if tarea is None:
        print(f"Error: No existe la tarea #{args.id}")
        sys.exit(1)

    respuesta = input(f'¿Eliminar "{tarea["descripcion"]}"? [s/N] ')

    if respuesta.lower() != "s":
        print("Operación cancelada")
        sys.exit(0)

    tareas = [t for t in tareas if t["id"] != args.id]
    guardar_tareas(tareas)
    print(f"Tarea #{args.id} eliminada")


def main():
    parser = argparse.ArgumentParser(
        description="Gestor de tareas simple."
    )

    subparsers = parser.add_subparsers(dest="comando", required=True)

    parser_add = subparsers.add_parser("add", help="Agrega una tarea")
    parser_add.add_argument("descripcion", help="Descripción de la tarea")
    parser_add.add_argument(
        "--priority",
        choices=["baja", "media", "alta"],
        help="Prioridad de la tarea"
    )
    parser_add.set_defaults(func=comando_add)

    parser_list = subparsers.add_parser("list", help="Lista tareas")
    parser_list.add_argument(
        "--pending",
        action="store_true",
        help="Muestra solo tareas pendientes"
    )
    parser_list.add_argument(
        "--done",
        action="store_true",
        help="Muestra solo tareas completadas"
    )
    parser_list.add_argument(
        "--priority",
        choices=["baja", "media", "alta"],
        help="Filtra por prioridad"
    )
    parser_list.set_defaults(func=comando_list)

    parser_done = subparsers.add_parser("done", help="Marca una tarea como completada")
    parser_done.add_argument("id", type=int, help="ID de la tarea")
    parser_done.set_defaults(func=comando_done)

    parser_remove = subparsers.add_parser("remove", help="Elimina una tarea")
    parser_remove.add_argument("id", type=int, help="ID de la tarea")
    parser_remove.set_defaults(func=comando_remove)

    args = parser.parse_args()
    args.func(args)
    sys.exit(0)


if __name__ == "__main__":
    main()