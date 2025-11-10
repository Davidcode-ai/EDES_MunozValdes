import tkinter as tk
from tkinter import ttk

# --- Variables Globales para Ventana ---
is_maximized = False
old_geometry = ""

# --- Funciones de Lógica de la App ---

def convertir_a_fahrenheit(event=None): 
    try:
        celsius = float(entry_celsius.get())
        fahrenheit = (celsius * 9/5) + 32
        label_resultado_f.config(text=f"Resultado: {fahrenheit:.2f} °F", foreground="#8AE9C1")
    except ValueError:
        label_resultado_f.config(text="Error: Introduce un número válido", foreground="#FF7F7F")

def generar_tabla_multiplicar(event=None):
    try:
        numero = int(entry_tabla.get())
        texto_tabla.config(state=tk.NORMAL)
        texto_tabla.delete("1.0", tk.END)
        tabla_texto = ""
        for i in range(1, 11):
            resultado = numero * i
            tabla_texto += f"{numero} x {i} = {resultado}\n"
        texto_tabla.insert(tk.END, tabla_texto)
        texto_tabla.config(foreground="#E0E0E0")
        texto_tabla.config(state=tk.DISABLED)
    except ValueError:
        texto_tabla.config(state=tk.NORMAL)
        texto_tabla.delete("1.0", tk.END)
        texto_tabla.insert(tk.END, "Error: Introduce un número válido")
        texto_tabla.config(foreground="#FF7F7F")
        texto_tabla.config(state=tk.DISABLED)

# --- ¡¡¡FUNCIÓN DE FOCO CORREGIDA!!! ---
def force_focus(event=None):
    """
    Se llama CADA VEZ que la ventana necesita recuperar el foco
    (cambio de pestaña, clic, restaurar)
    """
    try:
        # Intenta obtener la pestaña actual.
        # Si falla (p.ej. al inicio), simplemente pone el foco en la primera.
        current_tab = notebook.index(notebook.select())
        if current_tab == 0:
            entry_celsius.focus_force() # Usamos focus_force()
        else:
            entry_tabla.focus_force() # Usamos focus_force()
    except Exception:
        entry_celsius.focus_force() # Falla segura

# --- Funciones de la Barra de Título Personalizada ---

def start_move(event):
    """Guarda la posición del clic Y FUERZA EL FOCO."""
    ventana.x = event.x
    ventana.y = event.y
    # --- ¡¡¡CAMBIO CLAVE AQUÍ!!! ---
    # Al hacer clic en la barra, también forzamos el foco.
    force_focus()

def do_move(event):
    """Mueve la ventana."""
    deltax = event.x - ventana.x
    deltay = event.y - ventana.y
    new_x = ventana.winfo_x() + deltax
    new_y = ventana.winfo_y() + deltay
    ventana.geometry(f"+{new_x}+{new_y}")

def close_window(event=None):
    ventana.destroy()

def minimize_window(event=None):
    """Minimiza la ventana correctamente."""
    ventana.overrideredirect(False)
    ventana.iconify()

def on_restore(event):
    """Se llama al restaurar la ventana."""
    if ventana.state() == 'normal':
        ventana.overrideredirect(True)
        # --- ¡¡¡CAMBIO CLAVE AQUÍ!!! ---
        # Al restaurar, también forzamos el foco.
        force_focus()

def toggle_maximize(event=None):
    global is_maximized, old_geometry
    if not is_maximized:
        old_geometry = ventana.geometry()
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        ventana.geometry(f"{screen_width}x{screen_height-40}+0+0") 
        is_maximized = True
    else:
        ventana.geometry(old_geometry)
        is_maximized = False

# --- Configuración de la Ventana Principal ---
ventana = tk.Tk()
ventana.overrideredirect(True)
ventana.title("App Moderna")
ventana.geometry("450x520") 
ventana.resizable(False, False)
COLOR_FONDO_PRINCIPAL = "#1A1A2E" 
ventana.configure(bg=COLOR_FONDO_PRINCIPAL)

ventana.bind("<Map>", on_restore)

