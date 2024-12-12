import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from io import BytesIO
from util import *

def create_app():
    output_folder = "static/predictions/"
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

            files = request.files.getlist('files')  # Lấy tất cả các tệp
            response_data = []

            for file in files:
                if file.filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                    predict_img_path = predict_img(file, model)
                    response_data.append({
                        'isImage': True,
                        'image_url': predict_img_path
                    })

                elif file.filename.lower().endswith(('.mp4', '.avi')):
                    output_video_path = predict_video(file, model)
                    response_data.append({
                        'isImage': False,
                        'image_url': f"/static/predictions/{file.filename}"
                    })
                    
                else:
                    return jsonify({"error": "Invalid file format"}), 400
            # print(response_data)
            return jsonify({"files": response_data})

    @app.route('/predict_camera', methods = ['GET'])
    def predict_camera_route():
        result = predict_camera(model)
        if result == "Camera processing completed.":
            return jsonify({"message": result})
        else:
            return jsonify({"error": "Failed to process camera input"}), 500

    if __name__ == '__main__':
        app.run(debug=True)

    return app