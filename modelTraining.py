import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau

# Carica e normalizza il dataset MNIST
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizza le immagini a 28x28
x_train = x_train / 255.0
x_test = x_test / 255.0

# Aggiungi una dimensione per il canale di colore (grayscale)
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)
datagen.fit(x_train)

# Costruisci il modello CNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Compila il modello
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Definisci le callback
checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    '../doc/models/best_model.keras', save_best_only=True, monitor='val_loss', mode='min'
)
early_stopping_cb = tf.keras.callbacks.EarlyStopping(
    patience=5, restore_best_weights=True, monitor='val_loss', mode='min'
)
reduce_lr_cb = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, mode='min')

# Addestra il modello
history = model.fit(datagen.flow(x_train, y_train, batch_size=32), epochs=50, 
                    validation_data=(x_test, y_test), 
                    callbacks=[checkpoint_cb, early_stopping_cb, reduce_lr_cb])

# Salva il modello finale
model.save('../doc/models/final_model.keras')

# Valuta il modello sui dati di test
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc}")

# Carica il modello migliore per la predizione
best_model = tf.keras.models.load_model('../doc/models/best_model.keras')