# --- Definición de Colores y Fuentes ---
COLOR_PRIMARIO = "#0F3460"
COLOR_SECUNDARIO = COLOR_FONDO_PRINCIPAL
COLOR_ACENTO = "#E94560"
COLOR_TEXTO_CLARO = "#E0E0E0"
COLOR_TEXTO_OSCURO = "#AAAAAA"
COLOR_CAMPO_TEXTO = "#33334A"
COLOR_BARRA_TITULO = "#2A2A3E"
COLOR_BTN_CLOSE = "#FF605C"
COLOR_BTN_MIN = "#FFBD44"
COLOR_BTN_MAX = "#28CA41"
COLOR_BTN_CLOSE_HOVER = "#E04F4C"
COLOR_BTN_MIN_HOVER = "#E0A83A"
COLOR_BTN_MAX_HOVER = "#24B038"
FONT_TITULO = ("Segoe UI", 20, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_BOTON = ("Segoe UI", 10, "bold")
FONT_RESULTADO = ("Segoe UI", 14, "bold")
FONT_TABLA = ("Segoe UI", 11)

# --- Creación de la Barra de Título Personalizada ---
title_bar = tk.Frame(ventana, bg=COLOR_BARRA_TITULO, height=40)
title_bar.place(x=0, y=0, relwidth=1)
title_bar.bind("<ButtonPress-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)

# --- Animación Hover para botones Mac ---
def on_enter_close(e): btn_close.itemconfig(oval_close, fill=COLOR_BTN_CLOSE_HOVER, outline=COLOR_BTN_CLOSE_HOVER)
def on_leave_close(e): btn_close.itemconfig(oval_close, fill=COLOR_BTN_CLOSE, outline=COLOR_BTN_CLOSE)
def on_enter_min(e): btn_minimize.itemconfig(oval_min, fill=COLOR_BTN_MIN_HOVER, outline=COLOR_BTN_MIN_HOVER)
def on_leave_min(e): btn_minimize.itemconfig(oval_min, fill=COLOR_BTN_MIN, outline=COLOR_BTN_MIN)
def on_enter_max(e): btn_maximize.itemconfig(oval_max, fill=COLOR_BTN_MAX_HOVER, outline=COLOR_BTN_MAX_HOVER)
def on_leave_max(e): btn_maximize.itemconfig(oval_max, fill=COLOR_BTN_MAX, outline=COLOR_BTN_MAX)

btn_close = tk.Canvas(title_bar, width=15, height=15, bg=COLOR_BARRA_TITULO, 
                      highlightthickness=0, cursor="hand2")
oval_close = btn_close.create_oval(3, 3, 12, 12, fill=COLOR_BTN_CLOSE, outline=COLOR_BTN_CLOSE)
btn_close.place(x=15, y=12)
btn_close.bind("<Button-1>", close_window)
btn_close.bind("<Enter>", on_enter_close)
btn_close.bind("<Leave>", on_leave_close)

btn_minimize = tk.Canvas(title_bar, width=15, height=15, bg=COLOR_BARRA_TITULO, 
                         highlightthickness=0, cursor="hand2")
oval_min = btn_minimize.create_oval(3, 3, 12, 12, fill=COLOR_BTN_MIN, outline=COLOR_BTN_MIN)
btn_minimize.place(x=40, y=12)
btn_minimize.bind("<Button-1>", minimize_window)
btn_minimize.bind("<Enter>", on_enter_min)
btn_minimize.bind("<Leave>", on_leave_min)

btn_maximize = tk.Canvas(title_bar, width=15, height=15, bg=COLOR_BARRA_TITULO, 
                         highlightthickness=0, cursor="hand2")
oval_max = btn_maximize.create_oval(3, 3, 12, 12, fill=COLOR_BTN_MAX, outline=COLOR_BTN_MAX)
btn_maximize.place(x=65, y=12)
btn_maximize.bind("<Button-1>", toggle_maximize)
btn_maximize.bind("<Enter>", on_enter_max)
btn_maximize.bind("<Leave>", on_leave_max)

title_label = tk.Label(title_bar, text="Mi Aplicación", 
                       font=("Segoe UI", 10), 
                       fg=COLOR_TEXTO_OSCURO, 
                       bg=COLOR_BARRA_TITULO)
title_label.place(relx=0.5, rely=0.5, anchor="center")
title_label.bind("<ButtonPress-1>", start_move)
title_label.bind("<B1-Motion>", do_move)

# --- Configuración de Estilos ttk ---
style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background=COLOR_SECUNDARIO, borderwidth=0)
style.configure("TNotebook.Tab", background=COLOR_SECUNDARIO, foreground=COLOR_TEXTO_OSCURO, 
                font=FONT_LABEL, padding=[10, 5], borderwidth=0)
style.map("TNotebook.Tab", 
          background=[("selected", COLOR_PRIMARIO), ("!selected", COLOR_SECUNDARIO)], 
          foreground=[("selected", COLOR_TEXTO_CLARO), ("!selected", COLOR_TEXTO_OSCURO)])
style.configure("TFrame", background=COLOR_SECUNDARIO)
style.configure("TLabel", background=COLOR_SECUNDARIO, foreground=COLOR_TEXTO_CLARO, font=FONT_LABEL)
style.configure("TEntry", fieldbackground=COLOR_CAMPO_TEXTO, foreground=COLOR_TEXTO_CLARO, 
                insertcolor=COLOR_ACENTO, font=FONT_LABEL, borderwidth=0, relief="flat")
style.map("TEntry", fieldbackground=[('focus', '#4A4A6A')], relief=[('focus', 'flat')])
style.configure("TButton", background=COLOR_ACENTO, foreground="#FFFFFF", 
                font=FONT_BOTON, borderwidth=0, padding=10, relief="flat")
style.map(
    "TButton",
    background=[('active', '#C93F56'), ('hover', '#F05A74')]
)

# --- Creación de Widgets (Posiciones ajustadas) ---
main_title = tk.Label(ventana, text="Panel de Control", 
                      font=FONT_TITULO, fg=COLOR_TEXTO_CLARO, bg=COLOR_FONDO_PRINCIPAL)
main_title.place(x=25, y=60)

notebook = ttk.Notebook(ventana)
notebook.place(x=25, y=110, width=400, height=390)

# --- ¡¡¡ENLAZAR EL CAMBIO DE PESTAÑA!!! ---
# Ahora llama a la nueva función force_focus
notebook.bind("<<NotebookTabChanged>>", force_focus)


# --- Pestaña 1: Conversor Celsius a Fahrenheit ---
pestaña1 = ttk.Frame(notebook, style="TFrame")
notebook.add(pestaña1, text='  Celsius a Fahrenheit  ')
label_celsius_info = ttk.Label(pestaña1, text="Introduce Grados Celsius:")
label_celsius_info.pack(pady=(40, 10))
entry_celsius = ttk.Entry(pestaña1, justify="center", width=25)
entry_celsius.bind("<Return>", convertir_a_fahrenheit)
entry_celsius.pack(pady=5, ipady=5)
boton_convertir = ttk.Button(pestaña1, text="Convertir a Fahrenheit", command=convertir_a_fahrenheit)
boton_convertir.pack(pady=25)
label_resultado_f = ttk.Label(pestaña1, text="Resultado: ... °F", font=FONT_RESULTADO, 
                              foreground=COLOR_TEXTO_CLARO)
label_resultado_f.pack(pady=15)

# --- Pestaña 2: Tabla de Multiplicar ---
pestaña2 = ttk.Frame(notebook, style="TFrame")
notebook.add(pestaña2, text='  Tabla de Multiplicar  ')
label_tabla_info = ttk.Label(pestaña2, text="Introduce un número entero:")
label_tabla_info.pack(pady=(40, 10))
entry_tabla = ttk.Entry(pestaña2, justify="center", width=25)
entry_tabla.bind("<Return>", generar_tabla_multiplicar)
entry_tabla.pack(pady=5, ipady=5)
boton_generar = ttk.Button(pestaña2, text="Generar Tabla", command=generar_tabla_multiplicar)
boton_generar.pack(pady=25)
texto_tabla = tk.Text(
    pestaña2, width=30, height=11, wrap=tk.WORD, bg=COLOR_CAMPO_TEXTO, 
    fg=COLOR_TEXTO_CLARO, font=FONT_TABLA, relief="flat", borderwidth=0, 
    insertbackground=COLOR_ACENTO, padx=10, pady=10)
texto_tabla.pack(pady=5)
texto_tabla.config(state=tk.DISABLED)

# --- Foco inicial ---
# Llamamos a la función por primera vez para poner el foco
force_focus()

# --- Iniciar el bucle principal ---
ventana.mainloop()
