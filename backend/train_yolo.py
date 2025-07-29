from ultralytics import YOLO

def train_model():

    model = YOLO("models/yolov8m.pt")  

    model.train(
        data="dataset_test/data.yaml", 
        epochs=50,
        imgsz=640,
        batch=8,
        project="models",
        name="vegetable-fruit-detector",
        exist_ok=True
    )

if __name__ == "__main__":
    train_model()
