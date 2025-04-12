from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import json
from datetime import datetime

app = FastAPI()


# === Setup Directories ===
DATA_DIR = "training_data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
LABELS_FILE = os.path.join(DATA_DIR, "labels.json")

os.makedirs(IMAGE_DIR, exist_ok=True)
if not os.path.exists(LABELS_FILE):
    with open(LABELS_FILE, "w") as f:
        json.dump({}, f)

# === Save Uploaded Image ===
def save_uploaded_image(upload_file: UploadFile) -> str:
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{upload_file.filename}"
    file_path = os.path.join(IMAGE_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return filename

# === Log Prediction ===
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

# === Routes ===

@app.get("/")
def read_root():
    return {"message": "Sports Card AI is live!"}

@app.post("/analyze-card")
async def analyze_card(file: UploadFile = File(...)):
    # Save image
    filename = save_uploaded_image(file)

    # Placeholder AI logic
    prediction = "Example Card Name"

    # Log the prediction
    log_prediction(filename, prediction)

    # Return fake match results
    return JSONResponse({
        "card_detected": prediction,
        "suggested_matches": [
            {"site": "eBay", "listing": "https://www.ebay.com/example", "price": "$39.99"},
            {"site": "130Point", "sold": "https://www.130point.com/example", "price": "$34.50"},
        ]
    })
