import tensorflow as tf
from preprocessing.download_dataset import load_dataset

# Load datasets
train_ds, val_ds = load_dataset()

NUM_CLASSES = 39

# --------------------------------------------------
# BUILD CNN MODEL
# --------------------------------------------------

model = tf.keras.Sequential([

    # Convolution Block 1
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2,2),

    # Convolution Block 2
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    # Convolution Block 3
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    # Flatten
    tf.keras.layers.Flatten(),

    # Fully Connected Layer
    tf.keras.layers.Dense(128, activation='relu'),

    # Dropout (reduces overfitting)
    tf.keras.layers.Dropout(0.5),

    # Output Layer
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

# --------------------------------------------------
# COMPILE MODEL
# --------------------------------------------------

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

model.save("models/plant_disease_cnn.h5")

print("Model saved successfully.")
