import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from PIL import Image, ImageTk

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

imagen_perfil = None

panel_izquierdo = None
panel_derecho = None
boton_settings = None
boton_archivo = None
boton_edicion = None
boton_ver = None
etiqueta_usuario = None
etiqueta_bienvenida = None
etiqueta_descripcion = None


class ToolTip:

    def __init__(self, widget, text, delay=500):

        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip = None
        self._job = None

        widget.bind(
            "<Enter>",
            self._schedule,
            add="+"
        )

        widget.bind(
            "<Leave>",
            self._hide,
            add="+"
        )

        widget.bind(
            "<ButtonPress>",
            self._hide,
            add="+"
        )


    def _schedule(self, _event=None):

        self._cancel()

        self._job = self.widget.after(
            self.delay,
            self._show
        )


    def _cancel(self):

        if self._job is not None:

            self.widget.after_cancel(
                self._job
            )

            self._job = None


    def _show(self):

        if self.tip is not None:
            return

        x = (
            self.widget.winfo_rootx()
            + 12
        )

        y = (
            self.widget.winfo_rooty()
            + self.widget.winfo_height()
            + 6
        )

        self.tip = tk.Toplevel(
            self.widget
        )

        self.tip.wm_overrideredirect(
            True
        )

        self.tip.wm_geometry(
            f"+{x}+{y}"
        )

        tk.Label(
            self.tip,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padx=6,
            pady=3,
        ).pack()


    def _hide(self, _event=None):

        self._cancel()

        if self.tip is not None:

            self.tip.destroy()
            self.tip = None


def obtener_texto(clave):

    if config["idioma"] == "en-US":

        textos = {
            "titulo": "Welcome!",
            "usuario": "User: ",
            "configuracion": "Settings",
            "nombre": "Username:",
            "tema": "Theme:",
            "idioma": "Language:",
            "fuente": "Font size:",
            "color_barra": "Menu bar color:",
            "color_letra": "Text color:",
            "foto": "Profile photo:",
            "seleccionar_foto": "Select picture",
            "guardar": "Save configuration",
            "claro": "light",
            "oscuro": "dark",
            "descripcion": "With this application you can manage your settings and customize your experience",
            "archivo": "File",
            "edicion": "Edit",
            "ver": "View"
        }

    else:

        textos = {
            "titulo": "¡Bienvenido!",
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
            "claro": "claro",
            "oscuro": "oscuro",
            "descripcion": "Con esta aplicación puedes gestionar tu configuración y personalizar tu experiencia",
            "archivo": "Archivo",
            "edicion": "Edición",
            "ver": "Ver"
        }

    return textos[clave]


def cargar_foto_perfil():

    global imagen_perfil

    if foto_perfil:

        try:

            imagen = Image.open(
                foto_perfil
            )

            imagen = imagen.resize(
                (60, 60)
            )

            imagen_perfil = ImageTk.PhotoImage(
                imagen
            )

            etiqueta_usuario.configure(
                image=imagen_perfil,
                text=""
            )

            return

        except Exception:
            pass

    try:

        imagen = Image.open(
            "image.png"
        )

        imagen = imagen.resize(
            (60, 60)
        )

        imagen_perfil = ImageTk.PhotoImage(
            imagen
        )

        etiqueta_usuario.configure(
            image=imagen_perfil,
            text=""
        )

    except Exception:

        etiqueta_usuario.configure(
            image="",
            text="👤",
            font=("Arial", 25)
        )


def aplicar_configuracion():

    if config["tema_interfaz"] == "oscuro":
        color_fondo = "#222222"
    else:
        color_fondo = "#ffffff"

    panel_derecho.configure(
        bg=color_fondo
    )

    etiqueta_bienvenida.configure(
        bg=color_fondo,
        fg=color_letra,
        font=("Arial", config["tamano_fuente"] + 8, "bold")
    )

    etiqueta_descripcion.configure(
        bg=color_fondo
    )

    etiqueta_usuario.configure(
        bg="#171c26",
        fg=color_letra,
        font=("Arial", config["tamano_fuente"], "bold")
    )

    panel_izquierdo.configure(
        bg=color_barra
    )

    boton_settings.configure(
        bg=color_barra,
        fg=color_letra
    )

    boton_archivo.configure(
        bg=color_barra,
        fg=color_letra
    )

    boton_edicion.configure(
        bg=color_barra,
        fg=color_letra
    )

    boton_ver.configure(
        bg=color_barra,
        fg=color_letra
    )


