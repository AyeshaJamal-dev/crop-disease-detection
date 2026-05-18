"""
Data augmentation for training.
Uses tf.keras.preprocessing.image.ImageDataGenerator.
"""
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def get_training_augmentation():
    """
    Get ImageDataGenerator with augmentation as per proposal:
    - Random rotation ±20 degrees
    - Horizontal/vertical flips
    - Zoom 0.8-1.2x
    - Brightness adjustment
    """
    return ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=20,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.2,  # 0.8 to 1.2
        brightness_range=[0.8, 1.2],
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        fill_mode='nearest',
        validation_split=0.2,
    )


def get_validation_generator(rescale_only=True):
    """Generator for validation data (no augmentation)."""
    return ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=0.2,
    )
