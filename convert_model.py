import tensorflow as tf

# Load the .h5 model
print("Loading .h5 model...")
model = tf.keras.models.load_model('models/plant_disease_model.h5')

# Save as .keras format
print("Saving as .keras format...")
model.save('models/saved_model/crop_disease_model.keras')

print("✓ Conversion complete!")