"""
CNN architecture for crop disease detection.
Input(224,224,3) -> Conv2D(32)->ReLU->MaxPool -> Conv2D(64)->ReLU->MaxPool ->
Conv2D(128)->ReLU->MaxPool -> Flatten -> Dense(256)->ReLU->Dropout(0.5) -> Dense(N, softmax)
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def build_model(num_classes, input_shape=(224, 224, 3)):
    """
    Build the CNN model.

    Args:
        num_classes: Number of output classes (disease types + healthy)
        input_shape: (height, width, channels)

    Returns:
        Keras Model
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        # Classifier
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax'),
    ], name='crop_disease_cnn')

    return model
