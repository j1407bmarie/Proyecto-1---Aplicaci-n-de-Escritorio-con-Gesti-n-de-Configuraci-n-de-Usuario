# Config App

Aplicación de escritorio hecha en Python con Tkinter para manejar la configuración del usuario.

Es una  aplicación que permite cambiar diferentes opciones como el nombre, tema, idioma, tamaño de fuente, colores, estilos de texto y foto de perfil. Estos cambios se guardan en un archivo JSON para que se mantengan al volver a abrir el programa.

## Estructura

```text
Proyecto-1---Aplicación-de-Escritorio-con-Gestión-de-Configuración-de-Usuario
│
├── README.md
├── data/
│   ├── config.json
│   ├── config.bak
│   └── config.tmp
├── docs/
│   ├── Manual tecnico y de usuario
└── src/
    ├── __init__.py
    ├── config_manager.py
    └── main.py
```

* `src/`: contiene el código de la aplicación.
* `data/`: contiene los archivos de configuración.
* `docs/`: contiene los documentos y capturas del proyecto.

En `src/`, `main.py` contiene la interfaz y `config_manager.py` se encarga de leer y guardar la configuración.

En `data/`, `config.json` guarda la configuración actual, `config.bak` guarda un respaldo y `config.tmp` se utiliza temporalmente al guardar.

## Requisitos

Se necesita tener instalado:

* Python 3
* Pillow
* Un programa para abrir archivos PDF

`tkinter`, `json` y `os` vienen incluidos con Python.

Para instalar Pillow:

```bash
pip install Pillow
```

## Ejecución

Desde la carpeta principal del proyecto se ejecuta:

```bash
py -m src.main
```

Si el comando `py` no funciona, también se puede utilizar:

```bash
python -m src.main
```

## Configuración

La configuración se guarda en:

```text
data/config.json
```

El archivo utiliza formato JSON y codificación UTF-8 para poder guardar correctamente caracteres como tildes y la ñ.

Si `config.json` no existe, está corrupto o no se puede leer, el programa utiliza los valores predeterminados de `config_manager.py`.

## Manejo de archivos

Al guardar la configuración se utiliza un archivo temporal y un archivo de respaldo:

* `config.tmp`: se utiliza durante el guardado.
* `config.bak`: conserva la configuración anterior.
* `config.json`: contiene la configuración actual.

También se manejan los casos de archivo ausente, archivo corrupto y falta de permisos.

## Documentación

Los documentos del proyecto se encuentran en la carpeta `docs/`.

Los archivos PDF se pueden abrir con cualquier programa compatible con este formato, como Microsoft Edge, Google Chrome o Adobe Acrobat Reader.

Los PDF son parte de la documentación del proyecto, pero no son necesarios para ejecutar la aplicación.

## Referencias

* Python Documentation: https://docs.python.org/3/
* Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
* JSON Documentation: https://docs.python.org/3/library/json.html
* Pillow Documentation: https://pillow.readthedocs.io/
* Real Python: https://realpython.com/python-json/
* Visual Tkinter: https://visualtkinter.com/
