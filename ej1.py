# EJERCICIO ENTORNOS DE DESARROLLO - 31/10/2025
# Solución con Interfaz Gráfica (Tkinter)

import tkinter as tk
from tkinter import ttk  # Usamos ttk para widgets más modernos
from tkinter import messagebox

# --- 1. Lógica del Negocio (Las mismas funciones de antes) ---

def celsius_a_fahrenheit(celsius):
    """Convierte grados Celsius a Fahrenheit."""
    return (celsius * 9/5) + 32

def generar_texto_tabla(numero):
    """
    Genera un STRING con la tabla de multiplicar.
    (Modificada para devolver texto en lugar de imprimir).
    """
    # Usamos un list comprehension y .join() para construir el string
    lineas = [f"{numero} x {i} = {numero * i}" for i in range(1, 11)]
    return "\n".join(lineas)

# --- 2. Clase Principal de la Aplicación ---

class Aplicacion(tk.Tk):
    """Clase principal que hereda de tk.Tk para crear la ventana."""
    
    def __init__(self):
        super().__init__()  # Llama al constructor de la clase padre (tk.Tk)
        self.title("Ejercicio Entornos - (Solución 10/10)")
        self.geometry("350x400") # Tamaño inicial
        
        # --- Contenedor principal para los "frames" (pantallas) ---
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} # Un diccionario para guardar las pantallas

        # --- Creamos las diferentes pantallas (frames) ---
        # Pasamos 'container' como padre de cada frame
        for F in (FrameMenu, FrameTemperatura, FrameTabla):
            frame = F(container, self)
            self.frames[F] = frame
            # Colocamos todos los frames en el mismo sitio
            frame.grid(row=0, column=0, sticky="nsew") 

        # Mostramos la pantalla inicial (el menú)
        self.mostrar_frame(FrameMenu)

    def mostrar_frame(self, cont):
        """Muestra un frame específico (pantalla) y oculta los demás."""
        frame = self.frames[cont]
        frame.tkraise() # Trae el frame solicitado al frente

# --- 3. Pantalla del Menú Principal ---

class FrameMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        label = ttk.Label(self, text="Menú Principal", font=("Arial", 16, "bold"))
        label.pack(pady=20)

        # Botón 1: Ir a Temperatura
        btn_temp = ttk.Button(self, text="1) Conversión de Temperatura", 
                              command=lambda: controller.mostrar_frame(FrameTemperatura))
        btn_temp.pack(fill='x', pady=10)

        # Botón 2: Ir a Tabla de Multiplicar
        btn_tabla = ttk.Button(self, text="2) Tabla de Multiplicar",
                               command=lambda: controller.mostrar_frame(FrameTabla))
        btn_tabla.pack(fill='x', pady=10)

        # Botón 3: Salir
        btn_salir = ttk.Button(self, text="3) Salir",
                             command=self.quit)
        btn_salir.pack(fill='x', pady=10, side="bottom")

# --- 4. Pantalla de Conversión de Temperatura ---

class FrameTemperatura(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        # --- Variables de control de Tkinter ---
        self.celsius_var = tk.StringVar()
        self.resultado_f_var = tk.StringVar(value="Resultado: ...")

        # --- Título ---
        label = ttk.Label(self, text="Conversión de Temperatura", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        # --- Frame de entrada ---
        frame_input = ttk.Frame(self)
        frame_input.pack(pady=10)
        
        lbl_celsius = ttk.Label(frame_input, text="Grados Celsius:")
        lbl_celsius.pack(side="left", padx=5)
        
        entry_celsius = ttk.Entry(frame_input, textvariable=self.celsius_var, width=10)
        entry_celsius.pack(side="left")

        # --- Botón de conversión ---
        btn_convertir = ttk.Button(self, text="Convertir a Fahrenheit",
                                   command=self.convertir)
        btn_convertir.pack(pady=10)

        # --- Label de resultado ---
        lbl_resultado = ttk.Label(self, textvariable=self.resultado_f_var, 
                                  font=("Arial", 12, "italic"))
        lbl_resultado.pack(pady=20)

        # --- Botón de volver ---
        btn_volver = ttk.Button(self, text="< Volver al Menú",
                                command=lambda: controller.mostrar_frame(FrameMenu))
        btn_volver.pack(side="bottom", pady=10)

    def convertir(self):
        """Función 'callback' que se ejecuta al pulsar el botón convertir."""
        try:
            # Obtenemos el valor del Entry y lo convertimos a float
            celsius_val = float(self.celsius_var.get())
            # Calculamos
            fahrenheit_val = celsius_a_fahrenheit(celsius_val)
            # Actualizamos la variable de resultado
            self.resultado_f_var.set(f"Resultado: {fahrenheit_val:.2f}°F")
        except ValueError:
            # Si la conversión a float falla, mostramos un error
            messagebox.showerror("Error de Entrada", 
                                 "Por favor, introduzca un valor numérico válido (ej: 20.5).")
            self.celsius_var.set("") # Limpiamos la entrada

# --- 5. Pantalla de Tabla de Multiplicar ---

class FrameTabla(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        # --- Variables de control ---
        self.numero_var = tk.StringVar()
        self.resultado_tabla_var = tk.StringVar(value="--- Esperando número ---")

        # --- Título ---
        label = ttk.Label(self, text="Tabla de Multiplicar", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        # --- Frame de entrada ---
        frame_input = ttk.Frame(self)
        frame_input.pack(pady=10)
        
        lbl_numero = ttk.Label(frame_input, text="Número Entero:")
        lbl_numero.pack(side="left", padx=5)
        
        entry_numero = ttk.Entry(frame_input, textvariable=self.numero_var, width=10)
        entry_numero.pack(side="left")

        # --- Botón de generar ---
        btn_generar = ttk.Button(self, text="Generar Tabla",
                                 command=self.generar)
        btn_generar.pack(pady=10)

        # --- Label de resultado (con justificación a la izquierda) ---
        lbl_resultado = ttk.Label(self, textvariable=self.resultado_tabla_var, 
                                  font=("Courier", 12), justify="left")
        lbl_resultado.pack(pady=20)

        # --- Botón de volver ---
        btn_volver = ttk.Button(self, text="< Volver al Menú",
                                command=lambda: controller.mostrar_frame(FrameMenu))
        btn_volver.pack(side="bottom", pady=10)

    def generar(self):
        """Función 'callback' que se ejecuta al pulsar el botón generar."""
        try:
            # Obtenemos el valor y lo convertimos a int
            numero_val = int(self.numero_var.get())
            # Generamos el texto
            tabla_texto = generar_texto_tabla(numero_val)
            # Actualizamos la variable de resultado
            self.resultado_tabla_var.set(tabla_texto)
        except ValueError:
            # Si la conversión a int falla, mostramos un error
            messagebox.showerror("Error de Entrada", 
                                 "Por favor, introduzca un número entero válido (ej: 7).")
            self.numero_var.set("") # Limpiamos la entrada


# --- Punto de entrada principal ---
if __name__ == "__main__":
    app = Aplicacion() # Creamos la instancia de nuestra aplicación
    app.mainloop()     # Iniciamos el bucle principal de Tkinter