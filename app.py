import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for
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
            # file = request.files['file']

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

    if __name__ == '__main__':
        app.run(debug=True)

    return app


 