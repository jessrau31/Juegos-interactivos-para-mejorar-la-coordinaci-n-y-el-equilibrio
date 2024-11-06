import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Cargar el conjunto de datos de colores
data = pd.read_csv("coordinacion_colores.csv", encoding='latin1')

# Separar en variables de entrada y salida
X = data[["tiempo_respuesta", "aciertos"]]
y = data["dificultad"]

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de colores
modelo_colores = RandomForestClassifier(n_estimators=10, random_state=42)
modelo_colores.fit(X_train, y_train)

# Evaluar el modelo
y_pred = modelo_colores.predict(X_test)
print("Precisión del modelo de colores:", accuracy_score(y_test, y_pred))

# Guardar el modelo entrenado
joblib.dump(modelo_colores, "modelo_dificultad_colores_actualizado.pkl")
print("Modelo de coordinación de colores guardado como 'modelo_dificultad_colores_actualizado.pkl'")
