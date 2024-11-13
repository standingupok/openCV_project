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

def predict_emotion(input_data, model):
    # Set paths
    img = cv2.imdecode(np.frombuffer(input_data.read(), np.uint8), cv2.IMREAD_COLOR)
    # Load image
    # img = cv2.imread(input_data)
    desired_width = 640  # Adjust as needed
    desired_height = 480  # Adjust as needed
    
    # Kích thước ban đầu của ảnh
    original_height, original_width = img.shape[:2]

    # Tính tỷ lệ cho chiều rộng và chiều cao
    width_ratio = desired_width / original_width
    height_ratio = desired_height / original_height

    # Chọn tỷ lệ lớn hơn để ảnh lấp đầy khung
    scale = max(width_ratio, height_ratio)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    img_resize = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Perform prediction
    result = model(img_resize, verbose=False)[0]
    conf = float(result.probs.cpu().top1conf)
    result_id = int(result.probs.cpu().top1)
    cls = model.names[result_id]

    # Draw class name and confidence on the image
    text = f"{cls}: {conf:.2f}"
    cv2.putText(img_resize, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Save the annotated image
    output_img_path = output_folder + input_data.filename
    cv2.imwrite(output_img_path, img_resize)

    while not os.path.exists(output_img_path):
        pass

    return output_img_path;

def process_frame(frame, model):
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

    frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    # frame = cv2.resize(frame, (1280, 720))

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
    # output_img_path = output_folder + input_data.filename
    # cv2.imwrite(output_img_path, frame)
    # while not os.path.exists(output_img_path):
    #     pass
    # return output_img_path;