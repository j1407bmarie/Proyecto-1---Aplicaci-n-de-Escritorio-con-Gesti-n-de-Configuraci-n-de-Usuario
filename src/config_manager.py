import json
import os


CONFIG_PATH = "data/config.json"


CONFIG_DEFAULT = {
    "nombre_usuario": "Invitado",
    "tema_interfaz": "claro",
    "idioma": "es-ES",
    "tamano_fuente": 11,
    "color_barra_menu": "#2c3e50",
    "color_letra": "#ffffff",
    "foto_perfil": ""
}


def load_config():

    if not os.path.exists(CONFIG_PATH):
        return CONFIG_DEFAULT

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

        return config

    except json.JSONDecodeError:
        print("El archivo de configuracion esta corrupto.")
        return CONFIG_DEFAULT

    except PermissionError:
        print("No tienes permiso para leer el archivo de configuracion.")
        return CONFIG_DEFAULT
    
    
def save_config(config):

    with open(CONFIG_PATH, "w", encoding="utf-8") as archivo:
        json.dump(config, archivo, indent=4, ensure_ascii=False)