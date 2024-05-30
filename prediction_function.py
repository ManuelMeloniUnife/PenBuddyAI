import cv2
import numpy as np
import tensorflow as tf

# Carica il modello migliore
best_model = tf.keras.models.load_model("../doc/models/best_model.keras")

def prediction():
    try:
        # Carica l'immagine, ridimensionala a 28x28 e normalizzala
        img = cv2.imread("../doc/temp/temp_image.png", cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_LINEAR)
        img = np.invert(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=-1)  # Aggiungi la dimensione del canale
        img = np.array([img])
        prediction = best_model.predict(img)
        predicted_digit = np.argmax(prediction)
        return str(predicted_digit)  # Restituisce la previsione come stringa
    except Exception as e:
        return f"Error: {e}"
