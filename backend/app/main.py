from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import requests
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(title="RevoMotors API", version="1.0.0")

# Add CORS middleware FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Car database
CAR_DATA: Dict = {
    "Acura": {"MDX": ["Standard", "Technology", "A-Spec"], "RDX": ["Standard", "Technology", "A-Spec"], "TLX": ["Standard", "Technology"], "ILX": ["Standard", "Technology"]},
    "Alfa Romeo": {"Giulia": ["Standard", "Ti", "Quadrifoglio"], "Stelvio": ["Standard", "Ti", "Quadrifoglio"]},
    "Aston Martin": {"DB11": ["Base", "AMR"], "Vantage": ["Base", "AMR"]},
    "Audi": {"A3": ["Standard", "Premium", "Prestige"], "A4": ["Standard", "Premium", "Prestige"], "A6": ["Premium", "Prestige"], "Q3": ["Standard", "Premium"], "Q5": ["Premium", "Prestige"], "Q7": ["Premium", "Prestige"]},
    "Bentley": {"Continental": ["GT", "Flying Spur"], "Mulsanne": ["Speed"]},
    "BMW": {"3 Series": ["318i", "320i", "330i", "340i"], "5 Series": ["530i", "540i"], "X3": ["xDrive30i", "xDrive40i"], "X5": ["xDrive40i", "xDrive50i"]},
    "Bugatti": {"Chiron": ["Base", "Speed"]},
    "Buick": {"Regal": ["Base", "Preferred"], "Envision": ["Preferred", "Essence"], "Encore": ["Preferred", "Essence"]},
    "Cadillac": {"CT5": ["Luxury", "Premium"], "Escalade": ["Luxury", "Premium"], "XT5": ["Luxury", "Premium"]},
    "Chevrolet": {"Blazer": ["L", "LT", "RS"], "Malibu": ["L", "LT", "RS"], "Silverado": ["RST", "LTZ"], "Tahoe": ["LS", "LT"], "Traverse": ["LS", "LT", "RS"]},
    "Chrysler": {"300": ["Base", "Limited"], "Pacifica": ["Touring", "Limited"]},
    "Citroen": {"C3": ["Base", "Feel"], "C4": ["Live", "Shine"]},
    "Dodge": {"Charger": ["SE", "SXT", "R/T"], "Challenger": ["SXT", "R/T"], "Durango": ["SXT", "R/T"], "Journey": ["SE", "SXT"]},
    "Ferrari": {"F8 Tributo": ["Base"], "Portofino": ["Base"]},
    "Fiat": {"500": ["Pop", "Sport"], "500X": ["Pop", "Sport"]},
    "Ford": {"Edge": ["SE", "SEL", "Limited"], "Escape": ["S", "SE", "SEL"], "Explorer": ["Base", "XLT", "Limited"], "F-150": ["Regular", "SuperCrew", "XLT"], "Mustang": ["EcoBoost", "GT"], "Ranger": ["Regular", "SuperCrew"]},
    "Genesis": {"G70": ["2.0T", "3.8"], "G80": ["2.0T", "3.8"], "GV70": ["2.5T", "3.8"]},
    "GMC": {"Acadia": ["SL", "SLE"], "Sierra": ["Regular", "Crew Cab"], "Yukon": ["SLE", "SLT"]},
    "Honda": {"Accord": ["LX", "Sport", "EX"], "Civic": ["LX", "Sport", "EX"], "CR-V": ["LX", "EX", "EX-L"], "Pilot": ["LX", "EX", "Touring"], "Odyssey": ["LX", "EX", "Touring"]},
    "Hyundai": {"Elantra": ["SE", "SEL", "Limited"], "Sonata": ["SE", "SEL", "Limited"], "Tucson": ["SE", "SEL", "Limited"], "Santa Fe": ["SE", "SEL", "Limited"], "Kona": ["SE", "SEL", "Limited"]},
    "Infiniti": {"Q50": ["Pure", "Luxe"], "Q60": ["Pure", "Luxe"], "QX50": ["Pure", "Luxe"], "QX80": ["Base", "Luxury"]},
    "Jaguar": {"F-Pace": ["Base", "Premium"], "F-Type": ["Base", "R"], "XE": ["Base", "Premium"]},
    "Jeep": {"Cherokee": ["Sport", "Latitude"], "Compass": ["Sport", "Latitude"], "Grand Cherokee": ["Laredo", "Limited"], "Wrangler": ["Sport", "Sahara"]},
    "Kia": {"Forte": ["FE", "LX", "S"], "Niro": ["LX", "EX", "SX"], "Optima": ["LX", "EX"], "Sportage": ["LX", "S", "EX"], "Telluride": ["LX", "EX"]},
    "Koenigsegg": {"Agera": ["Base", "RS"]},
    "Lamborghini": {"Aventador": ["Base", "S"], "Huracán": ["Base", "Performante"]},
    "Land Rover": {"Discovery": ["SE", "HSE"], "Range Rover": ["Base", "Sport"], "Range Rover Evoque": ["Base", "HSE"]},
    "Lexus": {"ES": ["250", "350"], "IS": ["300", "350"], "RX": ["350", "Hybrid"], "GX": ["460", "550"], "LS": ["500", "Hybrid"]},
    "Lincoln": {"Aviator": ["Premiere", "Select"], "Corsair": ["Premiere", "Select"], "MKZ": ["Premiere", "Select"]},
    "Lucid": {"Air": ["Pure", "Touring"]},
    "Maserati": {"Ghibli": ["Base", "S"], "Levante": ["Base", "S"]},
    "Mazda": {"CX-3": ["Sport", "Touring"], "CX-5": ["Base", "Select"], "CX-9": ["Base", "Select"], "Mazda3": ["Base", "Select"], "Mazda6": ["Base", "Select"]},
    "McLaren": {"570GT": ["Base"], "720S": ["Base"]},
    "Mercedes-Benz": {"C-Class": ["C300", "C43 AMG"], "E-Class": ["E350", "E450"], "GLC": ["GLC300", "GLC43"], "S-Class": ["S500", "S580"]},
    "Mini": {"Clubman": ["Base", "Cooper"], "Countryman": ["Base", "Cooper"]},
    "Mitsubishi": {"Eclipse": ["Base", "Cross"], "Outlander": ["ES", "SEL"], "Lancer": ["ES", "SEL"]},
    "Nissan": {"Altima": ["S", "SV", "SL"], "Leaf": ["S", "SV", "SL"], "Maxima": ["S", "SV"], "Murano": ["S", "SV"], "Pathfinder": ["S", "SV"], "Rogue": ["S", "SV"], "Sentra": ["S", "SV"]},
    "Peugeot": {"208": ["Active", "Allure"], "308": ["Active", "Allure"], "3008": ["Active", "Allure"]},
    "Polestar": {"2": ["Standard Range", "Long Range"]},
    "Porsche": {"911": ["Carrera", "Turbo"], "Cayenne": ["Base", "S"], "Macan": ["Base", "S"]},
    "Ram": {"1500": ["Tradesman", "SLT"], "2500": ["Tradesman", "SLT"], "Promaster": ["City", "Cargo"]},
    "Renault": {"Clio": ["Base", "Interactive"], "Espace": ["Base", "Dynamique"]},
    "Rivian": {"R1S": ["Dual Motor", "Quad Motor"], "R1T": ["Dual Motor", "Quad Motor"]},
    "Rolls-Royce": {"Ghost": ["Base"], "Phantom": ["Base"]},
    "Saab": {"9-3": ["Base", "Sport"], "9-5": ["Base", "Aero"]},
    "Subaru": {"Ascent": ["Base", "Premium"], "BRZ": ["Base", "Premium"], "Crosstrek": ["Base", "Premium"], "Forester": ["Base", "Premium"], "Legacy": ["Base", "Premium"], "Outback": ["Base", "Premium"]},
    "Suzuki": {"Swift": ["Base", "VXi"], "Vitara": ["Base", "SZ5"], "S-Cross": ["Base", "ZXi"]},
    "Tata": {"Nexon": ["XE", "XM"], "Harrier": ["XE", "XM"]},
    "Tesla": {"Model 3": ["Standard Range", "Long Range"], "Model S": ["Long Range", "Performance"], "Model X": ["Long Range", "Performance"], "Model Y": ["RWD", "Long Range"]},
    "Toyota": {"Camry": ["LE", "SE", "XLE"], "Corolla": ["L", "LE", "SE"], "RAV4": ["LE", "XLE", "Adventure"], "Highlander": ["L", "LE", "XLE"], "Prius": ["L", "LE", "XLE"], "4Runner": ["SR5", "TRD"], "Tacoma": ["SR", "SR5"], "Tundra": ["SR", "SR5"], "Sienna": ["LE", "XLE"]},
    "Volkswagen": {"Golf": ["S", "SE", "SEL"], "Jetta": ["S", "SE", "SEL"], "Passat": ["S", "SE", "SEL"], "Tiguan": ["S", "SE", "SEL"], "Atlas": ["S", "SE", "SEL"], "ID.4": ["Standard", "Pro"]},
    "Volvo": {"S60": ["Momentum", "Inscription"], "S90": ["Momentum", "Inscription"], "XC60": ["Momentum", "Inscription"], "XC90": ["Momentum", "Inscription"]},
    "Xpeng": {"G9": ["Base", "Plus"], "P7": ["Base", "Plus"]},
}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"status": "ready", "service": "RevoMotors API", "version": "1.0.0"}

