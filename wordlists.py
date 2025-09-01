from pathlib import Path
from config import config, guardar_config

def seleccionar_wordlist():
    wordlist_dir = Path("./wordlist")
    if not wordlist_dir.exists() or not any(wordlist_dir.iterdir()):
        print("[!] No hay wordlists instaladas.")
        return

    listas = sorted(wordlist_dir.glob("*"), key=lambda x: x.name.lower())
    recomendadas = ["common.txt", "directory-list-2.3-small.txt", "directory-list-2.3-medium.txt"]

    print("\n=== Wordlists disponibles ===")
    for i, lista in enumerate(listas, 1):
        tag = " [⭐]" if lista.name in recomendadas else ""
        print(f"{i}. {lista.name}{tag}")

    seleccion = input("Seleccione listas (1,3,5 | 'a'=todas | 'r'=recomendadas): ").strip()

    if seleccion.lower() == "a":
        config["wordlist"] = [wl.name for wl in listas]  # todas
        print(f"[+] Todas las wordlists seleccionadas")
    elif seleccion.lower() == "r":
        config["wordlist"] = recomendadas[:]  # recomendadas exactas
        print(f"[+] Wordlists recomendadas seleccionadas: {', '.join(config['wordlist'])}")
    else:
        indices = [int(x) for x in seleccion.split(",") if x.strip().isdigit()]
        config["wordlist"] = [listas[i-1].name for i in indices if 1 <= i <= len(listas)]
        print(f"[+] Wordlists seleccionadas: {', '.join(config['wordlist'])}")

    guardar_config()
