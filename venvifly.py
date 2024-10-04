import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess

def seleccionar_ruta():
    ruta = filedialog.askdirectory(initialdir=ruta_predeterminada)
    if ruta:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, ruta)

def crear_script_activacion(ruta_completa, ruta_entorno, nombre_entorno):
    if os.name == 'nt':  # Para Windows
        ruta_script = os.path.join(ruta_entorno, f"activate_{nombre_entorno}.bat")
        contenido_script = f"@echo off\ncall \"{ruta_completa}\\Scripts\\activate.bat\"\ncmd"
    else:  # Para Unix/MacOS
        ruta_script = os.path.join(ruta_entorno, f"activate_{nombre_entorno}.sh")
        contenido_script = f"#!/bin/bash\nsource \"{ruta_completa}/bin/activate\"\nexec bash"

    with open(ruta_script, "w") as script:
        script.write(contenido_script)

    if os.name != 'nt':
        os.chmod(ruta_script, 0o755)

def actualizar_progreso(valor):
    progress_bar['value'] = valor
    root.update_idletasks()

def crear_entorno_virtual():
    nombre_entorno = entry_nombre.get() or "venv"
    ruta_entorno = entry_ruta.get()

    if not ruta_entorno:
        messagebox.showwarning("Advertencia", "Por favor selecciona una ruta.")
        return

    ruta_completa = os.path.join(ruta_entorno, nombre_entorno)
    comando = f"python -m venv \"{ruta_completa}\""

    try:
        actualizar_progreso(10)
        subprocess.run(comando, check=True, shell=True)
        actualizar_progreso(50)
        crear_script_activacion(ruta_completa, ruta_entorno, nombre_entorno)
        actualizar_progreso(100)
        messagebox.showinfo("Éxito", f"Entorno virtual '{nombre_entorno}' creado correctamente en {ruta_completa}.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo crear el entorno virtual. {e}")

def abrir_entorno_virtual():
    nombre_entorno = entry_nombre.get() or "venv"
    ruta_entorno = entry_ruta.get()

    if not ruta_entorno or not os.path.exists(os.path.join(ruta_entorno, nombre_entorno)):
        messagebox.showwarning("Advertencia", "Por favor asegúrate de que el entorno existe.")
        return

    ruta_completa = os.path.join(ruta_entorno, nombre_entorno)

    if os.name == 'nt':
        # Abrir cmd en el directorio del venv y activar el entorno
        comando = f'start "" cmd /K "cd /d \"{ruta_completa}\" && \"{ruta_completa}\\Scripts\\activate\""'
    else:
        # Para Unix/MacOS
        comando = f'gnome-terminal -- bash -c "cd \\"{ruta_completa}\\"; source bin/activate; exec bash"'

    try:
        subprocess.run(comando, shell=True)
        # Eliminamos el mensaje de confirmación
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo activar el entorno virtual. {e}")

def resource_path(relative_path):
    """ Obtener el camino absoluto del archivo, compatible con PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def obtener_ruta_ejecucion():
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Venvifly")

# Establecer el ícono de la ventana y barra de tareas
icon_path = resource_path("venvifly_icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)
else:
    print(f"Archivo de ícono no encontrado en: {icon_path}")

# Obtener la ruta desde donde se está ejecutando el script o el acceso directo
ruta_ejecucion = obtener_ruta_ejecucion()
ruta_predeterminada = os.path.abspath(os.path.join(ruta_ejecucion, '..'))

# Establecer el tamaño de la ventana
root.geometry("300x300")

# Etiqueta y campo de texto para ingresar la ruta del entorno virtual
label_ruta = tk.Label(root, text="Ruta para el Entorno Virtual:")
label_ruta.pack(padx=10, pady=5)

entry_ruta = tk.Entry(root, width=40)
entry_ruta.insert(0, ruta_predeterminada)
entry_ruta.pack(padx=10, pady=5)

# Botón para seleccionar la ruta
boton_ruta = tk.Button(root, text="Seleccionar Ruta", command=seleccionar_ruta)
boton_ruta.pack(padx=10, pady=5)

# Etiqueta y campo de texto para ingresar el nombre del entorno virtual
label_nombre = tk.Label(root, text="Nombre del Entorno Virtual:")
label_nombre.pack(padx=10, pady=5)

entry_nombre = tk.Entry(root, width=40)
entry_nombre.insert(0, 'venv')  # Valor predeterminado 'venv'
entry_nombre.pack(padx=10, pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(padx=10, pady=10)

# Botón para crear el entorno virtual
boton_crear = tk.Button(root, text="Crear Entorno Virtual", command=crear_entorno_virtual)
boton_crear.pack(padx=10, pady=10)

# Botón para activar el entorno virtual
boton_abrir = tk.Button(root, text="Activar Entorno Virtual", command=abrir_entorno_virtual)
boton_abrir.pack(padx=10, pady=10)

# Iniciar la ventana principal
root.mainloop()
