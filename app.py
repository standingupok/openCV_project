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
                    # Process image for prediction
                    frame = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
                    processed_frame = process_frame(frame, model)

                    # save result
                    predict_img_path = output_folder + file.filename;
                    cv2.imwrite(predict_img_path, processed_frame)
                    
                    # append into response_data list
                    response_data.append({
                        'emotion': predict_img_path,
                        'image_url': predict_img_path
                    })

                elif file.filename.lower().endswith(('.mp4', '.avi')):
                    # save video
                    fileName = file.filename
                    file_path = "static/videos/" + fileName
                    output_video_path = output_folder + fileName
                    file.save(file_path)

                    # read video
                    cap = cv2.VideoCapture(file_path)

                    # prepare tool for process video
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

                    # process video
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        processed_frame = process_frame(frame, model)
                        out.write(processed_frame)

                    cap.release()
                    out.release()
                    
                    response_data.append({
                        'emotion': output_video_path,
                        'image_url': output_video_path
                    })
                    
                else:
                    return jsonify({"error": "Invalid file format"}), 400
            print(response_data)
            return jsonify({"files": response_data})

    if __name__ == '__main__':
        app.run(debug=True)

    return app


 