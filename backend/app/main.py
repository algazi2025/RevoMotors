from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
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

MAKES_BY_YEAR = {
    "Acura": (1986, 2025), "Alfa Romeo": (1910, 2025), "Aston Martin": (1913, 2025), "Audi": (1968, 2025), "Bentley": (1919, 2025),
    "BMW": (1916, 2025), "Bugatti": (1909, 2025), "Buick": (1903, 2025), "Cadillac": (1902, 2025), "Chevrolet": (1911, 2025),
    "Chrysler": (1924, 2025), "Citroen": (1919, 2025), "Dodge": (1914, 2025), "Ferrari": (1947, 2025), "Fiat": (1899, 2025),
    "Ford": (1908, 2025), "Genesis": (2015, 2025), "GMC": (1912, 2025), "Honda": (1959, 2025), "Hyundai": (1986, 2025),
    "Infiniti": (1989, 2025), "Jaguar": (1935, 2025), "Jeep": (1941, 2025), "Kia": (1992, 2025), "Lamborghini": (1963, 2025),
    "Land Rover": (1948, 2025), "Lexus": (1989, 2025), "Lincoln": (1917, 2025), "Lucid": (2021, 2025), "Maserati": (1926, 2025),
    "Mazda": (1960, 2025), "McLaren": (1985, 2025), "Mercedes-Benz": (1901, 2025), "Mini": (1959, 2025), "Mitsubishi": (1917, 2025),
    "Nissan": (1933, 2025), "Polestar": (2017, 2025), "Porsche": (1948, 2025), "Ram": (2010, 2025), "Renault": (1898, 2025),
    "Rivian": (2021, 2025), "Rolls-Royce": (1906, 2025), "Saab": (1947, 2025), "Subaru": (1958, 2025), "Suzuki": (1955, 2025),
    "Tata": (1998, 2025), "Tesla": (2008, 2025), "Toyota": (1936, 2025), "Volkswagen": (1937, 2025), "Volvo": (1927, 2025), "Xpeng": (2017, 2025),
}

MODELS_DATABASE = {
    "Acura": [("ILX", 2013, 2025), ("MDX", 2001, 2025), ("RDX", 2006, 2025), ("TLX", 2014, 2025)],
    "Audi": [("A3", 1996, 2025), ("A4", 1994, 2025), ("A6", 1997, 2025), ("Q3", 2011, 2025), ("Q5", 2008, 2025)],
    "BMW": [("3 Series", 1975, 2025), ("5 Series", 1972, 2025), ("X1", 2009, 2025), ("X3", 2003, 2025), ("X5", 1999, 2025)],
    "Chevrolet": [("Camaro", 1966, 2025), ("Corvette", 1953, 2025), ("Cruze", 2009, 2019), ("Equinox", 2004, 2025), ("Malibu", 1964, 2025), ("Silverado 1500", 1999, 2025)],
    "Chrysler": [("300", 2004, 2025), ("Pacifica", 2017, 2025)],
    "Dodge": [("Charger", 1966, 2025), ("Challenger", 1970, 2025), ("Durango", 1998, 2025)],
    "Ford": [("Edge", 2006, 2025), ("Escape", 2000, 2025), ("Explorer", 1990, 2025), ("F-150", 1997, 2025), ("Mustang", 1964, 2025)],
    "Genesis": [("G70", 2017, 2025), ("G80", 2015, 2025), ("G90", 2015, 2025), ("GV70", 2021, 2025), ("GV80", 2020, 2025)],
    "GMC": [("Acadia", 2007, 2025), ("Sierra 1500", 1999, 2025), ("Yukon", 1992, 2025)],
    "Honda": [("Accord", 1976, 2025), ("Civic", 1972, 2025), ("CR-V", 1996, 2025), ("Odyssey", 1994, 2025), ("Pilot", 2002, 2025)],
    "Hyundai": [("Accent", 1994, 2025), ("Elantra", 1990, 2025), ("Kona", 2017, 2025), ("Santa Fe", 2000, 2025), ("Sonata", 1985, 2025), ("Tucson", 2004, 2025)],
    "Infiniti": [("Q50", 2013, 2025), ("Q60", 2016, 2025), ("QX50", 2018, 2025), ("QX60", 2013, 2025)],
    "Jaguar": [("F-Pace", 2015, 2025), ("F-Type", 2013, 2025), ("XE", 2015, 2025), ("XF", 2008, 2025)],
    "Jeep": [("Cherokee", 1974, 2025), ("Grand Cherokee", 1992, 2025), ("Wrangler", 1987, 2025)],
    "Kia": [("Forte", 2009, 2025), ("Niro", 2016, 2025), ("Seltos", 2019, 2025), ("Sorento", 2002, 2025), ("Sportage", 1995, 2025), ("Telluride", 2019, 2025), ("Sedona", 2001, 2025)],
    "Lamborghini": [("Aventador", 2011, 2025), ("Huracán", 2014, 2025), ("Urus", 2017, 2025)],
    "Land Rover": [("Discovery", 1989, 2025), ("Range Rover", 1970, 2025), ("Range Rover Evoque", 2011, 2025)],
    "Lexus": [("ES", 1989, 2025), ("IS", 1998, 2025), ("RX", 1998, 2025), ("NX", 2014, 2025)],
    "Lincoln": [("Navigator", 1997, 2025), ("MKZ", 2013, 2020)],
    "Lucid": [("Air", 2021, 2025)],
    "Maserati": [("Ghibli", 2013, 2025), ("Levante", 2016, 2025)],
    "Mazda": [("CX-5", 2012, 2025), ("Mazda3", 2003, 2025), ("Mazda6", 2002, 2025), ("MX-5 Miata", 1989, 2025)],
    "Mercedes-Benz": [("C-Class", 1993, 2025), ("E-Class", 1995, 2025), ("S-Class", 1954, 2025), ("GLC", 2015, 2025)],
    "Mini": [("Clubman", 2007, 2025), ("Hardtop", 2001, 2025)],
    "Mitsubishi": [("Outlander", 2002, 2025), ("Lancer", 1973, 2025)],
    "Nissan": [("Altima", 1992, 2025), ("Maxima", 1981, 2025), ("Rogue", 2006, 2025), ("Z", 1969, 2025)],
    "Polestar": [("2", 2019, 2025), ("3", 2023, 2025)],
    "Porsche": [("911", 1963, 2025), ("Cayenne", 2002, 2025), ("Macan", 2014, 2025)],
    "Ram": [("1500", 2002, 2025), ("2500", 2010, 2025)],
    "Rivian": [("R1S", 2021, 2025), ("R1T", 2021, 2025)],
    "Rolls-Royce": [("Ghost", 2009, 2025), ("Phantom", 2003, 2025)],
    "Subaru": [("Ascent", 2018, 2025), ("Crosstrek", 2012, 2025), ("Forester", 1997, 2025), ("Legacy", 1989, 2025), ("Outback", 1995, 2025)],
    "Suzuki": [("Swift", 2004, 2025), ("Vitara", 1988, 2025)],
    "Tata": [("Nexon", 2015, 2025), ("Harrier", 2019, 2025)],
    "Tesla": [("Model 3", 2017, 2025), ("Model S", 2012, 2025), ("Model X", 2015, 2025), ("Model Y", 2020, 2025)],
    "Toyota": [("Camry", 1983, 2025), ("Corolla", 1966, 2025), ("RAV4", 1995, 2025), ("Highlander", 2001, 2025), ("Prius", 1997, 2025), ("Sienna", 1997, 2025)],
    "Volkswagen": [("Golf", 1974, 2025), ("Passat", 1973, 2025), ("Tiguan", 2009, 2025)],
    "Volvo": [("S60", 2000, 2025), ("XC40", 2018, 2025), ("XC60", 2008, 2025), ("XC90", 2002, 2025)],
    "Xpeng": [("G9", 2021, 2025), ("P7", 2020, 2025)],
}

