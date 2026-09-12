import tkinter as tk
from src.config_manager import load_config, save_config


def main():
    config = load_config()

    config["nombre_usuario"] = "María Ñandú"
    save_config(config)

    root = tk.Tk()
    root.title("Config App")
    root.geometry("600x400")
    tk.Label(
        root,
        text=f"Config App - commit inicial\nUsuario: {config['nombre_usuario']}",
    ).pack(pady=20)
    root.mainloop()


if __name__ == "__main__":
    main()
