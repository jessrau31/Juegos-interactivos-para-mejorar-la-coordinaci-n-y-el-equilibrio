import tkinter as tk
import random
import time
import joblib
import numpy as np

# Cargar el modelo entrenado
modelo = joblib.load("modelo_dificultad_colores_actualizado.pkl")

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Juego de Coordinación Cognitiva con IA")
ventana.geometry("375x667")

# Definición de colores
colores = ["rojo", "azul", "verde", "amarillo", "morado"]
colores_rgb = {
    "rojo": "red",
    "azul": "blue",
    "verde": "green",
    "amarillo": "yellow",
    "morado": "purple"
}

# Variables del juego
color_palabra = ""
color_texto = ""
ronda_actual = 1
total_rondas = 6
tiempo_restante = 10
aciertos = 0
respuesta_tiempo = []

# Función para actualizar el juego
def actualizar_juego():
    global color_palabra, color_texto, tiempo_restante, ronda_actual, tiempo_inicio
    
    # Si el juego ha terminado
    if ronda_actual > total_rondas:
        resultado.config(text="¡Juego terminado!", fg="blue")
        aciertos_finales.config(text=f"Aciertos finales: {aciertos}")
        temporizador.config(text="")
        contador_aciertos.config(text="")
        return

    # Seleccionar color de la palabra y el texto
    color_palabra = random.choice(colores)
    color_texto = random.choice(colores)
    etiqueta_color.config(text=color_palabra, fg=colores_rgb[color_texto])
    resultado.config(text="")

    # Predicción de dificultad
    if respuesta_tiempo:
        tiempo_promedio = np.mean(respuesta_tiempo)
        dificultad_predicha = modelo.predict([[tiempo_promedio, aciertos]])[0]
        tiempo_restante = 5 if dificultad_predicha == 1 else 10
    else:
        tiempo_restante = 10  # tiempo inicial para la primera ronda

    tiempo_inicio = time.time()
    actualizar_tiempo()

# Verificar la respuesta del usuario
def verificar_respuesta(respuesta):
    global ronda_actual, aciertos
    tiempo_respuesta = time.time() - tiempo_inicio
    respuesta_tiempo.append(tiempo_respuesta)

    if respuesta == color_texto:
        resultado.config(text="¡Correcto!", fg="green")
        aciertos += 1
        contador_aciertos.config(text=f"Aciertos: {aciertos}")
        ronda_actual += 1
        if ronda_actual <= total_rondas:
            actualizar_juego()
        else:
            resultado.config(text="¡Juego terminado!", fg="blue")
            aciertos_finales.config(text=f"Aciertos finales: {aciertos}")
    else:
        resultado.config(text="¡Incorrecto! Juego terminado.", fg="red")
        aciertos_finales.config(text=f"Aciertos finales: {aciertos}")
        temporizador.config(text="")
        contador_aciertos.config(text="")

# Actualizar el temporizador
def actualizar_tiempo():
    global tiempo_restante
    if tiempo_restante > 0:
        tiempo_restante -= 1
        temporizador.config(text=f"Tiempo: {tiempo_restante:.1f} s")
        ventana.after(1000, actualizar_tiempo)
    else:
        resultado.config(text="¡Tiempo agotado! Juego terminado.", fg="orange")
        aciertos_finales.config(text=f"Aciertos finales: {aciertos}")
        contador_aciertos.config(text="")

# Configuración de la interfaz de usuario
etiqueta_color = tk.Label(ventana, font=("Arial", 40))
etiqueta_color.pack(pady=30)

resultado = tk.Label(ventana, text="", font=("Arial", 20))
resultado.pack(pady=5)

temporizador = tk.Label(ventana, text=f"Tiempo: {tiempo_restante} s", font=("Arial", 18))
temporizador.pack(pady=5)

contador_aciertos = tk.Label(ventana, text=f"Aciertos: {aciertos}", font=("Arial", 18))
contador_aciertos.pack(pady=5)

aciertos_finales = tk.Label(ventana, text="", font=("Arial", 18))
aciertos_finales.pack(pady=5)

marco_botones = tk.Frame(ventana)
marco_botones.pack(expand=True, fill=tk.BOTH)

# Botones de colores
for color in colores:
    boton = tk.Button(marco_botones, bg=colores_rgb[color], command=lambda c=color: verificar_respuesta(c), width=10, height=2)
    boton.pack(side=tk.TOP, padx=5, pady=10, fill=tk.X)

# Iniciar el juego
actualizar_juego()
ventana.mainloop()
