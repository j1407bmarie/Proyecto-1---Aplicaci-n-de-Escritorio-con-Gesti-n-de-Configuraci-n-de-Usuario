import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from src.config_manager import load_config, save_config


config = {}

root = None
ventana_settings = None

entrada_nombre = None
combo_tema = None
combo_idioma = None
entrada_fuente = None

etiqueta_foto = None

etiqueta_titulo = None
etiqueta_nombre = None

barra_menu = None

color_barra = ""
color_letra = ""
foto_perfil = ""


def obtener_texto(clave):

    if config["idioma"] == "en-US":

        textos = {
            "titulo": "Configuration Application",
            "usuario": "User: ",
            "configuracion": "Settings",
            "nombre": "Username:",
            "tema": "Theme:",
            "idioma": "Language:",
            "fuente": "Font size:",
            "color_barra": "Menu bar color:",
            "color_letra": "Text color:",
            "foto": "Profile photo:",
            "seleccionar_foto": "Select photo",
            "guardar": "Save configuration",
            "abrir": "Open Settings",
            "claro": "light",
            "oscuro": "dark"
        }

    else:

        textos = {
            "titulo": "Aplicacion de Configuracion",
            "usuario": "Usuario: ",
            "configuracion": "Configuracion",
            "nombre": "Nombre de usuario:",
            "tema": "Tema:",
            "idioma": "Idioma:",
            "fuente": "Tamaño de fuente:",
            "color_barra": "Color de barra de menu:",
            "color_letra": "Color de letra:",
            "foto": "Foto de perfil:",
            "seleccionar_foto": "Seleccionar foto",
            "guardar": "Guardar configuracion",
            "abrir": "Abrir Settings",
            "claro": "claro",
            "oscuro": "oscuro"
        }

    return textos[clave]


def aplicar_configuracion():

    if config["tema_interfaz"] == "oscuro":
        color_fondo = "#222222"
    else:
        color_fondo = "#ffffff"

    root.configure(
        bg=color_fondo
    )

    etiqueta_titulo.configure(
        bg=color_fondo,
        fg=color_letra,
        font=("Arial", config["tamano_fuente"] + 8, "bold")
    )

    etiqueta_nombre.configure(
        bg=color_fondo,
        fg=color_letra,
        font=("Arial", config["tamano_fuente"])
    )

    barra_menu.configure(
        background=color_barra,
        foreground=color_letra,
        activebackground=color_barra,
        activeforeground=color_letra
    )


def guardar_configuracion():

    global config

    try:

        config["nombre_usuario"] = entrada_nombre.get()
        config["tema_interfaz"] = combo_tema.get()
        config["idioma"] = combo_idioma.get()
        config["tamano_fuente"] = int(entrada_fuente.get())
        config["color_barra_menu"] = color_barra
        config["color_letra"] = color_letra
        config["foto_perfil"] = foto_perfil

        save_config(config)

        aplicar_configuracion()

        actualizar_textos()

        messagebox.showinfo(
            "Configuracion",
            "La configuracion se guardo correctamente."
        )

        ventana_settings.destroy()

    except ValueError:

        messagebox.showerror(
            "Error",
            "El tamaño de fuente debe ser un numero."
        )


def seleccionar_color_barra():

    global color_barra

    resultado = colorchooser.askcolor(
        title="Seleccionar color de barra"
    )

    if resultado[1]:

        color_barra = resultado[1]

        barra_menu.configure(
            background=color_barra,
            activebackground=color_barra
        )

        root.update()


def seleccionar_color_letra():

    global color_letra

    resultado = colorchooser.askcolor(
        title="Seleccionar color de letra"
    )

    if resultado[1]:

        color_letra = resultado[1]

        aplicar_configuracion()


