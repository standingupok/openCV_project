import os
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import os
import cv2
import torch
from flask import Flask, request, jsonify
from facenet_pytorch import MTCNN
# Define emotion dictionary
emotion_dict = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprise"
}
output_folder = "static/predictions/"

mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    model = YOLO("best.pt")
    return model

def predict_img(file, model):
    # Process image for prediction
    frame = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    processed_frame = process_frame(frame, model, True)

    # save result
    predict_img_path = output_folder + file.filename;
    cv2.imwrite(predict_img_path, processed_frame)
                
    # append into response_data list

    return predict_img_path;

def predict_video(file, model):
    # save video
    fileName = file.filename
    file_path = "static/videos/" + fileName
    output_video_path = output_folder + fileName
    file.save(file_path)

    # read video
    cap = cv2.VideoCapture(file_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # prepare tool for process video
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (frame_width, frame_height))

    # process video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame, model, False)
        out.write(processed_frame)

        if(cv2.waitKey(10) == ord('q')):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return output_video_path;

def process_frame(frame, model, isImage):
    # print(frame.shape, frame.dtype)

    desired_width = 640  # Adjust as needed
    desired_height = 480  # Adjust as needed
    
    # Kích thước ban đầu của ảnh
    original_height, original_width = frame.shape[:2]

    # Tính tỷ lệ cho chiều rộng và chiều cao
    width_ratio = desired_width / original_width
    height_ratio = desired_height / original_height

    # Chọn tỷ lệ lớn hơn để ảnh lấp đầy khung
    scale = max(width_ratio, height_ratio)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    if isImage: frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    else: frame = cv2.resize(frame, (1280, 720)) 

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    boxes, probs = mtcnn.detect(rgb_frame)

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            height, width = gray_frame.shape[:2]
            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(width, x2), min(height, y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)

            if x1 < x2 and y1 < y2:
                roi_gray_frame = gray_frame[y1:y2, x1:x2]
                if roi_gray_frame.size == 0:
                    print("ROI is empty after cropping!")
                    continue
                
                results = model.predict(source=roi_gray_frame)
            for result in results:
                class_id = int(result.probs.cpu().top1)
                conf = float(result.probs.cpu().top1conf)
                class_name = result.names[class_id]
                text = f"{class_name} ({conf:.2f})"
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame