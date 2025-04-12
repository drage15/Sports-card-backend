from fastapi import APIRouter, UploadFile, File
from app.utils.helpers import save_uploaded_image, log_prediction
import random

router = APIRouter()

@router.post("/card")
async def analyze_card(file: UploadFile = File(...)):
    filename = save_uploaded_image(file)

    cards = ["2023 Topps Chrome Shohei Ohtani", "2022 Prizm Joe Burrow", "2021 Optic LaMelo Ball"]
    card = random.choice(cards)
    confidence = round(random.uniform(0.85, 0.98), 2)

    listings = [
        {"title": f"{card} - PSA 10", "price": "$125.00", "link": "https://ebay.com"},
        {"title": f"{card} - Raw", "price": "$45.00", "link": "https://ebay.com"},
        {"title": f"{card} - Sold", "price": "$65.00", "link": "https://ebay.com"},
    ]

    log_prediction(filename, card)

    return {
        "identified_card": card,
        "confidence": confidence,
        "listings": listings
    }