def seleccionar_foto():

    global foto_perfil

    ruta = filedialog.askopenfilename(
        title="Seleccionar foto de perfil",
        filetypes=[
            ("Imagenes", "*.png *.gif"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta:

        foto_perfil = ruta

        etiqueta_foto.configure(
            text="Foto seleccionada:\n" + ruta
        )


def actualizar_textos():

    etiqueta_titulo.configure(
        text=obtener_texto("titulo")
    )

    etiqueta_nombre.configure(
        text=obtener_texto("usuario") + config["nombre_usuario"]
    )


def actualizar_tema():

    tema = combo_tema.get()

    if tema == "oscuro":

        ventana_settings.configure(
            bg="#222222"
        )

    else:

        ventana_settings.configure(
            bg="#ffffff"
        )


def mostrar_settings():

    global ventana_settings
    global entrada_nombre
    global combo_tema
    global combo_idioma
    global entrada_fuente
    global etiqueta_foto

    ventana_settings = tk.Toplevel(root)

    ventana_settings.title(
        obtener_texto("configuracion")
    )

    ventana_settings.geometry("600x650")

    if config["tema_interfaz"] == "oscuro":

        color_fondo = "#222222"
        color_texto = "#ffffff"

    else:

        color_fondo = "#ffffff"
        color_texto = "#000000"

    ventana_settings.configure(
        bg=color_fondo
    )

    tk.Label(
        ventana_settings,
        text=obtener_texto("configuracion"),
        font=("Arial", 20, "bold"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=15)

    tk.Label(
        ventana_settings,
        text=obtener_texto("nombre"),
        bg=color_fondo,
        fg=color_texto
    ).pack()

    entrada_nombre = tk.Entry(
        ventana_settings,
        width=40
    )

    entrada_nombre.insert(
        0,
        config["nombre_usuario"]
    )

    entrada_nombre.pack(pady=5)

    tk.Label(
        ventana_settings,
        text=obtener_texto("tema"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=(10, 0))

    combo_tema = ttk.Combobox(
        ventana_settings,
        values=["claro", "oscuro"],
        state="readonly"
    )

    combo_tema.set(
        config["tema_interfaz"]
    )

    combo_tema.pack()

    combo_tema.bind(
        "<<ComboboxSelected>>",
        lambda evento: actualizar_tema()
    )

    tk.Label(
        ventana_settings,
        text=obtener_texto("idioma"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=(10, 0))

    combo_idioma = ttk.Combobox(
        ventana_settings,
        values=["es-ES", "en-US"],
        state="readonly"
    )

    combo_idioma.set(
        config["idioma"]
    )

    combo_idioma.pack()

    tk.Label(
        ventana_settings,
        text=obtener_texto("fuente"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=(10, 0))

    entrada_fuente = tk.Spinbox(
        ventana_settings,
        from_=8,
        to=30,
        width=10
    )

    entrada_fuente.delete(
        0,
        "end"
    )

    entrada_fuente.insert(
        0,
        config["tamano_fuente"]
    )

    entrada_fuente.pack()

    tk.Label(
        ventana_settings,
        text=obtener_texto("color_barra"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=(10, 0))

    tk.Button(
        ventana_settings,
        text="Seleccionar color",
        command=seleccionar_color_barra
    ).pack()

    tk.Label(
        ventana_settings,
        text=obtener_texto("color_letra"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=(10, 0))

    tk.Button(
        ventana_settings,
        text="Seleccionar color",
        command=seleccionar_color_letra
    ).pack()

    tk.Label(
        ventana_settings,
        text=obtener_texto("foto"),
        bg=color_fondo,
        fg=color_texto
    ).pack(pady=(10, 0))

    if foto_perfil:

        texto_foto = "Foto seleccionada:\n" + foto_perfil

    else:

        texto_foto = "No se ha seleccionado una foto"

    etiqueta_foto = tk.Label(
        ventana_settings,
        text=texto_foto,
        wraplength=500,
        bg=color_fondo,
        fg=color_texto
    )

    etiqueta_foto.pack(pady=5)

    tk.Button(
        ventana_settings,
        text=obtener_texto("seleccionar_foto"),
        command=seleccionar_foto
    ).pack(pady=5)

    tk.Button(
        ventana_settings,
        text=obtener_texto("guardar"),
        command=guardar_configuracion
    ).pack(pady=20)


def main():

    global root
    global config
    global color_barra
    global color_letra
    global foto_perfil
    global etiqueta_titulo
    global etiqueta_nombre
    global barra_menu

    config = load_config()

    color_barra = config["color_barra_menu"]
    color_letra = config["color_letra"]
    foto_perfil = config["foto_perfil"]

    root = tk.Tk()

    root.title(
        obtener_texto("titulo")
    )

    root.geometry("700x450")

    barra_menu = tk.Menu(root)

    menu_archivo = tk.Menu(
        barra_menu,
        tearoff=0
    )

    menu_archivo.add_command(
        label="Salir",
        command=root.destroy
    )

    barra_menu.add_cascade(
        label="Archivo",
        menu=menu_archivo
    )

    menu_edicion = tk.Menu(
        barra_menu,
        tearoff=0
    )

    menu_edicion.add_command(
        label="Configuracion",
        command=mostrar_settings
    )

    barra_menu.add_cascade(
        label="Edicion",
        menu=menu_edicion
    )

    menu_ver = tk.Menu(
        barra_menu,
        tearoff=0
    )

    menu_ver.add_command(
        label="Actualizar",
        command=aplicar_configuracion
    )

    barra_menu.add_cascade(
        label="Ver",
        menu=menu_ver
    )

    menu_settings = tk.Menu(
        barra_menu,
        tearoff=0
    )

    menu_settings.add_command(
        label="Settings",
        command=mostrar_settings
    )

    barra_menu.add_cascade(
        label="Settings",
        menu=menu_settings
    )

    root.config(
        menu=barra_menu
    )

    etiqueta_titulo = tk.Label(
        root,
        text=obtener_texto("titulo"),
        font=("Arial", config["tamano_fuente"] + 8, "bold")
    )

    etiqueta_titulo.pack(
        pady=50
    )

    etiqueta_nombre = tk.Label(
        root,
        text=obtener_texto("usuario") + config["nombre_usuario"],
        font=("Arial", config["tamano_fuente"])
    )

    etiqueta_nombre.pack(
        pady=10
    )

    tk.Button(
        root,
        text=obtener_texto("abrir"),
        command=mostrar_settings
    ).pack(
        pady=20
    )

    aplicar_configuracion()

    root.mainloop()


if __name__ == "__main__":
    main()