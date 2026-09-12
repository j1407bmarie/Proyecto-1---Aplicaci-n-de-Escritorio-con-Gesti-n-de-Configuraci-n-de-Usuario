"""Gestor de configuracion JSON UTF-8."""
import json
from pathlib import Path

DATA_DIR = Path("data")
CONFIG_PATH = DATA_DIR / "config.json"
BACKUP_PATH = DATA_DIR / "config.bak"
TEMP_PATH = DATA_DIR / "config.tmp"

DEFAULT_CONFIG = {
    "nombre_usuario": "Invitado",
    "tema_interfaz": "claro",
    "idioma": "es-ES",
    "tamano_fuente": 11,
    "color_barra_menu": "#2c3e50",
    "color_letra": "#ffffff",
    "foto_perfil": "",
}


def load_config() -> dict:
    """Carga la configuracion desde disco o devuelve defaults."""
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Guarda la configuracion de forma segura."""
    pass