# Health check
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

# Get all makes
@app.get("/api/cars/makes")
async def get_makes() -> List[str]:
    """Get all car makes"""
    try:
        makes = sorted(list(CAR_DATA.keys()))
        logger.info(f"Returned {len(makes)} makes")
        return makes
    except Exception as e:
        logger.error(f"Error in get_makes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching makes")

# Get models for a make
@app.get("/api/cars/models")
async def get_models(make: str) -> List[str]:
    """Get models for a specific make"""
    try:
        if not make:
            return []
        if make not in CAR_DATA:
            logger.warning(f"Make not found: {make}")
            return []
        models = sorted(list(CAR_DATA[make].keys()))
        logger.info(f"Returned {len(models)} models for {make}")
        return models
    except Exception as e:
        logger.error(f"Error in get_models: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching models")

# Get trims for a model
@app.get("/api/cars/trims")
async def get_trims(make: str, model: str) -> List[str]:
    """Get trims for a specific model"""
    try:
        if not make or not model:
            return []
        if make not in CAR_DATA:
            logger.warning(f"Make not found: {make}")
            return []
        if model not in CAR_DATA[make]:
            logger.warning(f"Model not found: {model} for {make}")
            return []
        trims = sorted(CAR_DATA[make][model])
        logger.info(f"Returned {len(trims)} trims for {make} {model}")
        return trims
    except Exception as e:
        logger.error(f"Error in get_trims: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching trims")

