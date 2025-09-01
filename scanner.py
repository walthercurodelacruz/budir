import requests, concurrent.futures, json, time, hashlib
from pathlib import Path
from config import config
from utils import timestamp

# Variables globales (se reinician en ejecutar_scan)
found_urls = []
sizes_seen = set()
visited_dirs = set()
falsos_positivos = []
falsos_filtrados = 0  # contador dinámico de falsos positivos descartados

def cargar_wordlist():
    rutas = []
    if isinstance(config["wordlist"], list):
        for wl in config["wordlist"]:
            ruta = Path(wl)
            if not ruta.exists():
                ruta = Path("./wordlist") / wl
            rutas.append(ruta)
    elif isinstance(config["wordlist"], str):
        ruta = Path(config["wordlist"])
        if not ruta.exists():
            ruta = Path("./wordlist") / config["wordlist"]
        rutas = [ruta]
    else:
        return []

    words = []
    for ruta in rutas:
        if ruta.exists():
            with open(ruta, "r", errors="ignore") as f:
                words.extend([line.strip() for line in f if line.strip()])
    return words

# 🚨 Detectar respuestas genéricas (falsos positivos)
def detectar_respuesta_generica(base_url):
    resultados = []
    for i in range(2):
        fake_url = f"{base_url}/__budir_fake_{i}.txt"
        try:
            r = requests.get(fake_url, timeout=5, headers=config["headers"])
            h = hashlib.md5(r.content).hexdigest()
            resultados.append((r.status_code, len(r.content), h))
        except:
            pass
    return resultados

def es_falso_positivo(r):
    global falsos_filtrados
    h = hashlib.md5(r.content).hexdigest()
    if (r.status_code, len(r.content), h) in falsos_positivos:
        falsos_filtrados += 1
        return True
    return False

def scan_url(base_url, path, output_txt, fallos_txt, depth, max_depth, tasks):
    if config["port"] != 80 and f":{config['port']}" not in base_url:
        base_url = f"{base_url}:{config['port']}"

    urls = []
    if "." in path:
        urls.append(f"{base_url}/{path}")
    else:
        urls.append(f"{base_url}/{path}")
        if config["extensions"]:
            urls += [f"{base_url}/{path}.{ext}" for ext in config["extensions"]]

    for url in urls:
        try:
            r = requests.get(url, timeout=5, allow_redirects=True, headers=config["headers"])
            size = len(r.content)

            # Guardar todo en fallos
            with open(fallos_txt, "a") as f:
                f.write(f"{url} (code: {r.status_code}, size: {size})\n")

            # 🚨 Filtrar falsos positivos
            if es_falso_positivo(r):
                continue

            if size in sizes_seen:
                continue
            if r.status_code in config["status_codes"]:
                msg = f"{url} (code: {r.status_code}, size: {size})"
                found_urls.append({"url": url, "code": r.status_code, "size": size})

                with open(output_txt, "a") as f:
                    f.write(msg + "\n")

                if r.status_code == 200:
                    print(f"\033[92m[200]\033[0m {msg}")

                # 🚀 Crawling si aplica
                if config["recurse"] and depth < max_depth:
                    if url.endswith("/") or r.status_code in [301, 302, 403]:
                        if url not in visited_dirs:
                            visited_dirs.add(url)
                            tasks.append((url, depth + 1))

        except requests.RequestException as e:
            with open(fallos_txt, "a") as f:
                f.write(f"{url} (ERROR: {str(e)})\n")

def ejecutar_scan():
    global falsos_positivos, falsos_filtrados, found_urls, sizes_seen, visited_dirs

    # 🔄 Reiniciar estados para cada escaneo
    found_urls = []
    sizes_seen = set()
    visited_dirs = set()
    falsos_positivos = []
    falsos_filtrados = 0

    if not config["url"] or not config["wordlist"]:
        print("\033[91m[!] Define objetivo y wordlist primero.\033[0m")
        return []

    url = config["url"].strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    # 🚨 Detectamos respuestas falsas al inicio
    falsos_positivos = detectar_respuesta_generica(url)
    if falsos_positivos:
        print(f"\033[93m[!] Detectadas {len(falsos_positivos)} respuestas genéricas -> se filtrarán falsos positivos\033[0m")

    report_dir = Path("./reportes")
    report_dir.mkdir(exist_ok=True)
    ts = timestamp()
    output_txt = report_dir / f"budir_{ts}.txt"
    output_json = report_dir / f"budir_{ts}.json"
    fallos_txt = report_dir / f"budir_fallos_{ts}.txt"

    paths = cargar_wordlist()
    total = len(paths)
    print(f"\033[96m[*] Iniciando escaneo sobre {url} con {total} rutas...\033[0m")
    start_time = time.time()

    tasks = [(url, 1)]

    try:
        while tasks:
            current_url, depth = tasks.pop(0)
            print(f"\033[94m[~] Escaneando {current_url} (depth={depth})...\033[0m")

            with concurrent.futures.ThreadPoolExecutor(max_workers=config["threads"]) as executor:
                futures = []
                for path in paths:
                    futures.append(executor.submit(scan_url, current_url, path, output_txt, fallos_txt, depth, config["depth"], tasks))
                concurrent.futures.wait(futures)

    except KeyboardInterrupt:
        print("\n\033[91m[!] Escaneo interrumpido por el usuario.\033[0m")

    # Guardar resultados aunque se haya cancelado
    with open(output_json, "w") as jf:
        json.dump(found_urls, jf, indent=4)

    elapsed = time.time() - start_time
    print("\n\033[95m=== RESUMEN ===\033[0m")
    print(f"Total de rutas probadas: {total}")
    print(f"Hallazgos válidos (sin falsos positivos): {len(found_urls)}")
    print(f"Falsos positivos detectados al inicio: {len(falsos_positivos)}")
    print(f"Respuestas filtradas como falsos positivos: {falsos_filtrados}")
    print(f"Tiempo total: {elapsed:.2f} segundos")
    print(f"\033[96m[+] Resultados guardados en:\n - {output_txt}\n - {output_json}\n - {fallos_txt}\033[0m")

    only_200 = [f for f in found_urls if f["code"] == 200]
    if only_200:
        print("\n\033[92m=== HALLAZGOS ENCONTRADOS (200 OK) ===\033[0m")
        for item in only_200:
            print(f"{item['url']} (code: 200, size: {item['size']})")
    else:
        print("\033[91m\n[-] No se encontraron rutas con código 200 válidas.\033[0m")

    return only_200

