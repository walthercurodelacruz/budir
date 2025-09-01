# 🚀 BUDIR – Web Content Scanner Underground CLI

**BUDIR** (Burp + Dirbuster style) es una herramienta **open-source** desarrollada en **Python** para la **enumeración de contenido web oculto**, diseñada con un enfoque modular, técnico y altamente personalizable.  

Permite descubrir rutas, archivos sensibles y directorios ocultos en servidores web mediante el uso de **wordlists**, **extensiones personalizadas**, y **crawling controlado**, con reportes automáticos en múltiples formatos.

---

## ✨ Características Principales

- 🔎 **Descubrimiento de rutas y archivos sensibles** (zip, sql, bak, rar, etc.).
- 📂 **Gestión avanzada de wordlists** (integración directa con **SecLists**).
- ⚡ **Escaneo multihilo** con `ThreadPoolExecutor` para máxima velocidad.
- 🛡️ **Detección y filtrado de falsos positivos** (hash MD5 de respuestas).
- 🔁 **Recursividad configurable** con control de profundidad (`depth`).
- 📑 **Reportes automáticos en TXT y JSON** (fácil análisis y parseo).
- 🖥️ **Interfaz CLI con menús interactivos** y colores ANSI.
- ⏹️ **Cancelación segura del escaneo** (`Ctrl+C`) con resumen parcial.
- ⚙️ **Configuración persistente** vía `config.json` (se guarda entre sesiones).
- 🎨 **Estilo underground** en la CLI: minimalista y de alto impacto.

---

## 📂 Estructura del Proyecto

```
budir/
│── budir.py              # Entry point principal
│── config.json           # Configuración persistente
│── config.py             # Manejo de configuración
│── installer.py          # Instalación automática de SecLists
│── menu.py               # Interfaz CLI con menús interactivos
│── scanner.py            # Motor de escaneo principal
│── utils.py              # Funciones auxiliares
│── wordlists.py          # Selección interactiva de wordlists
│── reportes/             # Carpeta de salida de reportes
│── wordlist/             # Carpeta de wordlists instaladas
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio y ejecutar
```bash
git clone https://github.com/usuario/budir.git
cd budir
python budir.py
```

### 2. Python y dependencia requerido


> - Python 3.8+  
> - requests  
> - concurrent.futures (incluido en Python 3.8+)  

### 3. Instalar Wordlists
```bash
python budir.py
```
En el menú, selecciona:
```
[01] Instalar listas de SecLists
```
Esto descargará automáticamente las wordlists recomendadas desde el repo oficial.

---

### Menú Principal
```
[01] Instalar listas de seclists
[02] Definir Objetivo (url/IP)
[03] Definir puerto
[04] Gestionar wordlists
[05] Gestionar extensiones
[06] Gestionar cabeceras
[07] Gestionar recursividad
[08] Ejecutar escaneo
[09] Ver reportes
[10] Salir
```

### Ejemplo de Escaneo
1. Define objetivo (`[02]`) → ej: `http://target.com`  
2. Define puerto (`[03]`) → ej: `80`  
3. Selecciona wordlist (`[04]`) → ej: `common.txt`  
4. Ejecuta el escaneo (`[08]`)  

El resultado se mostrará en pantalla y se almacenará en:
```
./reportes/budir_TIMESTAMP.txt
./reportes/budir_TIMESTAMP.json
```

---

## 🔍 Motor de Escaneo

- Genera URLs combinando rutas de la wordlist + extensiones configuradas.
- Filtra **respuestas genéricas** que producen falsos positivos.
- Reporta solo códigos de estado configurados: `200, 301, 302, 403`.
- Guarda tanto hallazgos como errores en reportes separados.

Ejemplo de salida:
```
[200] http://target.com/admin (code: 200, size: 1524)
[403] http://target.com/backup.zip (code: 403, size: 210)
```

---

## 📑 Reportes

- **TXT**: listado plano de hallazgos.  
- **JSON**: estructurado con `url`, `code`, `size`.  
- **Fallos**: listado de errores o timeouts (`budir_fallos_TIMESTAMP.txt`).  

Ejemplo JSON:
```json
[
    {"url": "http://target.com/admin", "code": 200, "size": 1524},
    {"url": "http://target.com/backup.zip", "code": 403, "size": 210}
]
```

---

## 🛠️ Configuración Avanzada

El archivo `config.json` guarda la configuración actual:
```json
{
    "url": "target.com",
    "port": 80,
    "wordlist": ["common.txt"],
    "extensions": ["zip", "rar", "sql", "bak"],
    "threads": 10,
    "status_codes": [200, 301, 302, 403],
    "recurse": true,
    "depth": 1,
    "headers": {"User-Agent": "budir/1.0"}
}
```

Puedes modificarlo manualmente o desde el menú.

---

## ⚠️ Descargo de Responsabilidad

> **BUDIR** es una herramienta desarrollada con fines **educativos y de investigación**.  
> Está destinada **únicamente a entornos controlados**, laboratorios de ciberseguridad o sistemas propios donde tengas autorización expresa.  

El uso indebido de esta herramienta contra sistemas sin permiso constituye una **actividad ilegal** y puede acarrear **sanciones penales y civiles**.  
El autor **no se hace responsable** por el mal uso que pueda darse.

---

## 👨‍💻 Autor
- Desarrollado por **Walther Curo – 0xBUDIR**  


---
