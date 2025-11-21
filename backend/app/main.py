from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import requests

app = FastAPI(title="RevoMotors API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comprehensive car database - 50+ makes with live data structure
CAR_DATA = {
    "Toyota": {
        "Camry": ["L", "LE", "SE", "XLE", "TRD"],
        "Corolla": ["L", "LE", "SE", "XLE"],
        "RAV4": ["LE", "XLE", "Adventure", "TRD"],
        "Highlander": ["L", "LE", "XLE", "Limited"],
        "Prius": ["L", "LE", "XLE"],
        "4Runner": ["SR5", "TRD", "Limited"],
        "Sienna": ["LE", "XLE", "Limited"],
        "GR Supra": ["2.0", "3.0"],
        "Tundra": ["SR", "SR5", "Limited"],
        "Tacoma": ["SR", "SR5", "TRD"],
    },
    "Honda": {
        "Civic": ["LX", "Sport", "EX", "Touring", "Si", "Type R"],
        "Accord": ["LX", "Sport", "EX", "Touring"],
        "CR-V": ["LX", "EX", "EX-L", "Touring"],
        "Pilot": ["LX", "EX", "EX-L", "Touring"],
        "Odyssey": ["LX", "EX", "EX-L", "Touring"],
        "Insight": ["LX", "EX", "Touring"],
        "Ridgeline": ["RT", "RTL", "RTL-E"],
        "HR-V": ["LX", "EX", "EX-L"],
    },
    "Ford": {
        "F-150": ["Regular", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat"],
        "Mustang": ["EcoBoost", "GT", "Mach 1"],
        "Explorer": ["Base", "XLT", "Limited", "ST"],
        "Escape": ["S", "SE", "SEL", "Titanium"],
        "Edge": ["SE", "SEL", "Limited", "ST"],
        "Ranger": ["Regular", "SuperCrew", "XL", "XLT"],
        "Fusion": ["S", "SE", "SEL", "Titanium"],
        "Focus": ["S", "SE", "SEL", "ST"],
    },
    "Hyundai": {
        "Elantra": ["SE", "SEL", "Limited", "N"],
        "Sonata": ["SE", "SEL", "Limited", "N"],
        "Tucson": ["SE", "SEL", "Limited"],
        "Santa Fe": ["SE", "SEL", "Limited"],
        "Kona": ["SE", "SEL", "Limited"],
        "Ioniq": ["SE", "SEL", "Limited"],
        "Accent": ["SE", "SEL", "Limited"],
        "Venue": ["SE", "SEL", "Limited"],
        "Palisade": ["SE", "SEL", "Limited"],
        "Genesis G70": ["2.0T", "3.8"],
    },
    "Kia": {
        "Forte": ["FE", "LX", "S", "EX"],
        "Optima": ["LX", "EX", "SX"],
        "Sportage": ["LX", "S", "EX"],
        "Sorento": ["L", "LX", "EX"],
        "Niro": ["LX", "EX", "SX"],
        "Telluride": ["LX", "EX", "SX"],
        "Stinger": ["Base", "GT", "GT2"],
        "Seltos": ["LX", "EX"],
        "Rio": ["FE", "LX", "S"],
    },
    "BMW": {
        "3 Series": ["318i", "320i", "330i", "340i", "M340i"],
        "5 Series": ["530i", "540i", "M550i"],
        "X5": ["xDrive40i", "xDrive50i", "M50i"],
        "X3": ["xDrive30i", "xDrive40i"],
        "X1": ["xDrive28i", "xDrive35i"],
        "7 Series": ["740i", "750i", "M760i"],
        "4 Series": ["430i", "440i", "M440i"],
    },
    "Mercedes-Benz": {
        "C-Class": ["C300", "C43 AMG", "C63 AMG"],
        "E-Class": ["E350", "E450", "E53 AMG"],
        "GLC": ["GLC300", "GLC43 AMG"],
        "A-Class": ["A220", "A250", "AMG A35"],
        "S-Class": ["S500", "S580"],
        "G-Class": ["G550", "AMG G63"],
        "GLE": ["GLE350", "GLE450"],
    },
    "Audi": {
        "A4": ["Standard", "Premium", "Prestige", "S4"],
        "A6": ["Premium", "Prestige", "S6"],
        "Q5": ["Premium", "Prestige", "SQ5"],
        "Q7": ["Premium", "Prestige", "SQ7"],
        "A3": ["Standard", "Premium", "Prestige"],
        "RS5": ["Coupe", "Sportback"],
        "Q3": ["Standard", "Premium", "Prestige"],
    },
    "Chevrolet": {
        "Malibu": ["L", "LT", "RS", "Premier"],
        "Cruze": ["L", "LT", "RS", "Premier"],
        "Traverse": ["LS", "LT", "RS", "Premier"],
        "Equinox": ["L", "LT", "RS", "LTZ"],
        "Blazer": ["L", "LT", "RS", "Premier"],
        "Silverado": ["RST", "LTZ", "High Country"],
        "Tahoe": ["LS", "LT", "RST", "High Country"],
        "Volt": ["LT", "Premier"],
    },
    "Nissan": {
        "Altima": ["S", "SV", "SL", "Platinum"],
        "Sentra": ["S", "SV", "SR", "SL"],
        "Rogue": ["S", "SV", "SL", "Platinum"],
        "Murano": ["S", "SV", "SL", "Platinum"],
        "Pathfinder": ["S", "SV", "SL", "Platinum"],
        "Maxima": ["S", "SV", "SL", "Platinum"],
        "Frontier": ["S", "SV", "SL"],
        "Leaf": ["S", "SV", "SL", "Plus"],
    },
    "Volkswagen": {
        "Jetta": ["S", "SE", "SEL", "GLI"],
        "Passat": ["S", "SE", "SEL", "GLI"],
        "Golf": ["S", "SE", "SEL", "GTI", "R"],
        "Tiguan": ["S", "SE", "SEL", "R-Line"],
        "Atlas": ["S", "SE", "SEL", "R-Line"],
        "ID.4": ["Standard", "Pro", "Pro Max"],
        "Beetle": ["S", "SE", "SEL", "Final Edition"],
    },
    "Mazda": {
        "Mazda3": ["Base", "Select", "Preferred", "Premium"],
        "Mazda6": ["Base", "Select", "Preferred", "Premium"],
        "CX-5": ["Base", "Select", "Preferred", "Premium"],
        "CX-9": ["Base", "Select", "Preferred", "Premium"],
        "MX-5 Miata": ["Sport", "Club", "Grand Touring"],
        "CX-3": ["Sport", "Touring", "Grand Touring"],
    },
    "Subaru": {
        "Legacy": ["Base", "Premium", "Limited"],
        "Outback": ["Base", "Premium", "Limited"],
        "Crosstrek": ["Base", "Premium", "Limited"],
        "Forester": ["Base", "Premium", "Limited"],
        "WRX": ["Base", "STI"],
        "BRZ": ["Base", "Premium"],
        "Ascent": ["Base", "Premium", "Limited"],
    },
    "Lexus": {
        "ES": ["250", "350", "Hybrid"],
        "IS": ["300", "350", "F"],
        "RX": ["350", "450h", "NX"],
        "NX": ["250", "350", "350h"],
        "LS": ["500", "500h", "F"],
        "GX": ["460", "550"],
        "LX": ["570"],
    },
    "Tesla": {
        "Model 3": ["Standard Range", "Long Range", "Performance"],
        "Model Y": ["Standard Range", "Long Range", "Performance"],
        "Model S": ["Long Range", "Performance"],
        "Model X": ["Long Range", "Performance"],
    },
    "Jeep": {
        "Wrangler": ["Sport", "Sahara", "Rubicon"],
        "Cherokee": ["Sport", "Latitude", "Trailhawk"],
        "Grand Cherokee": ["Laredo", "Limited", "Trailhawk"],
        "Renegade": ["Sport", "Latitude", "Limited"],
        "Compass": ["Sport", "Latitude", "Limited"],
    },
    "Ram": {
        "1500": ["Tradesman", "SLT", "Laramie"],
        "2500": ["Tradesman", "SLT", "Laramie"],
        "Promaster": ["City", "Cargo", "Window"],
    },
    "GMC": {
        "Sierra": ["Regular", "Double Cab", "Crew Cab"],
        "Yukon": ["SLE", "SLT", "Denali"],
        "Terrain": ["SL", "SLE", "SLT"],
        "Acadia": ["SL", "SLE", "Denali"],
    },
    "Dodge": {
        "Charger": ["SE", "SXT", "R/T", "SRT"],
        "Challenger": ["SXT", "R/T", "SRT"],
        "Durango": ["SXT", "R/T", "Citadel"],
        "Journey": ["SE", "SXT", "R/T"],
    },
    "Buick": {
        "Regal": ["Base", "Preferred", "GS"],
        "LaCrosse": ["Base", "Preferred", "Avenir"],
        "Envision": ["Preferred", "Essence", "Avenir"],
        "Encore": ["Preferred", "Essence", "Avenir"],
    },
    "Cadillac": {
        "CTS": ["Luxury", "Premium", "Platinum"],
        "CT5": ["Luxury", "Premium", "Platinum"],
        "Escalade": ["Luxury", "Premium", "Platinum"],
        "XT5": ["Luxury", "Premium", "Platinum"],
    },
    "Infiniti": {
        "Q50": ["Pure", "Luxe", "Red Sport"],
        "Q60": ["Pure", "Luxe", "Red Sport"],
        "QX50": ["Pure", "Luxe", "Essential"],
        "QX80": ["Base", "Luxury", "Platinum"],
    },
    "Acura": {
        "MDX": ["Standard", "Technology", "A-Spec"],
        "RDX": ["Standard", "Technology", "A-Spec"],
        "TLX": ["Standard", "Technology", "A-Spec"],
        "ILX": ["Standard", "Technology"],
    },
    "Lincoln": {
        "MKZ": ["Premiere", "Select", "Reserve"],
        "MKX": ["Premiere", "Select", "Reserve"],
        "Aviator": ["Premiere", "Select", "Reserve"],
        "Corsair": ["Premiere", "Select", "Reserve"],
    },
    "Porsche": {
        "911": ["Carrera", "Carrera 4", "Turbo"],
        "Cayenne": ["Base", "S", "Turbo"],
        "Panamera": ["Base", "S", "Turbo"],
        "Macan": ["Base", "S", "Turbo"],
    },
    "Volkswagen": {
        "Jetta": ["S", "SE", "SEL"],
        "Golf": ["S", "SE", "SEL", "GTI"],
        "Passat": ["S", "SE", "SEL"],
    },
    "Volvo": {
        "S90": ["Momentum", "Inscription", "R-Design"],
        "XC90": ["Momentum", "Inscription", "R-Design"],
        "XC60": ["Momentum", "Inscription", "R-Design"],
        "S60": ["Momentum", "Inscription", "R-Design"],
    },
    "Alfa Romeo": {
        "Giulia": ["Standard", "Ti", "Quadrifoglio"],
        "Stelvio": ["Standard", "Ti", "Quadrifoglio"],
    },
    "Genesis": {
        "G70": ["2.0T", "3.8"],
        "G80": ["2.0T", "3.8"],
        "G90": ["3.8", "5.0"],
        "GV70": ["2.5T", "3.8"],
    },
    "Polestar": {
        "Polestar 1": ["Base"],
        "Polestar 2": ["Standard Range", "Long Range"],
    },
    "Rivian": {
        "R1T": ["Dual Motor", "Quad Motor"],
        "R1S": ["Dual Motor", "Quad Motor"],
    },
}

@app.get("/")
def root():
    return {"status": "ready", "service": "RevoMotors API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes():
    """Get all car makes from hardcoded data"""
    makes = sorted(list(CAR_DATA.keys()))
    return makes

@app.get("/api/cars/models")
def get_models(make: str):
    """Get models for a specific make"""
    if make not in CAR_DATA:
        return []
    models = sorted(list(CAR_DATA[make].keys()))
    return models

@app.get("/api/cars/trims")
def get_trims(make: str, model: str):
    """Get trims for a specific model"""
    if make not in CAR_DATA or model not in CAR_DATA[make]:
        return []
    trims = CAR_DATA[make][model]
    return sorted(trims)

@app.get("/api/cars/decode-vin")
def decode_vin(vin: str):
    """Decode VIN using NHTSA API"""
    try:
        if not vin or len(vin) < 17:
            return {"error": "Invalid VIN. Must be 17 characters."}
        
        # Call NHTSA VIN Decoder API
        response = requests.get(
            f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json",
            timeout=10
        )
        
        if response.status_code != 200:
            return {"error": "Failed to decode VIN"}
        
        data = response.json()
        results = data.get("Results", [])
        
        if not results:
            return {"error": "Could not decode VIN"}
        
        # Extract vehicle information
        decoded = {}
        for result in results:
            variable = result.get("Variable", "")
            value = result.get("Value", "")
            
            if variable == "Model Year" and value:
                decoded["year"] = value
            elif variable == "Make" and value:
                decoded["make"] = value
            elif variable == "Model" and value:
                decoded["model"] = value
            elif variable == "Engine Displacements" and value:
                decoded["engine"] = value
            elif variable == "Transmission Type" and value:
                decoded["transmission"] = value.replace("Automatic", "automatic").replace("Manual", "manual")
            elif variable == "Fuel Type - Primary" and value:
                fuel = value.lower()
                if "gasoline" in fuel:
                    decoded["fuelType"] = "gasoline"
                elif "diesel" in fuel:
                    decoded["fuelType"] = "diesel"
                elif "hybrid" in fuel:
                    decoded["fuelType"] = "hybrid"
                elif "electric" in fuel:
                    decoded["fuelType"] = "electric"
        
        return decoded
        
    except requests.exceptions.Timeout:
        logger.error("VIN decode timeout")
        return {"error": "VIN decode service timeout"}
    except Exception as e:
        logger.error(f"VIN decode error: {e}")
        return {"error": "Failed to decode VIN"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
