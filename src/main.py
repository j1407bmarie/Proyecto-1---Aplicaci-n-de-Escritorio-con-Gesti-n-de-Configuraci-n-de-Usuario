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

barra_menu = None

color_barra = ""
foto_perfil = ""

imagen_perfil = None

panel_izquierdo = None
panel_derecho = None

boton_settings = None
boton_archivo = None
boton_edicion = None
boton_ver = None

etiqueta_usuario = None
etiqueta_nombre = None
etiqueta_bienvenida = None
etiqueta_descripcion = None

combo_elemento = None
spin_tamano = None
boton_color_texto = None
check_negrita = None
check_cursiva = None
boton_color_barra = None

elemento_seleccionado = "bienvenida"
color_texto_seleccionado = "#ffffff"


ESTILOS_DEFAULT = {
    "bienvenida": {
        "fuente": "Arial",
        "tamano": 19,
        "color": "#5865f2",
        "negrita": True,
        "cursiva": False
    },
    "descripcion": {
        "fuente": "Arial",
        "tamano": 11,
        "color": "#777f95",
        "negrita": False,
        "cursiva": False
    },
    "nombre_usuario": {
        "fuente": "Helvetica",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "configuracion": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "archivo": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "edicion": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "ver": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    }
}


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

        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6

        self.tip = tk.Toplevel(self.widget)

        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")

        tk.Label(
            self.tip,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padx=6,
            pady=3
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
            "ver": "View",
            "personalizacion": "Text customization",
            "elemento": "Element:",
            "tamano": "Size:",
            "color": "Text color:",
            "negrita": "Bold",
            "cursiva": "Italic",
            "aplicar": "Apply style",
            "bienvenida": "Welcome text",
            "descripcion_elemento": "Description",
            "nombre_elemento": "Username",
            "configuracion_elemento": "Settings button",
            "archivo_elemento": "File button",
            "edicion_elemento": "Edit button",
            "ver_elemento": "View button"
        }

    else:

        textos = {
            "titulo": "¡Bienvenido!",
            "usuario": "Usuario: ",
            "configuracion": "Configuración",
            "nombre": "Nombre de usuario:",
            "tema": "Tema:",
            "idioma": "Idioma:",
            "fuente": "Tamaño de fuente:",
            "color_barra": "Color de barra de menú:",
            "color_letra": "Color de letra:",
            "foto": "Foto de perfil:",
            "seleccionar_foto": "Seleccionar foto",
            "guardar": "Guardar configuración",
            "claro": "claro",
            "oscuro": "oscuro",
            "descripcion": "Con esta aplicación puedes gestionar tu configuración y personalizar tu experiencia",
            "archivo": "Archivo",
            "edicion": "Edición",
            "ver": "Ver",
            "personalizacion": "Personalización de textos",
            "elemento": "Elemento:",
            "tamano": "Tamaño:",
            "color": "Color de texto:",
            "negrita": "Negrita",
            "cursiva": "Cursiva",
            "aplicar": "Aplicar estilo",
            "bienvenida": "Texto de bienvenida",
            "descripcion_elemento": "Descripción",
            "nombre_elemento": "Nombre de usuario",
            "configuracion_elemento": "Botón Configuración",
            "archivo_elemento": "Botón Archivo",
            "edicion_elemento": "Botón Edición",
            "ver_elemento": "Botón Ver"
        }

    return textos[clave]


def obtener_estilos():

    if "estilos_textos" not in config:

        config["estilos_textos"] = {}

    for clave, estilo in ESTILOS_DEFAULT.items():

        if clave not in config["estilos_textos"]:

            config["estilos_textos"][clave] = estilo.copy()

        else:

            for propiedad, valor in estilo.items():

                if propiedad not in config["estilos_textos"][clave]:

                    config["estilos_textos"][clave][propiedad] = valor

    return config["estilos_textos"]


