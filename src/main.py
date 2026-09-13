import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from src.config_manager import load_config, save_config


def guardar_configuracion():
    config["nombre_usuario"] = entrada_nombre.get()
    config["tema_interfaz"] = combo_tema.get()
    config["idioma"] = combo_idioma.get()
    config["tamano_fuente"] = int(entrada_fuente.get())
    config["color_barra_menu"] = color_barra
    config["color_letra"] = color_letra
    config["foto_perfil"] = foto_perfil

    save_config(config)

    aplicar_configuracion()

    messagebox.showinfo(
        "Configuracion",
        "La configuracion se guardo correctamente."
    )


def aplicar_configuracion():

    if config["tema_interfaz"] == "oscuro":
        color_fondo = "#222222"
        color_texto = "#ffffff"
    else:
        color_fondo = "#ffffff"
        color_texto = "#000000"

    root.configure(bg=color_fondo)

    etiqueta_nombre.configure(
        bg=color_fondo,
        fg=color_texto
    )

    etiqueta_titulo.configure(
        bg=color_fondo,
        fg=color_texto
    )


def seleccionar_color_barra():
    global color_barra

    resultado = colorchooser.askcolor(
        title="Seleccionar color de barra"
    )

    if resultado[1]:
        color_barra = resultado[1]
        boton_color_barra.configure(bg=color_barra)


def seleccionar_color_letra():
    global color_letra

    resultado = colorchooser.askcolor(
        title="Seleccionar color de letra"
    )

    if resultado[1]:
        color_letra = resultado[1]
        boton_color_letra.configure(bg=color_letra)


def seleccionar_foto():
    global foto_perfil

    ruta = filedialog.askopenfilename(
        title="Seleccionar foto de perfil",
        filetypes=[
            ("Imagenes", "*.png *.jpg *.jpeg"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta:
        foto_perfil = ruta
        etiqueta_foto.configure(
            text="Foto seleccionada"
        )


def mostrar_settings():

    global entrada_nombre
    global combo_tema
    global combo_idioma
    global entrada_fuente

    
    ventana_settings = tk.Toplevel(root)

    ventana_settings.title("Settings")
    ventana_settings.geometry("500x500")

    tk.Label(
        ventana_settings,
        text="Configuracion",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        ventana_settings,
        text="Nombre de usuario:"
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
        text="Tema:"
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

    tk.Label(
        ventana_settings,
        text="Idioma:"
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
        text="Tamaño de fuente:"
    ).pack(pady=(10, 0))

    entrada_fuente = tk.Spinbox(
        ventana_settings,
        from_=8,
        to=30,
        width=10
    )

    entrada_fuente.delete(0, "end")
    entrada_fuente.insert(
        0,
        config["tamano_fuente"]
    )

    entrada_fuente.pack()

    tk.Label(
        ventana_settings,
        text="Color de barra de menu:"
    ).pack(pady=(10, 0))

    boton_color_barra = tk.Button(
        ventana_settings,
        text="Seleccionar color",
        command=seleccionar_color_barra,
        bg=color_barra
    )

    boton_color_barra.pack()

    tk.Label(
        ventana_settings,
        text="Color de letra:"
    ).pack(pady=(10, 0))

    boton_color_letra = tk.Button(
        ventana_settings,
        text="Seleccionar color",
        command=seleccionar_color_letra,
        bg=color_letra
    )

    boton_color_letra.pack()

    tk.Label(
        ventana_settings,
        text="Foto de perfil:"
    ).pack(pady=(10, 0))

    etiqueta_foto = tk.Label(
        ventana_settings,
        text="No se ha seleccionado una foto"
    )

    etiqueta_foto.pack()

    tk.Button(
        ventana_settings,
        text="Seleccionar foto",
        command=seleccionar_foto
    ).pack(pady=5)

    tk.Button(
        ventana_settings,
        text="Guardar configuracion",
        command=guardar_configuracion
    ).pack(pady=20)


def main():

    global root
    global config
    global color_barra
    global color_letra
    global foto_perfil
    global entrada_nombre
    global combo_tema
    global combo_idioma
    global entrada_fuente
    global etiqueta_nombre
    global etiqueta_titulo

    config = load_config()

    color_barra = config["color_barra_menu"]
    color_letra = config["color_letra"]
    foto_perfil = config["foto_perfil"]

    root = tk.Tk()

    root.title("Aplicacion de Configuracion")
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
        label="Abrir Settings",
        command=mostrar_settings
    )

    barra_menu.add_cascade(
        label="Settings",
        menu=menu_settings
    )

    root.config(menu=barra_menu)

    etiqueta_titulo = tk.Label(
        root,
        text="Aplicacion de Configuracion",
        font=("Arial", 22, "bold")
    )

    etiqueta_titulo.pack(pady=50)

    etiqueta_nombre = tk.Label(
        root,
        text="Usuario: " + config["nombre_usuario"],
        font=("Arial", 14)
    )

    etiqueta_nombre.pack(pady=10)

    tk.Button(
        root,
        text="Abrir Settings",
        command=mostrar_settings
    ).pack(pady=20)

    aplicar_configuracion()

    root.mainloop()


if __name__ == "__main__":
    main()