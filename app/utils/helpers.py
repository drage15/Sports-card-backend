import os, json
from datetime import datetime
from fastapi import UploadFile

DATA_DIR = "training_data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
LABELS_FILE = os.path.join(DATA_DIR, "labels.json")

os.makedirs(IMAGE_DIR, exist_ok=True)
if not os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, "w") as f:
        json.dump({}, f)

def save_uploaded_image(upload_file: UploadFile) -> str:
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{upload_file.filename}"
    file_path = os.path.join(IMAGE_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return filename

def log_prediction(image_filename: str, prediction: str):
    with open(LABELS_FILE, "r+") as f:
        data = json.load(f)
        data[image_filename] = {
            "prediction": prediction,
            "timestamp": datetime.now().isoformat()
        }
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
