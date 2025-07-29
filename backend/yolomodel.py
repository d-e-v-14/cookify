import torch
from collections import Counter
from ultralytics import YOLO

model_path = 'models/yolov8m.pt'
confidence = 0.25

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO(model_path).to(device)
class_names = model.names

def detect_ingredients(image_path: str) -> dict:
    print(f"[INFO] Detecting ingredients in: {image_path}")
    results = model.predict(source=image_path, show=False, conf=confidence, save=False)
    result = results[0]
    
    boxes = result.boxes.cls.cpu().numpy().astype(int)
    print("[INFO] Detected class indices:", boxes)

    counts = Counter(boxes)
    detected = {class_names[k]: int(v) for k, v in counts.items() if k in class_names}
    print("[INFO] Final Detected:", detected)
    return detected
