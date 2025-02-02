from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
model = load_model('asl_cnn_interrupted.h5')  # Replace with your model path
class_names = sorted(os.listdir('dataset/asl_alphabet_train/asl_alphabet_train/'))

def preprocess_image(img):
    img = cv2.resize(img, (64, 64))
    img = img / 255.0
    return img.reshape(1, 64, 64, 3)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        img = preprocess_image(img)
        pred = model.predict(img)
        return jsonify({
            'class': class_names[np.argmax(pred)],
            'confidence': float(np.max(pred))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) 