# Decode VIN
@app.get("/api/cars/decode-vin")
async def decode_vin(vin: str) -> dict:
    """Decode VIN using NHTSA API"""
    try:
        if not vin:
            return {"error": "VIN is required"}
        
        vin = vin.strip().upper()
        
        if len(vin) < 17:
            return {"error": "Invalid VIN. Must be at least 17 characters."}
        
        # Call NHTSA VIN Decoder API
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
        logger.info(f"Decoding VIN: {vin}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"NHTSA API error: {response.status_code}")
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
            
            if not value:
                continue
                
            if variable == "Model Year":
                decoded["year"] = value
            elif variable == "Make":
                decoded["make"] = value
            elif variable == "Model":
                decoded["model"] = value
            elif variable == "Engine Displacements":
                decoded["engine"] = value
            elif variable == "Transmission Type":
                trans = value.lower()
                if "automatic" in trans:
                    decoded["transmission"] = "automatic"
                elif "manual" in trans:
                    decoded["transmission"] = "manual"
                elif "cvt" in trans:
                    decoded["transmission"] = "cvt"
            elif variable == "Fuel Type - Primary":
                fuel = value.lower()
                if "gasoline" in fuel:
                    decoded["fuelType"] = "gasoline"
                elif "diesel" in fuel:
                    decoded["fuelType"] = "diesel"
                elif "hybrid" in fuel or "electric" in fuel:
                    decoded["fuelType"] = "hybrid"
                elif "electric" in fuel:
                    decoded["fuelType"] = "electric"
        
        logger.info(f"VIN decoded successfully: {decoded}")
        return decoded
        
    except requests.exceptions.Timeout:
        logger.error("VIN decode timeout")
        return {"error": "VIN decode service timeout"}
    except requests.exceptions.ConnectionError:
        logger.error("VIN decode connection error")
        return {"error": "Failed to connect to VIN decoder service"}
    except Exception as e:
        logger.error(f"VIN decode error: {str(e)}")
        return {"error": f"Failed to decode VIN: {str(e)}"}

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    logger.info(f"Loaded {len(CAR_DATA)} makes and {sum(len(v) for v in CAR_DATA.values())} models")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")