def actualizar_textos():

    etiqueta_bienvenida.configure(
        text=obtener_texto("titulo")
    )

    etiqueta_nombre.configure(
        text=config["nombre_usuario"]
    )

    etiqueta_descripcion.configure(
        text=obtener_texto("descripcion")
    )

    boton_archivo.configure(
        text=obtener_texto("archivo")
    )

    boton_edicion.configure(
        text=obtener_texto("edicion")
    )

    boton_ver.configure(
        text=obtener_texto("ver")
    )
    
    boton_settings.configure(
    text=obtener_texto("configuracion")
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

        cargar_foto_perfil()

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

        if etiqueta_foto is not None:

            try:

                if etiqueta_foto.winfo_exists():

                    etiqueta_foto.configure(
                        text="Foto seleccionada:\n" + ruta
                    )

            except tk.TclError:

                pass



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

    global panel_izquierdo
    global panel_derecho

    global boton_settings
    global boton_archivo
    global boton_edicion
    global boton_ver

    global etiqueta_usuario
    global etiqueta_bienvenida
    global etiqueta_descripcion

    config = load_config()

    color_barra = config["color_barra_menu"]
    color_letra = config["color_letra"]
    foto_perfil = config["foto_perfil"]

    root = tk.Tk()

    root.title(
        "Main"
    )

    root.geometry(
        "520x380"
    )

    root.resizable(
        False,
        False
    )

    # Panel izquierdo

    panel_izquierdo = tk.Frame(
        root,
        bg="#171c26"
    )

    panel_izquierdo.place(
        x=0,
        y=0,
        width=190,
        height=370
    )

    barra_menu = panel_izquierdo

    # Panel derecho

    if config["tema_interfaz"] == "oscuro":
        color_fondo = "#222222"
    else:
        color_fondo = "#f8fafc"

    panel_derecho = tk.Frame(
        root,
        bg=color_fondo
    )

    panel_derecho.place(
        x=190,
        y=0,
        width=330,
        height=370
    )

    # Foto de usuario

    etiqueta_usuario = tk.Label(
        panel_izquierdo,
        text="👤",
        bg=color_barra,
        fg=color_letra,
        font=("Arial", 25)
    )

    etiqueta_usuario.place(
        x=30,
        y=50,
        width=60,
        height=60
    )

    ToolTip(
        etiqueta_usuario,
        "Bonita Foto ;3"
    )

    # Nombre

    etiqueta_nombre = tk.Label(
        panel_izquierdo,
        text=config["nombre_usuario"],
        bg=color_barra,
        fg=color_letra,
        font=("Helvetica", 10, "bold")
    )

    etiqueta_nombre.place(
        x=90,
        y=60,
        width=90,
        height=30
    )

    # Settings

    boton_settings = tk.Button(
        panel_izquierdo,
        text="Configuración",
        command=mostrar_settings,
        fg=color_letra,
        bg=color_barra,
        activeforeground=color_letra,
        activebackground=color_barra,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_settings.place(
        x=47,
        y=140,
        width=96,
        height=32
    )

    # Archivo

    boton_archivo = tk.Button(
        panel_izquierdo,
        text="Archivo",
        command=lambda: None,
        fg=color_letra,
        bg=color_barra,
        activeforeground=color_letra,
        activebackground=color_barra,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_archivo.place(
        x=47,
        y=190,
        width=96,
        height=32
    )

    # Edicion

    boton_edicion = tk.Button(
        panel_izquierdo,
        text="Edición",
        command=lambda: messagebox.showinfo(
            "Edición",
            "Hello!"
        ),
        fg=color_letra,
        bg=color_barra,
        activeforeground=color_letra,
        activebackground=color_barra,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_edicion.place(
        x=47,
        y=240,
        width=96,
        height=32
    )

    # Ver

    boton_ver = tk.Button(
        panel_izquierdo,
        text="Ver",
        command=lambda: messagebox.showinfo(
            "Ver",
            "Hello!"
        ),
        fg=color_letra,
        bg=color_barra,
        activeforeground=color_letra,
        activebackground=color_barra,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_ver.place(
        x=47,
        y=290,
        width=96,
        height=32
    )

    # Bienvenida

    etiqueta_bienvenida = tk.Label(
        panel_derecho,
        text="¡Bienvenido!",
        bg=color_fondo,
        fg=color_letra,
        font=("Helvetica", 19, "bold")
    )

    etiqueta_bienvenida.place(
        x=50,
        y=75,
        width=230,
        height=50
    )

    # Descripcion

    etiqueta_descripcion = tk.Label(
        panel_derecho,
        text="Con esta aplicación puedes gestionar tu configuración y personalizar tu experiencia",
        bg=color_fondo,
        fg="#777f95",
        wraplength=220
    )

    etiqueta_descripcion.place(
        x=50,
        y=112,
        width=230,
        height=60
    )

    cargar_foto_perfil()

    aplicar_configuracion()

    actualizar_textos()

    root.mainloop()


if __name__ == "__main__":
    main()