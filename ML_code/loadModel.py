# Load the saved model
loaded_model = tf.keras.models.load_model('my_asl_model.keras')

# Make predictions with the loaded model
predictions = loaded_model.predict(img.jpg)
print("Predictions:", predictions)
