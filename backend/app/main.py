from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import requests

app = FastAPI(title="RevoMotors API")

# CORS Middleware - MUST be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comprehensive car database - 50+ makes, 300+ models
CAR_DATA = {
    "Acura": {"MDX": ["Standard", "Technology", "A-Spec"], "RDX": ["Standard", "Technology", "A-Spec"], "TLX": ["Standard", "Technology", "A-Spec"], "ILX": ["Standard", "Technology"], "NSX": ["Base"], "TSX": ["Base", "Tech"]},
    "Alfa Romeo": {"Giulia": ["Standard", "Ti", "Quadrifoglio"], "Stelvio": ["Standard", "Ti", "Quadrifoglio"], "4C": ["Base", "Spider"]},
    "Aston Martin": {"DB11": ["Base", "AMR"], "Vantage": ["Base", "AMR"], "Rapide": ["S"], "DBX": ["Base", "AMR"]},
    "Audi": {"A1": ["Standard", "Premium"], "A3": ["Standard", "Premium", "Prestige"], "A4": ["Standard", "Premium", "Prestige", "S4"], "A5": ["Standard", "Premium", "S5"], "A6": ["Premium", "Prestige", "S6"], "A7": ["Premium", "Prestige", "S7"], "A8": ["Standard", "Premium", "S8"], "Q2": ["Standard", "Premium"], "Q3": ["Standard", "Premium", "Prestige"], "Q4": ["Standard", "Premium"], "Q5": ["Premium", "Prestige", "SQ5"], "Q7": ["Premium", "Prestige", "SQ7"], "Q8": ["Premium", "Prestige", "SQ8"], "R8": ["Coupe", "Spyder"], "TT": ["Base", "S"], "RS5": ["Coupe", "Sportback"], "RS6": ["Avant"], "RS7": ["Sportback"]},
    "Bentley": {"Continental": ["GT", "Flying Spur"], "Mulsanne": ["Speed"], "Bentayga": ["Base", "Speed"]},
    "BMW": {"i3": ["Standard", "S"], "i8": ["Base", "Roadster"], "M3": ["Base", "Competition"], "M4": ["Base", "Competition"], "M440i": ["xDrive"], "1 Series": ["120i", "128i", "M135i"], "2 Series": ["220i", "228i", "M240i"], "3 Series": ["318i", "320i", "330i", "340i", "M340i", "M3"], "4 Series": ["430i", "440i", "M440i", "M4"], "5 Series": ["530i", "540i", "M550i", "M5"], "6 Series": ["640i", "650i", "M650i"], "7 Series": ["740i", "750i", "M760i"], "M550i": ["xDrive"], "X1": ["xDrive28i", "xDrive35i"], "X2": ["xDrive28i", "xDrive35i"], "X3": ["xDrive30i", "xDrive40i", "M40i", "M"], "X4": ["xDrive30i", "xDrive40i", "M40i"], "X5": ["xDrive40i", "xDrive50i", "M50i", "M"], "X6": ["xDrive40i", "xDrive50i", "M50i", "M"], "X7": ["xDrive40i", "xDrive50i", "M50i"]},
    "Bugatti": {"Chiron": ["Base", "Speed", "Bolide"], "Veyron": ["Base", "Super Sport"]},
    "Buick": {"Regal": ["Base", "Preferred", "GS"], "LaCrosse": ["Base", "Preferred", "Avenir"], "Envision": ["Preferred", "Essence", "Avenir"], "Encore": ["Preferred", "Essence", "Avenir"], "Enclave": ["Base", "Preferred", "Avenir"]},
    "Cadillac": {"CT4": ["Luxury", "Premium"], "CT5": ["Luxury", "Premium", "Platinum"], "CT6": ["Base", "Luxury"], "CTS": ["Luxury", "Premium", "Platinum"], "CTS-V": ["Base"], "Escalade": ["Luxury", "Premium", "Platinum"], "Escalade ESV": ["Base", "Luxury"], "SRX": ["Base", "Luxury", "Premium"], "XT4": ["Luxury", "Premium"], "XT5": ["Luxury", "Premium", "Platinum"], "XT6": ["Luxury", "Premium", "Platinum"]},
    "Chevrolet": {"Blazer": ["L", "LT", "RS", "Premier"], "Bolt": ["LT", "Premier"], "Camaro": ["LT", "RS", "SS", "ZL1"], "Colorado": ["Base", "LT", "Z71"], "Corvette": ["Stingray", "Z06", "ZR2"], "Cruze": ["L", "LT", "RS", "Premier"], "Equinox": ["L", "LT", "RS", "LTZ"], "Impala": ["LS", "LT", "Premier"], "Malibu": ["L", "LT", "RS", "Premier"], "Silverado": ["RST", "LTZ", "High Country"], "Sonic": ["LS", "LT", "Premier"], "Spark": ["LS", "LT", "Premier"], "Suburban": ["LS", "LT", "RST", "Premier"], "Tahoe": ["LS", "LT", "RST", "High Country"], "Traverse": ["LS", "LT", "RS", "Premier"], "Trax": ["LS", "LT", "Premier"], "Volt": ["LT", "Premier"]},
    "Chrysler": {"300": ["Base", "Limited", "C"], "Pacifica": ["Touring", "Limited", "Pinnacle"], "Sebring": ["Base", "Limited"], "Town Country": ["Base", "Touring"]},
    "Citroen": {"C1": ["Base", "Feel"], "C3": ["Base", "Feel", "Shine"], "C4": ["Live", "Shine", "Exclusive"], "C5": ["Base", "Live", "Shine"]},
    "Dodge": {"Charger": ["SE", "SXT", "R/T", "SRT", "Hellcat"], "Challenger": ["SXT", "R/T", "SRT", "Hellcat"], "Dart": ["SE", "SXT", "Rallye"], "Durango": ["SXT", "R/T", "Citadel", "SRT"], "Journey": ["SE", "SXT", "R/T"], "Viper": ["Base", "ACR"]},
    "Ferrari": {"F8 Tributo": ["Base"], "F430": ["Base", "Scuderia"], "F458": ["Italia", "Spider"], "FF": ["Base"], "GTC4": ["Lusso"], "LaFerrari": ["Base"], "Portofino": ["Base"], "SF90": ["Stradale"]},
    "Fiat": {"500": ["Pop", "Sport", "Lounge"], "500X": ["Pop", "Sport", "Lounge"], "500L": ["Pop", "Sport", "Lounge"], "124 Spider": ["Classica", "Lusso"]},
    "Ford": {"Edge": ["SE", "SEL", "Limited", "ST"], "Escape": ["S", "SE", "SEL", "Titanium", "ST"], "Explorer": ["Base", "XLT", "Limited", "ST", "Platinum"], "F-150": ["Regular", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat", "King Ranch", "Platinum"], "Fiesta": ["S", "SE", "SES", "Titanium"], "Flex": ["SE", "SEL", "Limited"], "Focus": ["S", "SE", "SEL", "ST", "RS"], "Fusion": ["S", "SE", "SEL", "Titanium"], "GT": ["Base"], "GT40": ["Base"], "Mustang": ["EcoBoost", "GT", "Mach 1", "Shelby"], "Pinto": ["Base"], "Ranger": ["Regular", "SuperCrew", "XL", "XLT"], "Taurus": ["SE", "Limited", "SHO"], "Thunderbird": ["Base"], "Taurus": ["Base", "Limited"]},
    "Genesis": {"G70": ["2.0T", "3.8"], "G80": ["2.0T", "3.8", "Electrified"], "G90": ["3.8", "5.0", "Electrified"], "GV70": ["2.5T", "3.8", "Electrified"], "GV80": ["2.5T", "3.8"], "Electrified GV70": ["Base"], "Electrified G80": ["Base"]},
    "GMC": {"Acadia": ["SL", "SLE", "Denali"], "Canyon": ["Base", "SLE", "Denali"], "Sierra": ["Regular", "Double Cab", "Crew Cab", "Denali"], "Terrain": ["SL", "SLE", "SLT"], "Yukon": ["SLE", "SLT", "Denali"], "Yukon XL": ["SLE", "SLT", "Denali"]},
    "Honda": {"Accord": ["LX", "Sport", "EX", "Touring", "Hybrid"], "Civic": ["LX", "Sport", "EX", "Touring", "Si", "Type R", "Hybrid"], "CR-V": ["LX", "EX", "EX-L", "Touring", "Hybrid"], "Fit": ["LX", "Sport", "EX"], "HR-V": ["LX", "EX", "EX-L"], "Insight": ["LX", "EX", "Touring"], "Odyssey": ["LX", "EX", "EX-L", "Touring"], "Passport": ["Sport", "EX-L", "Touring"], "Pilot": ["LX", "EX", "EX-L", "Touring", "Hybrid"], "Ridgeline": ["RT", "RTL", "RTL-E", "Black Edition"], "S2000": ["Base"]},
    "Hyundai": {"Accent": ["SE", "SEL", "Limited"], "Elantra": ["SE", "SEL", "Limited", "N"], "Genesis": ["3.8", "5.0"], "Ioniq": ["SE", "SEL", "Limited", "Hybrid", "Plug-in Hybrid", "Electric"], "Kona": ["SE", "SEL", "Limited", "Electric"], "Palisade": ["SE", "SEL", "Limited"], "Prius": ["L", "LE", "XLE"], "Santa Fe": ["SE", "SEL", "Limited", "Calligraphy"], "Sonata": ["SE", "SEL", "Limited", "N", "Hybrid"], "Tiburon": ["Base", "SE", "Limited"], "Tucson": ["SE", "SEL", "Limited", "N Line"], "Venue": ["SE", "SEL", "Limited"]},
    "Infiniti": {"Q30": ["Base", "Premium"], "Q50": ["Pure", "Luxe", "Red Sport", "Eau Rouge"], "Q60": ["Pure", "Luxe", "Red Sport"], "Q70": ["Base", "Premium", "Signature"], "Q80": ["Base", "Signature", "Premium"], "QX30": ["Base", "Premium"], "QX50": ["Pure", "Luxe", "Essential"], "QX60": ["Base", "Luxury"], "QX80": ["Base", "Luxury", "Platinum"], "QX90": ["Base", "Luxury"]},
    "Jaguar": {"F-Pace": ["Base", "Premium", "R-Sport", "SVR"], "F-Type": ["Base", "R", "SVR"], "I-Pace": ["Base", "SE", "HSE"], "XE": ["Base", "Premium", "R-Sport", "SVR"], "XF": ["Base", "Premium", "R-Sport", "SVR"], "XJ": ["Base", "Premium", "Supersport"]},
    "Jeep": {"Cherokee": ["Sport", "Latitude", "Trailhawk", "High Altitude"], "Compass": ["Sport", "Latitude", "Limited", "Trailhawk"], "Gladiator": ["Sport", "Overland", "Rubicon"], "Grand Cherokee": ["Laredo", "Limited", "Trailhawk", "Summit", "High Altitude"], "Renegade": ["Sport", "Latitude", "Limited", "Trailhawk"], "Wrangler": ["Sport", "Sahara", "Rubicon", "Unlimited"]},
    "Kia": {"Forte": ["FE", "LX", "S", "EX", "GT"], "K5": ["LX", "EX", "SX"], "Niro": ["LX", "EX", "SX", "Hybrid", "Plug-in Hybrid"], "Optima": ["LX", "EX", "SX"], "Rio": ["FE", "LX", "S", "EX"], "Seltos": ["LX", "EX", "SX"], "Sorento": ["L", "LX", "EX", "SX"], "Sportage": ["LX", "S", "EX", "SX"], "Stinger": ["Base", "GT", "GT2"], "Telluride": ["LX", "EX", "SX", "Limited"]},
    "Koenigsegg": {"Agera": ["Base", "RS", "RR"], "Gemera": ["Base"], "Jesko": ["Base", "Attack"]},
    "Lamborghini": {"Aventador": ["Base", "S", "SV", "SVJ"], "Huracán": ["Base", "Performante", "Sterrato"], "Murciélago": ["Base", "LP640"], "Revuelto": ["Base"], "Urus": ["Base", "S", "Performante"]},
    "Lancia": {"Delta": ["Base", "HF"], "Ypsilon": ["Base", "Gold"], "Thema": ["Base", "Platino"]},
    "Land Rover": {"Discovery": ["SE", "HSE", "Landmark"], "Discovery Sport": ["SE", "HSE", "R-Dynamic"], "Range Rover": ["Base", "Sport", "Vogue"], "Range Rover Evoque": ["Base", "HSE", "R-Dynamic"], "Range Rover Sport": ["SE", "HSE", "SVR"], "Range Rover Velar": ["Base", "HSE", "R-Dynamic"]},
    "Lexus": {"CT": ["200h", "200h F Sport"], "ES": ["250", "350", "Hybrid", "F"], "GS": ["350", "Hybrid", "F"], "GX": ["460", "550", "Luxury"], "IS": ["300", "350", "F", "Hybrid"], "LC": ["500", "Hybrid"], "LS": ["500", "Hybrid", "F"], "LX": ["570", "Hybrid"], "NX": ["250", "350", "Hybrid", "F Sport"], "RC": ["300", "350", "F"], "RX": ["350", "Hybrid", "L", "Plug-in Hybrid"], "UX": ["200", "250h", "Hybrid"]},
    "Lincoln": {"Aviator": ["Premiere", "Select", "Reserve", "Black Label"], "Corsair": ["Premiere", "Select", "Reserve"], "MKZ": ["Premiere", "Select", "Reserve", "Black Label"], "MKX": ["Premiere", "Select", "Reserve"], "Navigator": ["Premiere", "Select", "Reserve", "Black Label"], "Town Car": ["Base", "Signature"]},
    "Lucid": {"Air": ["Pure", "Touring", "Grand Touring", "Sapphire"]},
    "Maserati": {"Ghibli": ["Base", "S", "Trofeo"], "Levante": ["Base", "S", "Trofeo"], "Quattroporte": ["Base", "S", "Trofeo"], "MC20": ["Base"]},
    "Mazda": {"CX-3": ["Sport", "Touring", "Grand Touring"], "CX-30": ["Base", "Select", "Preferred"], "CX-50": ["Base", "Select", "Preferred"], "CX-5": ["Base", "Select", "Preferred", "Premium"], "CX-9": ["Base", "Select", "Preferred", "Premium"], "Mazda2": ["Sport", "Select", "Preferred"], "Mazda3": ["Base", "Select", "Preferred", "Premium"], "Mazda6": ["Base", "Select", "Preferred", "Premium"], "MX-5 Miata": ["Sport", "Club", "Grand Touring"], "MX-30": ["Base", "Select"]},
    "McLaren": {"570GT": ["Base"], "570S": ["Base"], "650S": ["Base"], "720S": ["Base", "Performance"], "765LT": ["Base"], "GT": ["Base"]},
    "Mercedes-Benz": {"A-Class": ["A220", "A250", "AMG A35"], "AMG C63": ["Base"], "AMG G63": ["Base"], "AMG GT": ["Base", "R", "Black Series"], "B-Class": ["B250", "AMG B35"], "C-Class": ["C300", "C43 AMG", "C63 AMG"], "CLA": ["Base", "250", "AMG"], "CLS": ["450", "AMG 53"], "E-Class": ["E350", "E450", "E53 AMG", "E63 AMG"], "EQC": ["Base", "AMG"], "EQE": ["Base", "AMG"], "EQS": ["Base", "AMG"], "G-Class": ["G550", "AMG G63", "AMG G63 AMG"], "GLA": ["GLA250", "AMG GLA35"], "GLB": ["GLB250", "AMG GLB35"], "GLC": ["GLC300", "GLC43 AMG", "GLC63 AMG"], "GLE": ["GLE350", "GLE450", "AMG GLE53"], "GLK": ["Base"], "GLS": ["GLS450", "AMG GLS53"], "S-Class": ["S500", "S580", "AMG S63"], "SL": ["Base", "AMG"]},
    "Mini": {"Clubman": ["Base", "Cooper", "Cooper S"], "Countryman": ["Base", "Cooper", "Cooper S"], "Hardtop": ["Base", "Cooper", "Cooper S"], "Paceman": ["Base", "Cooper"], "Roadster": ["Base", "Cooper"]},
    "Mitsubishi": {"Diamante": ["Base"], "Eclipse": ["Base", "Cross"], "Galant": ["Base"], "Lancer": ["ES", "SEL", "Ralliart"], "Mirage": ["Base", "ES", "SEL"], "Outlander": ["ES", "SEL", "Limited", "Hybrid"], "Pajero": ["Base", "Exceed"], "i-MiEV": ["Base", "SE"]},
    "Nissan": {"Altima": ["S", "SV", "SL", "Platinum"], "Ariya": ["Base", "Plus", "Pro"], "Frontier": ["S", "SV", "SL"], "GT-R": ["Base", "Premium", "Track Edition"], "Leaf": ["S", "SV", "SL", "Plus"], "Maxima": ["S", "SV", "SL", "Platinum"], "Murano": ["S", "SV", "SL", "Platinum", "Hybrid"], "Pathfinder": ["S", "SV", "SL", "Platinum"], "Qashqai": ["Base", "SV", "SL"], "Rogue": ["S", "SV", "SL", "Platinum"], "Sentra": ["S", "SV", "SR", "SL"], "Titan": ["Single Cab", "Crew Cab", "XD"], "Versa": ["S", "SV", "SR", "SL"], "Z": ["Base", "Performance"]},
    "Peugeot": {"108": ["Active", "Allure"], "208": ["Active", "Allure", "GT"], "308": ["Active", "Allure", "GT"], "3008": ["Active", "Allure", "GT"], "5008": ["Active", "Allure", "GT"], "Expert": ["Base"], "Partner": ["Base"]},
    "Polestar": {"1": ["Base"], "2": ["Standard Range", "Long Range", "Performance"], "3": ["Base"], "4": ["Base"]},
    "Porsche": {"718 Boxster": ["Base", "S", "GTS"], "718 Cayman": ["Base", "S", "GTS"], "911": ["Carrera", "Carrera 4", "Turbo", "GT"], "Panamera": ["Base", "4", "Turbo"], "Cayenne": ["Base", "S", "Turbo", "E-Hybrid"], "Macan": ["Base", "S", "Turbo"], "Taycan": ["Base", "4", "Turbo", "Cross Turismo"]},
    "Ram": {"1500": ["Tradesman", "SLT", "Laramie", "Rebel", "Tungsten"], "2500": ["Tradesman", "Power Wagon", "Laramie", "Mega Cab"], "3500": ["Tradesman", "SLT", "Laramie"], "Promaster": ["City", "Cargo", "Window"]},
    "Renault": {"Clio": ["Base", "Interactive"], "Espace": ["Base", "Dynamique"], "Kangoo": ["Base", "Sport"], "Laguna": ["Base", "Dynamique"], "Megane": ["Base", "Dynamique"], "Scenic": ["Base", "Dynamique"], "Zoe": ["Base", "Dynamique"]},
    "Rivian": {"R1S": ["Dual Motor", "Quad Motor", "Tri Motor"], "R1T": ["Dual Motor", "Quad Motor", "Tri Motor"]},
    "Rolls-Royce": {"Cullinan": ["Base", "Black Badge"], "Ghost": ["Base", "Black Badge"], "Phantom": ["Base", "Black Badge"], "Wraith": ["Base", "Black Badge"]},
    "Saab": {"9-3": ["Base", "Sport"], "9-5": ["Base", "Aero"], "9000": ["Base"]},
    "Subaru": {"Ascent": ["Base", "Premium", "Limited"], "BRZ": ["Base", "Premium", "Limited"], "Crosstrek": ["Base", "Premium", "Limited"], "Forester": ["Base", "Premium", "Limited"], "Impreza": ["Base", "Sport", "Limited"], "Legacy": ["Base", "Premium", "Limited"], "Outback": ["Base", "Premium", "Limited"], "SVX": ["Base"], "WRX": ["Base", "STI", "Limited"]},
    "Suzuki": {"Alto": ["Base", "GL", "GLX"], "Celerio": ["Base", "VXi"], "Ciaz": ["Base", "VXi"], "Ertiga": ["Base", "VXi"], "Grand Vitara": ["Base", "SZ5"], "Maruti": ["800"], "S-Cross": ["Base", "ZXi"], "Swift": ["Base", "VXi", "ZXi"], "SX4": ["Base", "Hybrid"], "Vitara": ["Base", "SZ5", "AllGrip"]},
    "Tata": {"Altroz": ["Base", "XT"], "Altroz iCNG": ["Base"], "Harrier": ["XE", "XM"], "Hexa": ["XE", "XM"], "Nexon": ["XE", "XM", "EV"], "Punch": ["Base", "AMT"], "Tiago": ["Base", "XT"], "Tigor": ["Base", "XT"]},
    "Tesla": {"Model 3": ["Standard Range", "Long Range", "Performance"], "Model S": ["Long Range", "Performance", "Plaid"], "Model X": ["Long Range", "Performance", "Plaid"], "Model Y": ["RWD", "Long Range", "Performance"], "Roadster": ["Base"], "Cybertruck": ["Base", "AWD", "Tri Motor"]},
    "Toyota": {"4Runner": ["SR5", "TRD", "TRD Pro", "Limited"], "Avalon": ["LE", "XLE", "Limited", "Hybrid"], "bZ4X": ["Base", "Limited"], "Camry": ["LE", "SE", "XLE", "TRD", "Hybrid"], "Corolla": ["L", "LE", "SE", "XLE", "Hybrid"], "GR Supra": ["2.0", "3.0"], "GR Yaris": ["Base"], "GR Corolla": ["Base"], "GR86": ["Base", "Premium"], "Gross Countach": ["Base"], "Highlander": ["L", "LE", "XLE", "Limited", "Platinum"], "Mirai": ["LE", "XLE", "Limited"], "Prius": ["L", "LE", "XLE", "AWD-E", "Hybrid"], "Prius Prime": ["LE", "XLE"], "RAV4": ["LE", "XLE", "Adventure", "TRD", "Prime"], "Sequoia": ["SR5", "Limited", "Platinum"], "Sienna": ["LE", "XLE", "Limited"], "Tacoma": ["SR", "SR5", "TRD", "Limited"], "Tundra": ["SR", "SR5", "Limited", "Platinum"], "Venza": ["LE", "XLE", "Limited", "Hybrid"]},
    "Volkswagen": {"Arteon": ["S", "SE", "SEL"], "Atlas": ["S", "SE", "SEL", "R-Line"], "Atlas Cross Sport": ["S", "SE", "SEL", "R-Line"], "Beetle": ["S", "SE", "SEL", "Final Edition"], "Golf": ["S", "SE", "SEL", "GTI", "R"], "Golf Alltrack": ["Base", "S", "SE"], "ID.4": ["Standard", "Pro", "Pro Max", "1st Edition"], "ID.5": ["Standard", "Pro", "Pro Max"], "ID.Buzz": ["Base", "Pro", "Pro S"], "Jetta": ["S", "SE", "SEL", "GLI"], "Passat": ["S", "SE", "SEL", "GLI"], "Rabbit": ["S", "SE"], "Taos": ["S", "SE", "SEL"], "Tiguan": ["S", "SE", "SEL", "R-Line"], "Touareg": ["Standard", "Execline"]},
    "Volvo": {"C30": ["Base", "T5"], "C70": ["Base", "T5"], "S60": ["Momentum", "Inscription", "R-Design"], "S80": ["Base", "T6"], "S90": ["Momentum", "Inscription", "R-Design"], "V60": ["Momentum", "Inscription", "R-Design"], "V90": ["Momentum", "Inscription", "R-Design"], "XC40": ["Base", "Recharge", "R-Design"], "XC60": ["Momentum", "Inscription", "R-Design"], "XC90": ["Momentum", "Inscription", "R-Design"]},
    "Xpeng": {"G9": ["Base", "Plus", "Max"], "P7": ["Base", "Plus", "Max"], "P8": ["Base", "Plus", "Max"]},
}

@app.get("/")
def root():
    return {"status": "ready", "service": "RevoMotors API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes():
    """Get all car makes"""
    try:
        makes = sorted(list(CAR_DATA.keys()))
        return makes
    except Exception as e:
        logger.error(f"Error in get_makes: {e}")
        return {"error": str(e)}

@app.get("/api/cars/models")
def get_models(make: str):
    """Get models for a specific make"""
    try:
        if make not in CAR_DATA:
            return []
        models = sorted(list(CAR_DATA[make].keys()))
        return models
    except Exception as e:
        logger.error(f"Error in get_models: {e}")
        return {"error": str(e)}

@app.get("/api/cars/trims")
def get_trims(make: str, model: str):
    """Get trims for a specific model"""
    try:
        if make not in CAR_DATA or model not in CAR_DATA[make]:
            return []
        trims = CAR_DATA[make][model]
        return sorted(trims)
    except Exception as e:
        logger.error(f"Error in get_trims: {e}")
        return {"error": str(e)}

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
            logger.error(f"NHTSA API returned status {response.status_code}")
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
    except requests.exceptions.ConnectionError as e:
        logger.error(f"VIN decode connection error: {e}")
        return {"error": "Failed to connect to VIN decoder service"}
    except Exception as e:
        logger.error(f"VIN decode error: {e}")
        return {"error": "Failed to decode VIN"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)