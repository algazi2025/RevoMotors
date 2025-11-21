from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
from functools import lru_cache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeadData(BaseModel):
    vin: str
    year: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    trim: Optional[str] = None
    mileage: Optional[int] = None
    color: Optional[str] = None
    transmission: Optional[str] = None
    fuelType: Optional[str] = None
    titleStatus: Optional[str] = None
    accidentHistory: Optional[str] = None
    numOwners: Optional[int] = None
    askingPrice: Optional[int] = None
    description: Optional[str] = None

COLORS = ["Pearl White", "Black", "Silver", "Gray", "White", "Red", "Blue", "Brown", "Gold", "Green", "Orange", "Yellow", "Beige", "Charcoal", "Midnight Blue", "Burgundy", "Tan", "Ivory", "Navy", "Slate"]

NHTSA_BASE = "https://vpic.nhtsa.dot.gov/api/vehicles"

@lru_cache(maxsize=256)
def get_makes_for_year(year: str):
    """Fetch makes from NHTSA for a specific year"""
    try:
        url = f"{NHTSA_BASE}/GetMakesForVehicleType/car?format=json"
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return []
        data = resp.json()
        results = data.get("Results", [])
        makes = sorted(list(set([r.get("Make_Name") for r in results if r.get("Make_Name")])))
        return makes
    except:
        return []

@lru_cache(maxsize=256)
def get_models_for_make_year(make: str, year: str):
    """Fetch models from NHTSA for a specific make and year"""
    try:
        url = f"{NHTSA_BASE}/GetModelsForMakeYear/make/{make}/year/{year}?format=json"
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return []
        data = resp.json()
        results = data.get("Results", [])
        models = sorted(list(set([r.get("Model_Name") for r in results if r.get("Model_Name")])))
        return models
    except:
        return []

@app.get("/")
def root():
    return {"status": "ready"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes(year: str = None):
    """Get all makes for a given year using NHTSA API"""
    if not year:
        year = "2024"
    makes = get_makes_for_year(year)
    return makes if makes else ["No data available"]

@app.get("/api/cars/models")
def get_models(make: str, year: str = None):
    """Get all models for a make + year using NHTSA API"""
    if not year:
        year = "2024"
    models = get_models_for_make_year(make, year)
    return models if models else []

@app.get("/api/cars/trims")
def get_trims(make: str, model: str, year: str = None):
    """Get trims - approximate based on common trim levels"""
    common_trims = ["Base", "Standard", "LE", "LX", "SE", "EX", "Limited", "Premium", "Sport", "Luxury", "XLE", "SL", "SV", "SX", "Touring", "GT", "RS", "SS", "ZL1"]
    return common_trims

@app.get("/api/cars/colors")
def get_colors():
    """Get available colors"""
    return sorted(COLORS)

@app.get("/api/cars/decode-vin")
def decode_vin(vin: str):
    """Decode VIN using NHTSA API"""
    try:
        vin = vin.strip().upper() if vin else ""
        
        if len(vin) < 17:
            return {"error": "Invalid VIN"}
        
        url = f"{NHTSA_BASE}/DecodeVin/{vin}?format=json"
        resp = requests.get(url, timeout=5)
        
        if resp.status_code != 200:
            return {"error": "Failed to decode VIN"}
        
        data = resp.json()
        results = data.get("Results", [])
        
        decoded = {}
        for r in results:
            var = r.get("Variable", "")
            val = r.get("Value", "")
            
            if var == "Model Year" and val:
                decoded["year"] = val
            elif var == "Make" and val:
                decoded["Make"] = val
            elif var == "Model" and val:
                decoded["model"] = val
            elif var == "Fuel Type - Primary" and val:
                fuel = val.lower()
                if "gasoline" in fuel:
                    decoded["fuelType"] = "gasoline"
                elif "diesel" in fuel:
                    decoded["fuelType"] = "diesel"
                elif "hybrid" in fuel:
                    decoded["fuelType"] = "hybrid"
                elif "electric" in fuel:
                    decoded["fuelType"] = "electric"
        
        return decoded
        
    except Exception as e:
        return {"error": "VIN decode failed"}

@app.post("/api/leads/webhook/lead_received")
def lead_received(lead: LeadData):
    """Receive lead submission"""
    try:
        lead_id = f"LEAD_{lead.vin[:8] if lead.vin else 'NO_VIN'}"
        
        return {
            "success": True,
            "listing_id": lead_id,
            "ai_draft_offer": {
                "fair": 24500,
                "low": 22000,
                "max": 27000
            },
            "message": "Listing received successfully"
        }
    except Exception as e:
        return {"error": str(e)}