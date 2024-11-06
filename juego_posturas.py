import cv2
import mediapipe as mp
import time
import random
import winsound
import joblib
import numpy as np

# Cargar el modelo entrenado
modelo = joblib.load("modelo_dificultad_equilibrio_actualizado.pkl")

# Inicialización de MediaPipe y OpenCV
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Variables del juego
puntuacion = 0
duracion_desafio = 3
desafios = [
    (0.4, 'Baja la cabeza'),
    (0.4, 'Inclinate hacia la izquierda'),
    (0.4, 'Inclinate hacia la derecha')
]
desafio_actual = random.choice(desafios)
tiempo_inicio = time.time()
respuesta_tiempos = []

# Función para verificar el equilibrio
def verificar_equilibrio(landmarks, target_y):
    cabeza_y = landmarks[0].y
    return abs(cabeza_y - target_y) < 0.05

# Función para reproducir sonido
def reproducir_sonido(frecuencia=1000, duracion=500):
    winsound.Beep(frecuencia, duracion)

# Loop principal
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Procesamiento de la imagen y detección de pose
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = pose.process(frame_rgb)

    if resultados.pose_landmarks:
        mp_drawing.draw_landmarks(frame, resultados.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if verificar_equilibrio(resultados.pose_landmarks.landmark, desafio_actual[0]):
            tiempo_elapsed = time.time() - tiempo_inicio
            if tiempo_elapsed > duracion_desafio:
                puntuacion += 1
                reproducir_sonido()
                respuesta_tiempos.append(tiempo_elapsed)

                # Predicción de la dificultad para el siguiente desafío
                tiempo_promedio = np.mean(respuesta_tiempos)
                dificultad_predicha = modelo.predict([[tiempo_promedio, 1]])[0]  # "1" para indicar que completó el desafío
                
                # Ajustar la duración del desafío según la dificultad predicha
                duracion_desafio = 5 if dificultad_predicha == 1 else 3

                tiempo_inicio = time.time()
                desafio_actual = random.choice(desafios)
                cv2.putText(frame, "¡Bien hecho! ¡Siguiente desafio!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            tiempo_inicio = time.time()

        # Mostrar instrucciones en pantalla
        cv2.putText(frame, f"Manten: {desafio_actual[1]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Puntuacion: {puntuacion}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Mostrar el frame en pantalla
    cv2.imshow("Juego de Equilibrio", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
