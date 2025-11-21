from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAKES = ["Acura", "Audi", "BMW", "Chevrolet", "Dodge", "Ford", "Honda", "Hyundai", "Jeep", "Kia", "Lexus", "Mercedes-Benz", "Nissan", "Porsche", "Ram", "Subaru", "Tesla", "Toyota", "Volkswagen", "Volvo"]

MODELS = {
    "Acura": ["MDX", "RDX", "TLX"],
    "Audi": ["A3", "A4", "A6", "Q3", "Q5"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Chevrolet": ["Malibu", "Silverado", "Traverse"],
    "Dodge": ["Charger", "Challenger", "Durango"],
    "Ford": ["F-150", "Mustang", "Explorer"],
    "Honda": ["Accord", "Civic", "CR-V", "Pilot"],
    "Hyundai": ["Elantra", "Sonata", "Tucson"],
    "Jeep": ["Cherokee", "Grand Cherokee", "Wrangler"],
    "Kia": ["Forte", "Sportage", "Telluride"],
    "Lexus": ["ES", "IS", "RX"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class"],
    "Nissan": ["Altima", "Rogue", "Sentra"],
    "Porsche": ["911", "Cayenne"],
    "Ram": ["1500", "2500"],
    "Subaru": ["Forester", "Legacy", "Outback"],
    "Tesla": ["Model 3", "Model S", "Model Y"],
    "Toyota": ["Camry", "Corolla", "RAV4", "Tundra"],
    "Volkswagen": ["Golf", "Jetta", "Passat"],
    "Volvo": ["S90", "XC90"],
}

TRIMS = {
    "Acura|MDX": ["Standard", "Technology"],
    "Audi|A3": ["Standard", "Premium"],
    "BMW|3 Series": ["318i", "320i", "330i"],
    "Chevrolet|Malibu": ["L", "LT", "RS"],
    "Chevrolet|Silverado": ["RST", "LTZ"],
    "Dodge|Charger": ["SE", "SXT", "R/T"],
    "Ford|F-150": ["Regular", "SuperCrew", "XLT"],
    "Ford|Mustang": ["EcoBoost", "GT"],
    "Honda|Accord": ["LX", "Sport", "EX"],
    "Honda|Civic": ["LX", "Sport", "EX"],
    "Honda|CR-V": ["LX", "EX", "EX-L"],
    "Honda|Pilot": ["LX", "EX", "Touring"],
    "Hyundai|Elantra": ["SE", "SEL", "Limited"],
    "Hyundai|Sonata": ["SE", "SEL", "Limited"],
    "Hyundai|Tucson": ["SE", "SEL", "Limited"],
    "Jeep|Cherokee": ["Sport", "Latitude"],
    "Jeep|Grand Cherokee": ["Laredo", "Limited"],
    "Jeep|Wrangler": ["Sport", "Sahara"],
    "Kia|Forte": ["FE", "LX", "S"],
    "Kia|Sportage": ["LX", "S", "EX"],
    "Kia|Telluride": ["LX", "EX"],
    "Lexus|ES": ["250", "350"],
    "Lexus|IS": ["300", "350"],
    "Lexus|RX": ["350", "Hybrid"],
    "Mercedes-Benz|C-Class": ["C300", "C43 AMG"],
    "Mercedes-Benz|E-Class": ["E350", "E450"],
    "Mercedes-Benz|S-Class": ["S500", "S580"],
    "Nissan|Altima": ["S", "SV", "SL"],
    "Nissan|Rogue": ["S", "SV"],
    "Nissan|Sentra": ["S", "SV"],
    "Porsche|911": ["Carrera", "Turbo"],
    "Porsche|Cayenne": ["Base", "S"],
    "Ram|1500": ["Tradesman", "SLT"],
    "Ram|2500": ["Tradesman", "SLT"],
    "Subaru|Forester": ["Base", "Premium"],
    "Subaru|Legacy": ["Base", "Premium"],
    "Subaru|Outback": ["Base", "Premium"],
    "Tesla|Model 3": ["Standard", "Long Range"],
    "Tesla|Model S": ["Long Range", "Performance"],
    "Tesla|Model Y": ["RWD", "Long Range"],
    "Toyota|Camry": ["LE", "SE", "XLE"],
    "Toyota|Corolla": ["L", "LE", "SE"],
    "Toyota|RAV4": ["LE", "XLE"],
    "Toyota|Tundra": ["SR", "SR5"],
    "Volkswagen|Golf": ["S", "SE"],
    "Volkswagen|Jetta": ["S", "SE"],
    "Volkswagen|Passat": ["S", "SE"],
    "Volvo|S90": ["Momentum", "Inscription"],
    "Volvo|XC90": ["Momentum", "Inscription"],
}

@app.get("/")
def root():
    return {"status": "ready"}

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
        # Lazy import - only import when needed
        import requests
        
        vin = vin.strip().upper() if vin else ""
        
        if len(vin) < 17:
            return {"error": "Invalid VIN"}
        
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
        resp = requests.get(url, timeout=5)
        
        if resp.status_code != 200:
            return {"error": "Failed"}
        
        data = resp.json()
        results = data.get("Results", [])
        
        decoded = {}
        for r in results:
            var = r.get("Variable", "")
            val = r.get("Value", "")
            
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
        return {"error": "VIN decode failed"}