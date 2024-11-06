import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Cargar el conjunto de datos de equilibrio
data = pd.read_csv("posturas_equilibrio.csv")

# Separar en variables de entrada y salida
X = data[["tiempo_respuesta", "completado"]]
y = data["dificultad"]

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de equilibrio
modelo_equilibrio = RandomForestClassifier(n_estimators=10, random_state=42)
modelo_equilibrio.fit(X_train, y_train)

# Evaluar el modelo
y_pred = modelo_equilibrio.predict(X_test)
print("Precisión del modelo de equilibrio:", accuracy_score(y_test, y_pred))

# Guardar el modelo entrenado
joblib.dump(modelo_equilibrio, "modelo_dificultad_equilibrio_actualizado.pkl")
print("Modelo de equilibrio guardado como 'modelo_dificultad_equilibrio_actualizado.pkl'")
