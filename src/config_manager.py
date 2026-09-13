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
        return CONFIG_DEFAULT.copy()

    try:

        with open(CONFIG_PATH, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

        if not isinstance(config, dict):
            print("El archivo de configuracion no tiene un formato valido.")
            return CONFIG_DEFAULT.copy()

        for clave in CONFIG_DEFAULT:

            if clave not in config:
                print("Falta informacion en el archivo de configuracion.")
                return CONFIG_DEFAULT.copy()

        return config

    except json.JSONDecodeError:

        print("El archivo de configuracion esta corrupto.")
        return CONFIG_DEFAULT.copy()

    except PermissionError:

        print("No tienes permiso para leer el archivo de configuracion.")
        return CONFIG_DEFAULT.copy()

    except OSError:

        print("Ocurrio un error al leer el archivo de configuracion.")
        return CONFIG_DEFAULT.copy()


def save_config(config):

    archivo_temporal = "data/config.tmp"
    archivo_backup = "data/config.bak"

    try:

        with open(archivo_temporal, "w", encoding="utf-8") as archivo:
            json.dump(
                config,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        if os.path.exists(CONFIG_PATH):

            os.replace(
                CONFIG_PATH,
                archivo_backup
            )

        os.replace(
            archivo_temporal,
            CONFIG_PATH
        )

        print("Configuracion guardada correctamente.")

    except (PermissionError, OSError) as error:

        print("No se pudo guardar la configuracion.")
        print("Detalle:", error)

        if os.path.exists(archivo_temporal):

            os.remove(
                archivo_temporal
            )

        if (
            os.path.exists(archivo_backup)
            and not os.path.exists(CONFIG_PATH)
        ):

            os.replace(
                archivo_backup,
                CONFIG_PATH
            )