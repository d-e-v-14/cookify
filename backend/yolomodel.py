from ultralytics import YOLO

model = YOLO("models/yolov8m.pt")  

def detect_ingredients(image_path):
    results = model(image_path)
    detections = {}

    for box in results[0].boxes.data:
        cls_id = int(box[5])
        cls_name = results[0].names[cls_id]
        detections[cls_name] = detections.get(cls_name, 0) + 1

    return detections
