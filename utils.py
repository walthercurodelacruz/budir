import os, platform
from datetime import datetime

def limpiar_pantalla():
    os.system("cls" if platform.system() == "Windows" else "clear")

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M")
