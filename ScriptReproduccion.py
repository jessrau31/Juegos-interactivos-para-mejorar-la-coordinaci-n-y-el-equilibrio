### 2e. Script de Reproducción

# Guarde el siguiente script como `reproducir_resultados.py` para entrenar el modelo y ejecutar los juegos:

# python
import subprocess

# Entrenar el modelo del juego de colores
print("Entrenando los modelos con el conjunto de datos...")
subprocess.run(["python", "modelo_entrenamiento_colores.py"])

# Entrenar el modelo del juego de equilibrio
print("Entrenando los modelos con el conjunto de datos...")
subprocess.run(["python", "modelo_entrenamiento_equilibrio.py"])

# Ejecutar el juego de coordinación de colores
print("Ejecutando el juego de Coordinación Cognitiva con Colores...")
subprocess.run(["python", "juego_colores.py"])

# Ejecutar el juego de posturas de equilibrio
print("Ejecutando el juego de Posturas de Equilibrio...")
subprocess.run(["python", "juego_equilibrio.py"])