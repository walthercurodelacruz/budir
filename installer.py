import subprocess, shutil
from pathlib import Path

def instalar_seclists():
    destino = Path("./wordlist")
    destino.mkdir(exist_ok=True)

    if any(destino.iterdir()):
        choice = input("[!] Existen listas en ./wordlist. ¿Actualizar con SecList? (S/N): ").strip().lower()
        if choice != "s":
            print("[*] Instalación cancelada.")
            return
        shutil.rmtree(destino)
        destino.mkdir(exist_ok=True)

    repo_url = "https://github.com/danielmiessler/SecLists.git"
    temp_dir = Path("./SecLists")

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    print("[*] Clonando SecLists...")
    subprocess.run(["git", "clone", "--depth", "1", repo_url, str(temp_dir)], check=True)

    src = temp_dir / "Discovery" / "Web-Content"
    if src.exists():
        for item in src.iterdir():
            dest_item = destino / item.name
            if item.is_file():
                shutil.copy2(item, dest_item)
            elif item.is_dir():
                if dest_item.exists():
                    shutil.rmtree(dest_item)
                shutil.copytree(item, dest_item)
        print(f"[+] Wordlists copiadas a {destino}")
    shutil.rmtree(temp_dir)
