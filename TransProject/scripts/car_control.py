import os
import cv2
import numpy as np
from keras.models import load_model
from flask import Flask, request, jsonify
import time

# Flask app
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'  # Relative path for uploads folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create upload folder if it doesn't exist

# Load the pre-trained H5 model once during server startup
MODEL_PATH = "../models/traffic_sign_model.h5"
print("Loading the model...")
model = load_model(MODEL_PATH)
print("Model loaded successfully.")

# Function to preprocess an image for the model
def preprocess_image(image, target_size=(64, 64)):
    """
    Preprocess the image for prediction by the model.
    :param image: Input image (numpy array).
    :param target_size: Tuple indicating the target size for resizing.
    :return: Preprocessed image ready for the model.
    """
    img = cv2.resize(image, target_size)  # Resize image to the target size
    img = img.astype("float32") / 255.0  # Normalize pixel values to [0, 1]
    return np.expand_dims(img, axis=0)  # Add batch dimension

# Function to predict the class of an image
def predict_class(image, model):
    """
    Predict the class of the given image using the model.
    :param image: Preprocessed image (numpy array).
    :param model: Loaded model for prediction.
    :return: Predicted class index.
    """
    predictions = model.predict(image, verbose=0)
    return np.argmax(predictions)  # Return the class index with highest probability

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to receive an image from the client.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a dynamic filename to prevent overwriting
    filename = f"{int(time.time())}.jpg"  # Use timestamp to ensure unique filenames
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Save the file
        file.save(filepath)
        print(f"File received and saved at {filepath}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Load and preprocess the image
    image = cv2.imread(filepath)
    preprocessed_image = preprocess_image(image)  # Preprocess the image
    predicted_class = predict_class(preprocessed_image, model)  # Predict the class

    # Map the predicted class to a command
    commands = {0: "stop", 1: "right", 2: "left"}  # Example mapping, adjust as needed
    response = commands.get(predicted_class, "ff")  # Default to "stop" if class is not found

    print(f"Predicted class: {predicted_class}, Command: {response}")
    
    # Return the response as JSON
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
