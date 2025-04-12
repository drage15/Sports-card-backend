import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

# === Paths ===
DATA_DIR = "training_data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
LABELS_FILE = os.path.join(DATA_DIR, "labels.json")

# === Parameters ===
IMG_SIZE = (224, 224)

# === Load Labels ===
with open(LABELS_FILE, "r") as f:
    raw_labels = json.load(f)

image_paths = []
labels = []

for filename, info in raw_labels.items():
    full_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(full_path):
        image_paths.append(full_path)
        labels.append(info["prediction"])

# === Encode Labels ===
le = LabelEncoder()
labels_encoded = le.fit_transform(labels)

# === Load and Preprocess Images ===
images = []
for path in image_paths:
    img = load_img(path, target_size=IMG_SIZE)
    img_array = img_to_array(img) / 255.0  # Normalize
    images.append(img_array)

X = np.array(images)
y = np.array(labels_encoded)

# === Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Define Model ===
model = models.Sequential([
    layers.Input(shape=(*IMG_SIZE, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(le.classes_), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# === Train Model ===
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# === Save Model and Label Encoder ===
model.save("card_classifier.h5")
with open("label_encoder.json", "w") as f:
    json.dump(le.classes_.tolist(), f)

print("✅ Model training complete and saved as card_classifier.h5")
