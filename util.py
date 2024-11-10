import os
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

def load_model():
    model = YOLO("best(raw).pt")
    return model

def predict_emotion(input_data, model):
    # Set paths
    img = cv2.imdecode(np.frombuffer(input_data.read(), np.uint8), cv2.IMREAD_COLOR)
    output_folder = "static/predictions/"

        # Load image
    # img = cv2.imread(input_data)
    desired_width = 640  # Adjust as needed
    desired_height = 480  # Adjust as needed
    # img = cv2.cvtColor(input_data, cv2.COLOR_BGR2GRAY)
    # img = cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_AREA)
    
    img = cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_AREA)

    # Perform prediction
    result = model(img, verbose=False)[0]
    conf = float(result.probs.cpu().top1conf)
    result_id = int(result.probs.cpu().top1)
    cls = model.names[result_id]

    # Draw class name and confidence on the image
    text = f"{cls}: {conf:.2f}"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Save the annotated image
    output_img_path = output_folder + input_data.filename
    cv2.imwrite(output_img_path, img)

    while not os.path.exists(output_img_path):
        pass

    return output_img_path;