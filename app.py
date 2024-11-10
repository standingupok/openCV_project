import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for
from util import *

def create_app():
    model = load_model()
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/predict', methods=['POST'])
    def predict():
        if request.method == 'POST':
            if 'files' not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            # file = request.files['file']

            files = request.files.getlist('files')  # Lấy tất cả các tệp
            response_data = []
            print(files)
            for file in files:
                print(file)
                if file.filename.endswith(('.jpg', '.png')):
                    # Process image for prediction
                    predict_img_path = predict_emotion(file, model)
                    response_data.append({
                        'emotion': predict_img_path,
                        'image_url': predict_img_path
                    })
                    
                # elif file.filename.endswith(('.mp4', '.avi')):
                #     # Process video for prediction
                #     video = cv2.VideoCapture(file)
                #     emotion = predict_emotion(video, model)
                else:
                    return jsonify({"error": "Invalid file format"}), 400
            print(response_data)
            return jsonify({"files": response_data})

    if __name__ == '__main__':
        app.run(debug=True)

    return app