COMMON_TRIMS = ["Base", "Standard", "LE", "LX", "SE", "EX", "Limited", "Premium", "Sport", "Luxury", "XLE", "SL", "SV", "SX", "Touring", "GT"]

@app.get("/")
def root():
    return {"status": "ready"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes(year: str = None):
    if not year:
        year = "2024"
    try:
        year_int = int(year)
        makes = [make for make, (start, end) in MAKES_BY_YEAR.items() if start <= year_int <= end]
        return sorted(makes)
    except:
        return sorted(MAKES_BY_YEAR.keys())

@app.get("/api/cars/models")
def get_models(make: str, year: str = None):
    if not year:
        year = "2024"
    try:
        year_int = int(year)
        models_list = MODELS_DATABASE.get(make, [])
        available = [model for model, start, end in models_list if start <= year_int <= end]
        return sorted(available)
    except:
        models_list = MODELS_DATABASE.get(make, [])
        return sorted([model for model, _, _ in models_list])

@app.get("/api/cars/trims")
def get_trims(make: str, model: str, year: str = None):
    return COMMON_TRIMS

@app.get("/api/cars/colors")
def get_colors():
    return sorted(COLORS)

@app.get("/api/cars/decode-vin")
def decode_vin(vin: str):
    try:
        vin = vin.strip().upper() if vin else ""
        
        if len(vin) < 17:
            return {"error": "Invalid VIN - must be 17 characters"}
        
        # Try NHTSA API
        try:
            logger.info(f"Attempting to decode VIN: {vin}")
            url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
            response = requests.get(url, timeout=5)
            logger.info(f"NHTSA response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("Results", [])
                logger.info(f"NHTSA results: {results}")
                
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
                
                if decoded and "year" in decoded and "Make" in decoded and "model" in decoded:
                    logger.info(f"Successfully decoded: {decoded}")
                    return decoded
        except Exception as e:
            logger.error(f"NHTSA API error: {e}")
            pass
        
        return {"error": "VIN not found - please select Year, Make, Model manually"}
        
    except Exception as e:
        logger.error(f"VIN decode error: {e}")
        return {"error": str(e)}

@app.post("/api/leads/webhook/lead_received")
def lead_received(lead: LeadData):
    try:
        lead_id = f"LEAD_{lead.vin[:8] if lead.vin else 'NO_VIN'}"
        return {
            "success": True,
            "listing_id": lead_id,
            "ai_draft_offer": {"fair": 24500, "low": 22000, "max": 27000},
            "message": "Listing received successfully"
        }
    except Exception as e:
        return {"error": str(e)}