def crear_fuente(elemento):

    estilos = obtener_estilos()
    estilo = estilos[elemento]

    tipo = estilo["fuente"]
    tamano = estilo["tamano"]

    if estilo["negrita"] and estilo["cursiva"]:

        tipo_estilo = "bold italic"

    elif estilo["negrita"]:

        tipo_estilo = "bold"

    elif estilo["cursiva"]:

        tipo_estilo = "italic"

    else:

        tipo_estilo = "normal"

    return (
        tipo,
        tamano,
        tipo_estilo
    )


def aplicar_estilo_widget(widget, elemento):

    estilos = obtener_estilos()
    estilo = estilos[elemento]

    widget.configure(
        font=crear_fuente(elemento),
        fg=estilo["color"]
    )


def cargar_foto_perfil():

    global imagen_perfil

    if foto_perfil:

        try:

            imagen = Image.open(foto_perfil)
            imagen = imagen.resize((60, 60))

            imagen_perfil = ImageTk.PhotoImage(imagen)

            etiqueta_usuario.configure(
                image=imagen_perfil,
                text=""
            )

            return

        except Exception:
            pass

    try:

        imagen = Image.open("image.png")
        imagen = imagen.resize((60, 60))

        imagen_perfil = ImageTk.PhotoImage(imagen)

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

    estilos = obtener_estilos()

    if config["tema_interfaz"] == "oscuro":

        color_fondo = "#222222"

    else:

        color_fondo = "#ffffff"

    panel_derecho.configure(
        bg=color_fondo
    )

    panel_izquierdo.configure(
        bg=color_barra
    )

    etiqueta_usuario.configure(
        bg=color_barra
    )

    etiqueta_nombre.configure(
        bg=color_barra
    )

    etiqueta_bienvenida.configure(
        bg=color_fondo
    )

    etiqueta_descripcion.configure(
        bg=color_fondo
    )

    boton_settings.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    boton_archivo.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    boton_edicion.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    boton_ver.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    aplicar_estilo_widget(
        etiqueta_bienvenida,
        "bienvenida"
    )

    aplicar_estilo_widget(
        etiqueta_descripcion,
        "descripcion"
    )

    aplicar_estilo_widget(
        etiqueta_nombre,
        "nombre_usuario"
    )

    aplicar_estilo_widget(
        boton_settings,
        "configuracion"
    )

    aplicar_estilo_widget(
        boton_archivo,
        "archivo"
    )

    aplicar_estilo_widget(
        boton_edicion,
        "edicion"
    )

    aplicar_estilo_widget(
        boton_ver,
        "ver"
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

    boton_settings.configure(
        text=obtener_texto("configuracion")
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


def guardar_configuracion():
    global config

    try:
        # Guardar los datos generales
        config["nombre_usuario"] = entrada_nombre.get()
        config["tema_interfaz"] = combo_tema.get()
        config["idioma"] = combo_idioma.get()
        config["color_barra_menu"] = color_barra
        config["foto_perfil"] = foto_perfil

        # Guardar el estilo que se esté editando actualmente
        guardar_estilo_actual()

        # Guardar todos los cambios en el archivo JSON
        save_config(config)

        # Aplicar los cambios a la ventana principal
        aplicar_configuracion()
        actualizar_textos()
        cargar_foto_perfil()

        messagebox.showinfo(
            "Configuración",
            "Todos los cambios se guardaron correctamente."
        )

        cerrar_settings()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Verifica que los valores ingresados sean correctos."
        )

    except tk.TclError:
        messagebox.showerror(
            "Error",
            "La ventana de configuración ya no está disponible."
        )

def seleccionar_color_barra():

    global color_barra

    resultado = colorchooser.askcolor(
        title="Seleccionar color de barra"
    )

    if resultado[1]:

        color_barra = resultado[1]

        barra_menu.configure(
            background=color_barra
        )

        aplicar_configuracion()


def seleccionar_color_texto():

    global color_texto_seleccionado

    resultado = colorchooser.askcolor(
        title="Seleccionar color de texto"
    )

    if resultado[1]:

        color_texto_seleccionado = resultado[1]

        boton_color_texto.configure(
            bg=color_texto_seleccionado
        )


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
        config["color_fondo"] = "#202124"
        config["color_panel"] = "#292a2d"
        config["color_tarjeta"] = "#303134"
    else:
        config["color_fondo"] = "#f4f6fb"
        config["color_panel"] = "#ffffff"
        config["color_tarjeta"] = "#ffffff"

    aplicar_configuracion()

def nombres_elementos():

    return [
        obtener_texto("bienvenida"),
        obtener_texto("descripcion_elemento"),
        obtener_texto("nombre_elemento"),
        obtener_texto("configuracion_elemento"),
        obtener_texto("archivo_elemento"),
        obtener_texto("edicion_elemento"),
        obtener_texto("ver_elemento")
    ]


def claves_elementos():

    return [
        "bienvenida",
        "descripcion",
        "nombre_usuario",
        "configuracion",
        "archivo",
        "edicion",
        "ver"
    ]


def cargar_estilo_seleccionado():

    global elemento_seleccionado
    global color_texto_seleccionado

    posicion = combo_elemento.current()

    if posicion < 0:
        return

    elemento_seleccionado = claves_elementos()[posicion]

    estilo = obtener_estilos()[elemento_seleccionado]

    spin_tamano.delete(
        0,
        "end"
    )

    spin_tamano.insert(
        0,
        estilo["tamano"]
    )

    color_texto_seleccionado = estilo["color"]

    boton_color_texto.configure(
        bg=color_texto_seleccionado
    )

    check_negrita.set(
        estilo["negrita"]
    )

    check_cursiva.set(
        estilo["cursiva"]
    )


def guardar_estilo_actual():

    if combo_elemento is None:
        return

    try:

        tamano = int(spin_tamano.get())

    except ValueError:

        return

    estilos = obtener_estilos()

    estilos[elemento_seleccionado]["tamano"] = tamano
    estilos[elemento_seleccionado]["color"] = color_texto_seleccionado
    estilos[elemento_seleccionado]["negrita"] = check_negrita.get()
    estilos[elemento_seleccionado]["cursiva"] = check_cursiva.get()


def aplicar_estilo_seleccionado():

    guardar_estilo_actual()

    aplicar_configuracion()

    messagebox.showinfo(
        "Configuración",
        "El estilo se aplicó correctamente."
    )

def cerrar_settings():

    global ventana_settings

    if ventana_settings is not None:

        ventana_settings.grab_release()
        ventana_settings.destroy()
        ventana_settings = None
        

def mostrar_settings():

    global ventana_settings
    global entrada_nombre
    global combo_tema
    global combo_idioma
    global entrada_fuente
    global etiqueta_foto
    global boton_color_barra

    global combo_elemento
    global spin_tamano
    global boton_color_texto
    global check_negrita
    global check_cursiva

    if ventana_settings is not None:

        if ventana_settings.winfo_exists():

            ventana_settings.lift()
            ventana_settings.focus_force()

            return

    ventana_settings = tk.Toplevel(root)

    ventana_settings.transient(root)
    ventana_settings.grab_set()

    ventana_settings.protocol(
        "WM_DELETE_WINDOW",
        cerrar_settings
    )

    ventana_settings.title(
        obtener_texto("configuracion")
    )

    # Mismo ancho que la ventana principal
    ventana_settings.geometry("520x520")
    ventana_settings.resizable(False, False)

    if config["tema_interfaz"] == "oscuro":

        color_fondo = "#222222"
        color_texto = "#ffffff"

    else:

        color_fondo = "#ffffff"
        color_texto = "#000000"

    ventana_settings.configure(
        bg=color_fondo
    )

    # titulo de la ventana de configuración

    tk.Label(
        ventana_settings,
        text=obtener_texto("configuracion"),
        font=("Arial", 20, "bold"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(18, 12)
    )

    # contenedor principal

    marco_principal = tk.Frame(
        ventana_settings,
        bg=color_fondo
    )

    marco_principal.pack(
        fill="x",
        padx=25
    )

    columna_izquierda = tk.Frame(
        marco_principal,
        bg=color_fondo
    )

    columna_izquierda.grid(
        row=0,
        column=0,
        padx=(0, 15),
        sticky="n"
    )

    columna_derecha = tk.Frame(
        marco_principal,
        bg=color_fondo
    )

    columna_derecha.grid(
        row=0,
        column=1,
        padx=(15, 0),
        sticky="n"
    )

    # CONFIGURACION GENERAL

    tk.Label(
        columna_izquierda,
        text=obtener_texto("nombre"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(5, 2)
    )

    entrada_nombre = tk.Entry(
        columna_izquierda,
        width=22
    )

    entrada_nombre.insert(
        0,
        config["nombre_usuario"]
    )

    entrada_nombre.pack(
        pady=4
    )

    # tema (claro u oscuro)

    tk.Label(
        columna_izquierda,
        text=obtener_texto("tema"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    combo_tema = ttk.Combobox(
        columna_izquierda,
        values=["claro", "oscuro"],
        state="readonly",
        width=19
    )

    combo_tema.set(
        config["tema_interfaz"]
    )

    combo_tema.pack()

    combo_tema.bind(
        "<<ComboboxSelected>>",
        lambda evento: actualizar_tema()
    )

    # cambiar idioma

    tk.Label(
        columna_izquierda,
        text=obtener_texto("idioma"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    combo_idioma = ttk.Combobox(
        columna_izquierda,
        values=["es-ES", "en-US"],
        state="readonly",
        width=19
    )

    combo_idioma.set(
        config["idioma"]
    )

    combo_idioma.pack()

    # personalizar color de la barra de menú

    tk.Label(
        columna_izquierda,
        text=obtener_texto("color_barra"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(10, 2)
    )

    boton_color_barra = tk.Button(
        columna_izquierda,
        text="      ",
        bg=color_barra,
        width=19,
        command=seleccionar_color_barra
    )

    boton_color_barra.pack(
        pady=4
    )

    # escoger foto de perfil

    tk.Label(
        columna_izquierda,
        text=obtener_texto("foto"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(10, 2)
    )

    if foto_perfil:

        texto_foto = (
            "Foto seleccionada:\n"
            + foto_perfil
        )

    else:

        texto_foto = (
            "No se ha seleccionado una foto"
        )

    etiqueta_foto = tk.Label(
        columna_izquierda,
        text=texto_foto,
        wraplength=180,
        bg=color_fondo,
        fg=color_texto
    )

    etiqueta_foto.pack(
        pady=4
    )

    tk.Button(
        columna_izquierda,
        text=obtener_texto("seleccionar_foto"),
        command=seleccionar_foto,
        width=19
    ).pack(
        pady=4
    )

    # Personalización de textos

    tk.Label(
        columna_derecha,
        text=obtener_texto("personalizacion"),
        font=("Arial", 14, "bold"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(5, 12)
    )

    # elementos de la combo box

    tk.Label(
        columna_derecha,
        text=obtener_texto("elemento"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=2
    )

    combo_elemento = ttk.Combobox(
        columna_derecha,
        values=nombres_elementos(),
        state="readonly",
        width=19
    )

    combo_elemento.pack(
        pady=4
    )

    combo_elemento.current(0)

    combo_elemento.bind(
        "<<ComboboxSelected>>",
        lambda evento: cargar_estilo_seleccionado()
    )

    # tamaño de fuente

    tk.Label(
        columna_derecha,
        text=obtener_texto("tamano"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    spin_tamano = tk.Spinbox(
        columna_derecha,
        from_=8,
        to=40,
        width=8
    )

    spin_tamano.pack(
        pady=4
    )

    # cambiar color del texto

    tk.Label(
        columna_derecha,
        text=obtener_texto("color"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    boton_color_texto = tk.Button(
        columna_derecha,
        text="      ",
        bg="#ffffff",
        width=10,
        command=seleccionar_color_texto
    )

    boton_color_texto.pack(
        pady=4
    )

    # negrita

    check_negrita = tk.BooleanVar()

    tk.Checkbutton(
        columna_derecha,
        text=obtener_texto("negrita"),
        variable=check_negrita,
        bg=color_fondo,
        fg=color_texto,
        selectcolor=color_fondo,
        activebackground=color_fondo,
        activeforeground=color_texto
    ).pack(
        pady=(8, 2)
    )

    #cursiva

    check_cursiva = tk.BooleanVar()

    tk.Checkbutton(
        columna_derecha,
        text=obtener_texto("cursiva"),
        variable=check_cursiva,
        bg=color_fondo,
        fg=color_texto,
        selectcolor=color_fondo,
        activebackground=color_fondo,
        activeforeground=color_texto
    ).pack(
        pady=2
    )

    #Aplicar estilo seleccionado

    tk.Button(
        columna_derecha,
        text=obtener_texto("aplicar"),
        command=aplicar_estilo_seleccionado,
        width=19
    ).pack(
        pady=12
    )

    cargar_estilo_seleccionado()

    
    # Guradar configuración
    

    tk.Button(
        ventana_settings,
        text=obtener_texto("guardar"),
        command=guardar_configuracion,
        width=28
    ).pack(
        pady=(12, 18)
    )


def mostrar_menu_archivo(): # menu simulado de archivo

    menu = tk.Menu(
        root,
        tearoff=0
    )

    menu.add_command(
        label="Nuevo",
        command=lambda: messagebox.showinfo(
            "Archivo",
            "Opción Nuevo seleccionada."
        )
    )

    menu.add_command(
        label="Abrir",
        command=lambda: messagebox.showinfo(
            "Archivo",
            "Opción Abrir seleccionada."
        )
    )

    menu.add_command(
        label="Guardar",
        command=lambda: messagebox.showinfo(
            "Archivo",
            "Opción Guardar seleccionada."
        )
    )

    menu.add_separator()

    menu.add_command(
        label="Salir",
        command=lambda: messagebox.showinfo(
            "Archivo",
            "Opción Salir seleccionada."
        )
    )

    menu.post(
        boton_archivo.winfo_rootx(),
        boton_archivo.winfo_rooty() + boton_archivo.winfo_height()
    )


def main():

    global root
    global config
    global color_barra
    global foto_perfil

    global panel_izquierdo
    global panel_derecho
    global barra_menu

    global boton_settings
    global boton_archivo
    global boton_edicion
    global boton_ver

    global etiqueta_usuario
    global etiqueta_nombre
    global etiqueta_bienvenida
    global etiqueta_descripcion

    config = load_config()

    obtener_estilos()

    color_barra = config.get("color_barra_menu", "#171c26")
    foto_perfil = config["foto_perfil"]

    root = tk.Tk()

    root.title("Main")
    root.geometry("520x380")
    root.resizable(False, False)

    panel_izquierdo = tk.Frame(
        root,
        bg=color_barra
    )

    panel_izquierdo.place(
        x=0,
        y=0,
        width=190,
        height=370
    )

    barra_menu = panel_izquierdo

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

    etiqueta_usuario = tk.Label(
        panel_izquierdo,
        text="👤",
        bg=color_barra,
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

    etiqueta_nombre = tk.Label(
        panel_izquierdo,
        text=config["nombre_usuario"],
        bg=color_barra
    )

    etiqueta_nombre.place(
        x=90,
        y=60,
        width=90,
        height=30
    )

    boton_settings = tk.Button(
        panel_izquierdo,
        text="Configuración",
        command=mostrar_settings,
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

    boton_archivo = tk.Button(
        panel_izquierdo,
        text="Archivo",
        command=mostrar_menu_archivo,
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

    boton_edicion = tk.Button(
        panel_izquierdo,
        text="Edición",
        command=lambda: messagebox.showinfo(
            "Edición",
            "Abriendo Edición..."
        ),
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

    boton_ver = tk.Button(
        panel_izquierdo,
        text="Ver",
        command=lambda: messagebox.showinfo(
            "Ver",
            "Abriendo Ver..."
        ),
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

    etiqueta_bienvenida = tk.Label(
        panel_derecho,
        text="¡Bienvenido!",
        bg=color_fondo
    )

    etiqueta_bienvenida.place(
        x=50,
        y=75,
        width=230,
        height=50
    )

    etiqueta_descripcion = tk.Label(
        panel_derecho,
        text="Con esta aplicación puedes gestionar tu configuración y personalizar tu experiencia",
        bg=color_fondo,
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