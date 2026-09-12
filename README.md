# Config App

Aplicacion de escritorio en Python (Tkinter) con gestion robusta de configuracion de usuario.

## Estructura

- `src/` - codigo fuente
- `data/` - archivos de configuracion generados en tiempo de ejecucion
- `docs/` - documentacion, capturas y PDF

## Formato

JSON codificado en UTF-8.

## Ejecucion

Desde la raiz del proyecto:

    python -m src.main

## Manejo de archivos

- Carga con valores por defecto si el archivo no existe.
- Escritura segura: config.tmp -> rename -> config.json.
- Respaldo automatico a config.bak.
- Manejo explicito de errores: ausente, corrupto, sin permisos.
