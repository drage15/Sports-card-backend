🧠 main.py

python
CopyEdit
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import random

app = FastAPI()

# Allow frontend (iOS app) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Listing(BaseModel):
    title: str
    price: str
    link: str

class CardResult(BaseModel):
    identified_card: str
    confidence: float
    listings: List[Listing]

@app.post("/analyze-card/", response_model=CardResult)
async def analyze_card(file: UploadFile = File(...
)):
    # TODO: Replace with real model later
    fake_cards = ["2023 Topps Chrome Shohei Ohtani", "2022 Prizm Joe Burrow", "2021 Optic LaMelo Ball"]
    card = random.choice(fake_cards)
    confidence = round(random.uniform(0.85, 0.98), 2)

    # TODO: Replace with real scraped data
    fake_listings = [
        {"title": f"{card} - PSA 10", "price": "$125.00", "link": "https://ebay.com"},
        {"title": f"{card} - Raw", "price": "$45.00", "link": "https://ebay.com"},
        {"title": f"{card} - Sold", "price": "$65.00", "link": "https://ebay.com"},
    ]

    return {
        "identified_card": card,
        "confidence": confidence,
        "listings": fake_listings
    }
