from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Sports Card AI is live!"}

@app.post("/analyze-card")
async def analyze_card(file: UploadFile = File(...)):
    # Placeholder logic for now
    return JSONResponse({
        "card_detected": "Example Card Name",
        "suggested_matches": [
            {"site": "eBay", "listing": "https://www.ebay.com/example", "price": "$39.99"},
            {"site": "130Point", "sold": "https://www.130point.com/example", "price": "$34.50"},
        ]
    })
