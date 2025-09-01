from utils import limpiar_pantalla
from installer import instalar_seclists
from wordlists import seleccionar_wordlist
from scanner import ejecutar_scan
from config import config, cargar_config, guardar_config
import os, json

# Colores ANSI
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
M = "\033[95m"
C = "\033[96m"
RESET = "\033[0m"

def header():
    print(C + "===================================================" + RESET)
    print(G + "    BUDIR // Web Content Scanner - Underground CLI " + RESET)
    print(M + "          by Walther Curo - 0xBUDIR               " + RESET)
    print(C + "===================================================" + RESET)
    print(Y + ":: SCAN AND ENUMERATE THE HIDDEN PATHS ::" + RESET + "\n")

# === SUBMENÚ WORDLISTS ===
def gestionar_wordlists():
    while True:
        limpiar_pantalla()
        listas = config["wordlist"] if isinstance(config["wordlist"], list) else [config["wordlist"]]
        print(C + "=== GESTIÓN DE WORDLISTS ===" + RESET)
        print("Wordlists actuales:")
        for idx, wl in enumerate(listas, 1):
            print(f"  {idx}. {wl}")

        print("\n[1] Agregar wordlist (mostrar disponibles en ./wordlist/)")
        print("[2] Eliminar wordlist")
        print("[3] Restaurar por defecto (common.txt)")
        print("[4] Volver al menú principal")

        opcion = input(C + "\nbudir@underground:~$ " + RESET).strip()

        if opcion == "1":
            print(Y + "\n=== LISTAS DISPONIBLES EN ./wordlist/ ===" + RESET)
            wordlist_dir = "./wordlist"
            if not os.path.exists(wordlist_dir):
                os.makedirs(wordlist_dir, exist_ok=True)

            disponibles = sorted(os.listdir(wordlist_dir))
            if not disponibles:
                print(R + "[!] No hay wordlists en ./wordlist/. Instala SecLists o añade manualmente." + RESET)
            else:
                for idx, f in enumerate(disponibles, 1):
                    print(f"{Y}[{idx:02d}]{RESET} {f}")

                num = input("\nSelecciona el número de la wordlist a agregar: ").strip()
                if num.isdigit() and 1 <= int(num) <= len(disponibles):
                    nueva = os.path.join(wordlist_dir, disponibles[int(num)-1])
                    if isinstance(config["wordlist"], list):
                        if nueva not in config["wordlist"]:
                            config["wordlist"].append(nueva)
                    else:
                        config["wordlist"] = [config["wordlist"], nueva] if config["wordlist"] else [nueva]
                    guardar_config()
                    print(G + f"[+] Wordlist '{nueva}' agregada." + RESET)
                else:
                    print(R + "[!] Número inválido." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "2":
            borrar = input("Nombre o ruta de la wordlist a eliminar: ").strip()
            if isinstance(config["wordlist"], list) and borrar in config["wordlist"]:
                config["wordlist"].remove(borrar)
                guardar_config()
                print(R + f"[-] Wordlist '{borrar}' eliminada." + RESET)
            elif config["wordlist"] == borrar:
                config["wordlist"] = []
                guardar_config()
                print(R + f"[-] Wordlist '{borrar}' eliminada." + RESET)
            else:
                print(R + "[!] Wordlist no encontrada." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "3":
            config["wordlist"] = ["common.txt"]
            guardar_config()
            print(Y + "[*] Lista restaurada a valores por defecto (common.txt)." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "4":
            break

# === SUBMENÚ EXTENSIONES ===
def gestionar_extensiones():
    while True:
        limpiar_pantalla()
        print(C + "=== GESTIÓN DE EXTENSIONES SENSIBLES ===" + RESET)
        print(f"{Y}Extensiones actuales:{RESET} {', '.join(config['extensions'])}")

        print("\n[1] Agregar extensión")
        print("[2] Eliminar extensión")
        print("[3] Restaurar por defecto (zip,rar,sql,bak,gz,tar,7z)")
        print("[4] Volver al menú principal")

        opcion = input(C + "\nbudir@underground:~$ " + RESET).strip()

        if opcion == "1":
            nueva = input("Extensión a agregar (sin punto, ej: conf): ").strip().lower()
            if nueva and nueva.isalnum() and nueva not in config["extensions"]:
                config["extensions"].append(nueva)
                guardar_config()
                print(G + f"[+] Extensión '{nueva}' agregada." + RESET)
            else:
                print(R + "[!] Extensión inválida o ya existe." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "2":
            borrar = input("Extensión a eliminar (sin punto): ").strip().lower()
            if borrar in config["extensions"]:
                config["extensions"].remove(borrar)
                guardar_config()
                print(R + f"[-] Extensión '{borrar}' eliminada." + RESET)
            else:
                print(R + "[!] Extensión no encontrada." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "3":
            config["extensions"] = ["zip", "rar", "sql", "bak", "gz", "tar", "7z"]
            guardar_config()
            print(Y + "[*] Lista restaurada a valores por defecto." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "4":
            break

# === SUBMENÚ CABECERAS ===
def gestionar_cabeceras():
    while True:
        limpiar_pantalla()
        print(C + "=== GESTIÓN DE CABECERAS (HEADERS) ===" + RESET)
        if config["headers"]:
            print(Y + "Cabeceras actuales:" + RESET)
            for k, v in config["headers"].items():
                print(f" - {k}: {v}")
        else:
            print(R + "[!] No hay cabeceras configuradas." + RESET)

        print("\n[1] Agregar cabecera")
        print("[2] Eliminar cabecera")
        print("[3] Restaurar por defecto (User-Agent: budir/1.0)")
        print("[4] Volver al menú principal")

        opcion = input(C + "\nbudir@underground:~$ " + RESET).strip()

        if opcion == "1":
            key = input("Nombre de la cabecera (ej: Authorization): ").strip()
            val = input("Valor de la cabecera: ").strip()
            if key and val:
                config["headers"][key] = val
                guardar_config()
                print(G + f"[+] Cabecera '{key}: {val}' agregada." + RESET)
            else:
                print(R + "[!] Clave o valor inválido." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "2":
            key = input("Nombre de la cabecera a eliminar: ").strip()
            if key in config["headers"]:
                del config["headers"][key]
                guardar_config()
                print(R + f"[-] Cabecera '{key}' eliminada." + RESET)
            else:
                print(R + "[!] Cabecera no encontrada." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "3":
            config["headers"] = {"User-Agent": "budir/1.0"}
            guardar_config()
            print(Y + "[*] Cabeceras restauradas por defecto." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "4":
            break

# === SUBMENÚ RECURSIVIDAD ===
def gestionar_recursividad():
    while True:
        limpiar_pantalla()
        print(C + "=== GESTIÓN DE RECURSIVIDAD ===" + RESET)
        print(f"{Y}Estado actual:{RESET} recurse={config['recurse']} depth={config['depth']}")

        print("\n[1] Activar/Desactivar recursividad")
        print("[2] Aumentar profundidad (+1)")
        print("[3] Disminuir profundidad (-1)")
        print("[4] Restaurar valores por defecto (False, depth=1)")
        print("[5] Volver al menú principal")

        opcion = input(C + "\nbudir@underground:~$ " + RESET).strip()

        if opcion == "1":
            config["recurse"] = not config["recurse"]
            guardar_config()
            estado = "activada" if config["recurse"] else "desactivada"
            print(G + f"[+] Recursividad {estado}." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "2":
            config["depth"] += 1
            guardar_config()
            print(G + f"[+] Profundidad aumentada a {config['depth']}." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "3":
            if config["depth"] > 1:
                config["depth"] -= 1
                guardar_config()
                print(G + f"[+] Profundidad reducida a {config['depth']}." + RESET)
            else:
                print(R + "[!] La profundidad mínima es 1." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "4":
            config["recurse"] = False
            config["depth"] = 1
            guardar_config()
            print(Y + "[*] Recursividad restaurada a valores por defecto." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "5":
            break

# === RESUMEN DESPUÉS DE ESCANEO ===
def ejecutar_con_resumen():
    limpiar_pantalla()
    print(Y + "[*] Iniciando escaneo..." + RESET)
    hallazgos = ejecutar_scan()

    print("\n" + C + "=== RESUMEN DEL ESCANEO ===" + RESET)
    print(f"{B}Objetivo:{RESET} {config['url']}")
    print(f"{B}Puerto:{RESET} {config['port']}")
    print(f"{B}Wordlists:{RESET} {config['wordlist']}")
    print(f"{B}Extensiones:{RESET} {config['extensions']}")
    print(f"{B}Headers:{RESET} {config['headers']}")
    print(f"{B}Recursividad:{RESET} {config['recurse']} (depth={config['depth']})")
    print(f"{G}Hallazgos encontrados:{RESET} {len(hallazgos)}")

    if hallazgos:
        print("\n" + M + "Rutas encontradas (HTTP 200):" + RESET)
        for h in hallazgos:
            print(f" {G}[200]{RESET} {h['url']} (size: {h['size']})")

    input("\n[ENTER] para continuar...")

# === SUBMENÚ REPORTES ===
def ver_reportes():
    while True:
        limpiar_pantalla()
        print(C + "=== GESTIÓN DE REPORTES ===\n" + RESET)
        report_dir = "./reportes"

        if not os.path.exists(report_dir):
            print(R + "[!] No existe la carpeta de reportes todavía." + RESET)
            input("\n[ENTER] para continuar...")
            break

        archivos = sorted(os.listdir(report_dir))
        if not archivos:
            print(R + "[!] No se encontraron reportes en ./reportes/" + RESET)
            input("\n[ENTER] para continuar...")
            break

        print("Reportes disponibles:")
        for idx, f in enumerate(archivos, 1):
            tipo = "TXT" if f.endswith(".txt") else "JSON" if f.endswith(".json") else "OTRO"
            print(f"{Y}[{idx:02d}]{RESET} {f}   ({C}{tipo}{RESET})")

        print("\n[1] Leer un reporte")
        print("[2] Eliminar un reporte")
        print("[3] Limpiar carpeta de reportes")
        print("[4] Volver al menú principal")

        opcion = input(C + "\nbudir@underground:~$ " + RESET).strip()

        if opcion == "1":
            num = input("Número del reporte a leer: ").strip()
            if num.isdigit() and 1 <= int(num) <= len(archivos):
                archivo = archivos[int(num)-1]
                ruta = os.path.join(report_dir, archivo)
                print(f"\n{G}=== CONTENIDO DE: {archivo} ==={RESET}\n")
                try:
                    if archivo.endswith(".json"):
                        with open(ruta, "r", errors="ignore") as f:
                            data = json.load(f)
                            print(json.dumps(data, indent=4))
                    else:
                        with open(ruta, "r", errors="ignore") as f:
                            print(f.read())
                except Exception as e:
                    print(f"{R}[!] Error al leer el archivo: {e}{RESET}")
            else:
                print(R + "[!] Número inválido." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "2":
            num = input("Número del reporte a eliminar: ").strip()
            if num.isdigit() and 1 <= int(num) <= len(archivos):
                archivo = archivos[int(num)-1]
                ruta = os.path.join(report_dir, archivo)
                try:
                    os.remove(ruta)
                    print(f"{R}[-] Reporte '{archivo}' eliminado.{RESET}")
                except Exception as e:
                    print(f"{R}[!] Error al eliminar: {e}{RESET}")
            else:
                print(R + "[!] Número inválido." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "3":
            confirm = input(R + "¿Seguro que deseas eliminar TODOS los reportes? (s/n): " + RESET).strip().lower()
            if confirm == "s":
                try:
                    for f in archivos:
                        os.remove(os.path.join(report_dir, f))
                    print(G + "[*] Todos los reportes eliminados." + RESET)
                except Exception as e:
                    print(f"{R}[!] Error al limpiar: {e}{RESET}")
            else:
                print(Y + "[*] Operación cancelada." + RESET)
            input("\n[ENTER] para continuar...")

        elif opcion == "4":
            break

# === MENÚ PRINCIPAL ===
def menu():
    cargar_config()
    while True:
        limpiar_pantalla()
        header()
        print(f"{Y}[01]{RESET} Instalar listas de seclists")
        print(f"{Y}[02]{RESET} Definir Objetivo (url/IP)  -> {C}{config['url']}{RESET}")
        print(f"{Y}[03]{RESET} Definir puerto             -> {C}{config['port']}{RESET}")

        if isinstance(config["wordlist"], list):
            wl_str = ", ".join(config["wordlist"])
        else:
            wl_str = str(config["wordlist"])
        print(f"{Y}[04]{RESET} Gestionar wordlists        -> {C}{wl_str}{RESET}")

        print(f"{Y}[05]{RESET} Gestionar extensiones      -> {C}{','.join(config['extensions'])}{RESET}")
        print(f"{Y}[06]{RESET} Gestionar cabeceras        -> {C}{config['headers']}{RESET}")
        print(f"{Y}[07]{RESET} Gestionar recursividad     -> {C}{config['recurse']} depth={config['depth']}{RESET}")
        print(f"{Y}[08]{RESET} Ejecutar escaneo")
        print(f"{Y}[09]{RESET} Ver reportes")
        print(f"{Y}[10]{RESET} Salir")

        opcion = input(C + "\nbudir@underground:~$ " + RESET).strip()
        if opcion in ["1", "01"]:
            instalar_seclists(); input("\n[ENTER] para continuar...")
        elif opcion in ["2", "02"]:
            config["url"] = input("Objetivo: ").strip(); guardar_config()
        elif opcion in ["3", "03"]:
            p = input("Puerto: ").strip()
            if p.isdigit(): config["port"] = int(p); guardar_config()
        elif opcion in ["4", "04"]:
            gestionar_wordlists()
        elif opcion in ["5", "05"]:
            gestionar_extensiones()
        elif opcion in ["6", "06"]:
            gestionar_cabeceras()
        elif opcion in ["7", "07"]:
            gestionar_recursividad()
        elif opcion in ["8", "08"]:
            ejecutar_con_resumen()
        elif opcion in ["9", "09"]:
            ver_reportes()
        elif opcion == "10":
            break

