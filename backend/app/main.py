from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Minimal car database - preloaded in memory
MAKES = ["Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Bugatti", "Buick", "Cadillac", "Chevrolet", "Chrysler", "Citroen", "Dodge", "Ferrari", "Fiat", "Ford", "Genesis", "GMC", "Honda", "Hyundai", "Infiniti", "Jaguar", "Jeep", "Kia", "Koenigsegg", "Lamborghini", "Lancia", "Land Rover", "Lexus", "Lincoln", "Lucid", "Maserati", "Mazda", "McLaren", "Mercedes-Benz", "Mini", "Mitsubishi", "Nissan", "Peugeot", "Polestar", "Porsche", "Ram", "Renault", "Rivian", "Rolls-Royce", "Saab", "Subaru", "Suzuki", "Tata", "Tesla", "Toyota", "Volkswagen", "Volvo", "Xpeng"]

MODELS = {
    "Acura": ["MDX", "RDX", "TLX", "ILX"],
    "Audi": ["A3", "A4", "A6", "Q3", "Q5", "Q7"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Chevrolet": ["Blazer", "Malibu", "Silverado", "Tahoe", "Traverse"],
    "Dodge": ["Charger", "Challenger", "Durango", "Journey"],
    "Ford": ["Edge", "Escape", "Explorer", "F-150", "Mustang", "Ranger"],
    "Honda": ["Accord", "Civic", "CR-V", "Pilot", "Odyssey"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Kona"],
    "Jeep": ["Cherokee", "Compass", "Grand Cherokee", "Wrangler"],
    "Kia": ["Forte", "Niro", "Optima", "Sportage", "Telluride"],
    "Lexus": ["ES", "IS", "RX", "GX", "LS"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "S-Class"],
    "Nissan": ["Altima", "Leaf", "Maxima", "Murano", "Rogue", "Sentra"],
    "Porsche": ["911", "Cayenne", "Macan"],
    "Ram": ["1500", "2500", "Promaster"],
    "Subaru": ["Ascent", "BRZ", "Crosstrek", "Forester", "Legacy", "Outback"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Prius", "4Runner", "Tacoma", "Tundra", "Sienna"],
    "Volkswagen": ["Golf", "Jetta", "Passat", "Tiguan", "Atlas", "ID.4"],
    "Volvo": ["S60", "S90", "XC60", "XC90"],
}

TRIMS = {
    "Acura|MDX": ["Standard", "Technology", "A-Spec"],
    "Audi|A3": ["Standard", "Premium", "Prestige"],
    "Audi|A4": ["Standard", "Premium", "Prestige"],
    "BMW|3 Series": ["318i", "320i", "330i", "340i"],
    "Chevrolet|Malibu": ["L", "LT", "RS"],
    "Chevrolet|Silverado": ["RST", "LTZ"],
    "Dodge|Charger": ["SE", "SXT", "R/T"],
    "Ford|F-150": ["Regular", "SuperCrew", "XLT"],
    "Ford|Mustang": ["EcoBoost", "GT"],
    "Honda|Accord": ["LX", "Sport", "EX"],
    "Honda|Civic": ["LX", "Sport", "EX"],
    "Honda|CR-V": ["LX", "EX", "EX-L"],
    "Hyundai|Elantra": ["SE", "SEL", "Limited"],
    "Hyundai|Tucson": ["SE", "SEL", "Limited"],
    "Jeep|Cherokee": ["Sport", "Latitude"],
    "Jeep|Grand Cherokee": ["Laredo", "Limited"],
    "Jeep|Wrangler": ["Sport", "Sahara"],
    "Kia|Forte": ["FE", "LX", "S"],
    "Kia|Sportage": ["LX", "S", "EX"],
    "Lexus|ES": ["250", "350"],
    "Lexus|IS": ["300", "350"],
    "Lexus|RX": ["350", "Hybrid"],
    "Mercedes-Benz|C-Class": ["C300", "C43 AMG"],
    "Nissan|Altima": ["S", "SV", "SL"],
    "Nissan|Rogue": ["S", "SV"],
    "Porsche|911": ["Carrera", "Turbo"],
    "Subaru|Forester": ["Base", "Premium"],
    "Subaru|Legacy": ["Base", "Premium"],
    "Tesla|Model 3": ["Standard Range", "Long Range"],
    "Tesla|Model S": ["Long Range", "Performance"],
    "Toyota|Camry": ["LE", "SE", "XLE"],
    "Toyota|Corolla": ["L", "LE", "SE"],
    "Toyota|RAV4": ["LE", "XLE", "Adventure"],
    "Toyota|Tundra": ["SR", "SR5"],
    "Volkswagen|Golf": ["S", "SE", "SEL"],
    "Volkswagen|Jetta": ["S", "SE", "SEL"],
    "Volvo|S90": ["Momentum", "Inscription"],
    "Volvo|XC90": ["Momentum", "Inscription"],
}

@app.get("/")
def root():
    return {"status": "ready", "service": "RevoMotors API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes():
    return sorted(MAKES)

@app.get("/api/cars/models")
def get_models(make: str):
    return sorted(MODELS.get(make, []))

@app.get("/api/cars/trims")
def get_trims(make: str, model: str):
    key = f"{make}|{model}"
    return sorted(TRIMS.get(key, []))

@app.get("/api/cars/decode-vin")
def decode_vin(vin: str):
    """Decode VIN using NHTSA API"""
    try:
        import requests
        
        if not vin or len(vin) < 17:
            return {"error": "Invalid VIN"}
        
        response = requests.get(
            f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json",
            timeout=5
        )
        
        if response.status_code != 200:
            return {"error": "Failed to decode"}
        
        data = response.json()
        results = data.get("Results", [])
        
        decoded = {}
        for result in results:
            var = result.get("Variable", "")
            val = result.get("Value", "")
            
            if var == "Model Year" and val:
                decoded["year"] = val
            elif var == "Make" and val:
                decoded["make"] = val
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
        return {"error": str(e)}