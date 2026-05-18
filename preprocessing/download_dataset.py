import tensorflow as tf

DATA_DIR = "datasets/raw/PlantVillage"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def load_dataset():

    print("Loading training dataset...")

    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )

    print("Loading validation dataset...")

    val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )

    print("Classes:", train_dataset.class_names)

    # --------------------------------------------------
    # PREPROCESSING
    # --------------------------------------------------

    normalization_layer = tf.keras.layers.Rescaling(1./255)

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
    ])

    # Apply augmentation only to training data
    train_dataset = train_dataset.map(
        lambda x, y: (data_augmentation(normalization_layer(x), training=True), y)
    )

    # Only normalization for validation data
    val_dataset = val_dataset.map(
        lambda x, y: (normalization_layer(x), y)
    )

    # --------------------------------------------------
    # PERFORMANCE OPTIMIZATION
    # --------------------------------------------------

    AUTOTUNE = tf.data.AUTOTUNE

    train_dataset = train_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_dataset = val_dataset.cache().prefetch(buffer_size=AUTOTUNE)

    return train_dataset, val_dataset


if __name__ == "__main__":
    train_ds, val_ds = load_dataset()
