import os
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

def load_model():
    model = YOLO("best.pt")
    return model

def predict_emotion(input_data, model):
    # Set paths
    img = cv2.imdecode(np.frombuffer(input_data.read(), np.uint8), cv2.IMREAD_COLOR)
    output_folder = "static/predictions/"

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