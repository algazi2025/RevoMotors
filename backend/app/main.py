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

COLORS = ["Pearl White", "Black", "Silver", "Gray", "White", "Red", "Blue", "Brown", "Gold", "Green", "Orange", "Yellow", "Beige", "Charcoal", "Midnight Blue", "Burgundy", "Tan", "Ivory", "Navy", "Slate"]

CAR_DATABASE = {
    "Acura": {
        "ILX": {"trims": ["Standard", "Technology", "A-Spec"], "engines": ["2.0L 4-Cyl", "2.4L Turbo"]},
        "MDX": {"trims": ["Standard", "Technology", "A-Spec", "Advance"], "engines": ["3.5L V6", "3.0L Turbo"]},
        "RDX": {"trims": ["Standard", "Technology", "A-Spec", "Advance"], "engines": ["2.0L Turbo", "3.5L V6"]},
        "TLX": {"trims": ["Standard", "Technology", "A-Spec", "PMC"], "engines": ["2.4L Turbo", "3.5L V6"]},
        "NSX": {"trims": ["Base", "Type-R"], "engines": ["3.5L Twin-Turbo Hybrid"]}
    },
    "Alfa Romeo": {
        "Giulia": {"trims": ["Standard", "Ti", "Quadrifoglio"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "Stelvio": {"trims": ["Standard", "Ti", "Quadrifoglio"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "4C": {"trims": ["Base", "Spider"], "engines": ["1.7L Turbo"]}
    },
    "Aston Martin": {
        "DB11": {"trims": ["Base", "AMR"], "engines": ["5.2L Twin-Turbo V12", "5.2L Twin-Turbo"]},
        "Vantage": {"trims": ["Base", "AMR"], "engines": ["4.0L Twin-Turbo V8"]},
        "Rapide": {"trims": ["S"], "engines": ["5.9L V12"]},
        "DBX": {"trims": ["Base", "AMR"], "engines": ["4.0L Twin-Turbo"]}
    },
    "Audi": {
        "A3": {"trims": ["Standard", "Premium", "Premium Plus", "Prestige"], "engines": ["2.0L Turbo 4-Cyl"]},
        "A4": {"trims": ["Standard", "Premium", "Premium Plus", "Prestige", "S4"], "engines": ["2.0L Turbo", "3.0L TFSI", "2.9L Twin-Turbo"]},
        "A6": {"trims": ["Premium", "Premium Plus", "Prestige", "S6"], "engines": ["3.0L TFSI", "2.9L Twin-Turbo"]},
        "Q3": {"trims": ["Standard", "Premium", "Premium Plus", "Prestige"], "engines": ["2.0L Turbo", "2.5L TFSI"]},
        "Q5": {"trims": ["Premium", "Premium Plus", "Prestige", "SQ5"], "engines": ["2.0L Turbo", "3.0L TFSI", "2.9L Twin-Turbo"]},
        "Q7": {"trims": ["Premium", "Premium Plus", "Prestige", "SQ7"], "engines": ["3.0L TFSI", "2.9L Twin-Turbo"]},
        "A8": {"trims": ["Standard", "Premium", "Prestige"], "engines": ["3.0L TFSI", "4.0L Twin-Turbo"]}
    },
    "Bentley": {
        "Continental": {"trims": ["GT", "Flying Spur"], "engines": ["6.0L Twin-Turbo W12"]},
        "Mulsanne": {"trims": ["Speed"], "engines": ["6.75L Twin-Turbo V8"]},
        "Bentayga": {"trims": ["Base", "Speed"], "engines": ["6.0L Twin-Turbo W12", "4.0L Twin-Turbo V8"]}
    },
    "BMW": {
        "3 Series": {"trims": ["320i", "330i", "340i", "M340i", "M3"], "engines": ["2.0L Turbo", "3.0L Turbo", "3.0L Twin-Turbo"]},
        "5 Series": {"trims": ["530i", "540i", "M550i", "M5"], "engines": ["2.0L Turbo", "3.0L Turbo", "4.4L Twin-Turbo"]},
        "7 Series": {"trims": ["740i", "750i", "M760i"], "engines": ["3.0L Turbo", "4.4L Twin-Turbo"]},
        "X1": {"trims": ["sDrive28i", "xDrive28i", "xDrive35i"], "engines": ["2.0L Turbo", "3.0L Turbo"]},
        "X3": {"trims": ["sDrive30i", "xDrive30i", "xDrive40i", "M40i", "M"], "engines": ["2.0L Turbo", "3.0L Turbo"]},
        "X5": {"trims": ["xDrive40i", "xDrive50i", "M50i", "M"], "engines": ["3.0L Turbo", "4.4L Twin-Turbo"]},
        "X7": {"trims": ["xDrive40i", "xDrive50i", "M50i"], "engines": ["3.0L Turbo", "4.4L Twin-Turbo"]}
    },
    "Bugatti": {
        "Chiron": {"trims": ["Base", "Speed", "Super Sport"], "engines": ["8.0L Quad-Turbo W16"]},
        "Veyron": {"trims": ["Base", "Super Sport"], "engines": ["8.0L Quad-Turbo W16"]}
    },
    "Buick": {
        "Regal": {"trims": ["Base", "Preferred", "GS"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "LaCrosse": {"trims": ["Base", "Preferred", "Avenir"], "engines": ["3.5L V6", "3.6L V6"]},
        "Envision": {"trims": ["Preferred", "Essence", "Avenir"], "engines": ["2.0L Turbo", "2.5L 4-Cyl"]},
        "Encore": {"trims": ["Preferred", "Essence", "Avenir"], "engines": ["1.4L Turbo", "1.5L 4-Cyl"]},
        "Enclave": {"trims": ["Base", "Preferred", "Avenir"], "engines": ["3.6L V6"]}
    },
    "Cadillac": {
        "CT4": {"trims": ["Luxury", "Premium", "Sport"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "CT5": {"trims": ["Luxury", "Premium", "Platinum", "Sport"], "engines": ["2.0L Turbo", "3.6L V6", "3.0L Turbo"]},
        "CT6": {"trims": ["Base", "Luxury", "Premium"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "Escalade": {"trims": ["Luxury", "Premium", "Platinum"], "engines": ["5.3L V8", "6.2L V8"]},
        "XT4": {"trims": ["Luxury", "Premium"], "engines": ["2.0L Turbo", "2.5L 4-Cyl"]},
        "XT5": {"trims": ["Luxury", "Premium", "Platinum"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "XT6": {"trims": ["Luxury", "Premium", "Platinum"], "engines": ["3.6L V6"]}
    },
    "Chevrolet": {
        "Blazer": {"trims": ["L", "LT", "RS", "Premier"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "Camaro": {"trims": ["LT", "RS", "SS", "ZL1"], "engines": ["2.0L Turbo", "3.6L V6", "6.2L V8", "6.2L Supercharged V8"]},
        "Colorado": {"trims": ["Base", "LT", "Z71", "ZR2"], "engines": ["2.5L 4-Cyl", "3.6L V6", "2.7L Turbo"]},
        "Corvette": {"trims": ["Stingray", "Z06", "ZR2"], "engines": ["5.2L V8", "5.5L V8", "5.5L Twin-Turbo"]},
        "Cruze": {"trims": ["L", "LT", "RS", "Premier"], "engines": ["1.4L Turbo", "1.5L Turbo"]},
        "Equinox": {"trims": ["L", "LT", "RS", "LTZ"], "engines": ["1.5L Turbo", "2.0L Turbo"]},
        "Malibu": {"trims": ["L", "LT", "RS", "Premier"], "engines": ["1.5L Turbo", "2.0L Turbo"]},
        "Silverado 1500": {"trims": ["RST", "LTZ", "High Country", "Duramax"], "engines": ["5.3L V8", "6.2L V8", "3.0L Turbo Diesel"]},
        "Traverse": {"trims": ["LS", "LT", "RS", "Premier"], "engines": ["3.6L V6"]},
        "Tahoe": {"trims": ["LS", "LT", "RST", "High Country"], "engines": ["5.3L V8", "6.2L V8", "3.0L Turbo Diesel"]}
    },
    "Chrysler": {
        "300": {"trims": ["Base", "Limited", "C"], "engines": ["3.6L V6", "5.7L V8"]},
        "Pacifica": {"trims": ["Touring", "Limited", "Pinnacle"], "engines": ["3.6L V6"]},
        "Prowler": {"trims": ["Base"], "engines": ["3.5L V6"]}
    },
    "Citroen": {
        "C3": {"trims": ["Base", "Feel", "Shine"], "engines": ["1.2L Turbo", "1.5L Diesel"]},
        "C4": {"trims": ["Live", "Shine", "Exclusive"], "engines": ["1.2L Turbo", "1.5L Diesel"]},
        "C5": {"trims": ["Base", "Live", "Shine"], "engines": ["1.6L Turbo", "2.0L Diesel"]}
    },
    "Dodge": {
        "Charger": {"trims": ["SE", "SXT", "R/T", "SRT", "Hellcat"], "engines": ["3.6L V6", "5.7L V8", "6.4L V8", "6.2L Supercharged"]},
        "Challenger": {"trims": ["SXT", "R/T", "SRT", "Hellcat", "Demon"], "engines": ["3.6L V6", "5.7L V8", "6.4L V8", "6.2L Supercharged"]},
        "Durango": {"trims": ["SXT", "R/T", "Citadel", "SRT"], "engines": ["3.6L V6", "5.7L V8", "6.4L V8"]},
        "Journey": {"trims": ["SE", "SXT", "R/T"], "engines": ["2.4L 4-Cyl", "3.6L V6"]}
    },
    "Ferrari": {
        "F8 Tributo": {"trims": ["Base"], "engines": ["3.9L Twin-Turbo V8"]},
        "F430": {"trims": ["Base", "Scuderia"], "engines": ["4.3L V8"]},
        "F458": {"trims": ["Italia", "Spider"], "engines": ["4.5L V8"]},
        "FF": {"trims": ["Base"], "engines": ["6.3L V12"]},
        "Portofino": {"trims": ["Base"], "engines": ["3.9L Twin-Turbo V8"]}
    },
    "Fiat": {
        "500": {"trims": ["Pop", "Sport", "Lounge"], "engines": ["1.2L 4-Cyl", "0.9L Turbo"]},
        "500X": {"trims": ["Pop", "Sport", "Lounge"], "engines": ["1.4L Turbo", "1.6L Diesel"]},
        "500L": {"trims": ["Pop", "Sport", "Lounge"], "engines": ["1.4L Turbo", "1.3L Turbo Diesel"]}
    },
    "Ford": {
        "Edge": {"trims": ["SE", "SEL", "Limited", "ST"], "engines": ["2.0L Turbo", "2.7L Turbo"]},
        "Escape": {"trims": ["S", "SE", "SEL", "Titanium", "ST"], "engines": ["1.5L Turbo", "2.0L Turbo", "1.6L Turbo Diesel"]},
        "Explorer": {"trims": ["Base", "XLT", "Limited", "ST", "Platinum"], "engines": ["2.3L Turbo", "3.0L Turbo", "3.3L V6"]},
        "F-150": {"trims": ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat", "King Ranch", "Platinum"], "engines": ["3.3L V6", "5.0L V8", "3.5L EcoBoost", "2.7L EcoBoost", "3.0L EcoBoost Turbo Diesel"]},
        "Mustang": {"trims": ["EcoBoost", "GT", "Mach 1", "Shelby GT500", "Dark Horse"], "engines": ["2.3L EcoBoost", "5.0L V8", "5.2L V8"]},
        "Ranger": {"trims": ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat"], "engines": ["2.3L Turbo", "3.0L Power Stroke Diesel", "2.7L Turbo"]},
        "Bronco": {"trims": ["Base", "Big Bend", "Black Diamond", "Outer Banks", "Wildtrak"], "engines": ["2.3L Turbo", "3.0L Turbo"]}
    },
    "Genesis": {
        "G70": {"trims": ["2.0T", "3.8", "G70 2.0T"], "engines": ["2.0L Twin-Turbo", "3.8L V6"]},
        "G80": {"trims": ["2.0T", "3.8", "Electrified"], "engines": ["2.0L Twin-Turbo", "3.8L V6", "Electric"]},
        "G90": {"trims": ["3.8", "5.0", "Electrified"], "engines": ["3.8L V6", "5.0L V8", "Electric"]},
        "GV70": {"trims": ["2.5T", "3.8", "Electrified"], "engines": ["2.5L Turbo", "3.8L V6", "Electric"]},
        "GV80": {"trims": ["2.5T", "3.8"], "engines": ["2.5L Turbo", "3.8L V6"]}
    },
    "GMC": {
        "Acadia": {"trims": ["SL", "SLE", "Denali", "AT4"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "Canyon": {"trims": ["Base", "SLE", "Denali", "AT4"], "engines": ["2.5L 4-Cyl", "3.6L V6", "2.8L Duramax Diesel"]},
        "Sierra 1500": {"trims": ["Regular", "Double Cab", "Crew Cab", "Denali", "AT4"], "engines": ["5.3L V8", "6.2L V8", "3.0L Turbo Diesel"]},
        "Terrain": {"trims": ["SL", "SLE", "SLT", "Denali"], "engines": ["1.5L Turbo", "2.0L Turbo"]},
        "Yukon": {"trims": ["SLE", "SLT", "Denali", "AT4"], "engines": ["5.3L V8", "6.2L V8", "3.0L Turbo Diesel"]},
        "Yukon XL": {"trims": ["SLE", "SLT", "Denali"], "engines": ["5.3L V8", "6.2L V8"]}
    },
    "Honda": {
        "Accord": {"trims": ["LX", "Sport", "EX", "EX-L", "Touring", "Hybrid"], "engines": ["1.5L Turbo", "2.0L Turbo", "2.0L Hybrid"]},
        "Civic": {"trims": ["LX", "Sport", "EX", "EX-T", "Touring", "Si", "Type R", "Hybrid"], "engines": ["2.0L 4-Cyl", "1.5L Turbo", "2.0L Turbo", "2.0L Hybrid"]},
        "CR-V": {"trims": ["LX", "EX", "EX-L", "Touring", "Hybrid"], "engines": ["1.5L Turbo", "2.0L Turbo", "2.0L Hybrid"]},
        "Odyssey": {"trims": ["LX", "EX", "EX-L", "Touring", "Elite"], "engines": ["3.5L V6"]},
        "Pilot": {"trims": ["LX", "EX", "EX-L", "Touring", "Elite", "Hybrid"], "engines": ["3.5L V6", "3.5L Hybrid"]},
        "Ridgeline": {"trims": ["RT", "RTL", "RTL-E", "Black Edition"], "engines": ["3.5L V6"]},
        "Fit": {"trims": ["LX", "Sport", "EX"], "engines": ["1.5L 4-Cyl"]},
        "Insight": {"trims": ["LX", "EX", "Touring"], "engines": ["1.5L Hybrid"]}
    },
    "Hyundai": {
        "Accent": {"trims": ["SE", "SEL", "Limited"], "engines": ["1.6L 4-Cyl", "1.5L Turbo"]},
        "Elantra": {"trims": ["SE", "SEL", "Limited", "N", "Hybrid"], "engines": ["2.0L 4-Cyl", "1.6L Turbo", "1.8L Hybrid"]},
        "Ioniq": {"trims": ["SE", "SEL", "Limited", "Hybrid", "Plug-in Hybrid", "Electric"], "engines": ["1.6L Hybrid", "1.6L Plug-in Hybrid", "Electric Motor"]},
        "Kona": {"trims": ["SE", "SEL", "Limited", "N Line", "Electric"], "engines": ["2.0L 4-Cyl", "1.6L Turbo", "Electric Motor"]},
        "Palisade": {"trims": ["SE", "SEL", "Limited", "Calligraphy"], "engines": ["2.2L Diesel", "3.8L V6"]},
        "Santa Fe": {"trims": ["SE", "SEL", "Limited", "Calligraphy"], "engines": ["2.5L 4-Cyl", "2.2L Diesel", "2.5L Turbo"]},
        "Sonata": {"trims": ["SE", "SEL", "Limited", "N Line", "Hybrid", "Plug-in Hybrid"], "engines": ["2.5L 4-Cyl", "2.0L Turbo", "2.0L Hybrid", "2.0L Plug-in Hybrid"]},
        "Tucson": {"trims": ["SE", "SEL", "Limited", "N Line"], "engines": ["2.0L 4-Cyl", "1.6L Turbo", "2.5L Turbo"]},
        "Venue": {"trims": ["SE", "SEL", "Limited"], "engines": ["1.6L 4-Cyl"]}
    },
    "Infiniti": {
        "Q30": {"trims": ["Base", "Premium"], "engines": ["2.0L Turbo", "2.2L Diesel"]},
        "Q50": {"trims": ["Pure", "Luxe", "Red Sport", "Eau Rouge"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo", "3.7L V6"]},
        "Q60": {"trims": ["Pure", "Luxe", "Red Sport"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "Q70": {"trims": ["Base", "Premium", "Signature"], "engines": ["3.5L V6", "3.7L V6"]},
        "QX50": {"trims": ["Pure", "Luxe", "Essential"], "engines": ["2.0L Turbo", "3.7L V6"]},
        "QX60": {"trims": ["Base", "Luxury"], "engines": ["3.5L V6"]},
        "QX80": {"trims": ["Base", "Luxury", "Platinum"], "engines": ["5.6L V8"]}
    },
    "Jaguar": {
        "F-Pace": {"trims": ["Base", "Premium", "R-Sport", "SVR"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "F-Type": {"trims": ["Base", "R", "SVR"], "engines": ["2.0L Turbo", "3.0L Supercharged", "5.0L Supercharged"]},
        "I-Pace": {"trims": ["Base", "SE", "HSE"], "engines": ["Electric Motor"]},
        "XE": {"trims": ["Base", "Premium", "R-Sport", "SVR"], "engines": ["2.0L Turbo", "3.0L Supercharged"]},
        "XF": {"trims": ["Base", "Premium", "R-Sport", "SVR"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]}
    },
    "Jeep": {
        "Cherokee": {"trims": ["Sport", "Latitude", "Limited", "Trailhawk", "High Altitude"], "engines": ["2.0L Turbo", "3.2L V6", "3.5L V6"]},
        "Compass": {"trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "engines": ["2.0L Turbo", "1.6L Turbo Diesel"]},
        "Gladiator": {"trims": ["Sport", "Overland", "Rubicon", "Mojave"], "engines": ["3.6L V6", "2.0L Turbo Diesel"]},
        "Grand Cherokee": {"trims": ["Laredo", "Limited", "Limited X", "Trailhawk", "Summit", "High Altitude"], "engines": ["3.6L V6", "5.7L V8", "3.0L Turbo Diesel", "3.0L Twin-Turbo Diesel"]},
        "Renegade": {"trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "engines": ["1.3L Turbo", "1.4L Turbo", "1.6L Turbo Diesel"]},
        "Wrangler": {"trims": ["Sport", "Sahara", "Rubicon", "Unlimited", "Willys"], "engines": ["2.0L Turbo", "3.6L V6", "2.0L Turbo Diesel"]}
    },
    "Kia": {
        "Forte": {"trims": ["FE", "LX", "S", "EX", "GT"], "engines": ["2.0L 4-Cyl", "1.6L Turbo"]},
        "K5": {"trims": ["LX", "EX", "SX", "SX Prestige"], "engines": ["2.5L 4-Cyl", "2.0L Turbo", "3.3L Turbo"]},
        "Niro": {"trims": ["LX", "EX", "SX", "SX Prestige", "Hybrid", "Plug-in Hybrid"], "engines": ["2.0L 4-Cyl", "1.6L Turbo", "Hybrid 1.6L", "Plug-in Hybrid 1.6L"]},
        "Rio": {"trims": ["FE", "LX", "S", "EX"], "engines": ["1.6L 4-Cyl"]},
        "Seltos": {"trims": ["LX", "EX", "SX"], "engines": ["2.0L 4-Cyl"]},
        "Sorento": {"trims": ["L", "LX", "EX", "SX", "SX Prestige"], "engines": ["2.5L 4-Cyl", "2.2L Diesel", "3.3L Turbo"]},
        "Sportage": {"trims": ["LX", "S", "EX", "SX"], "engines": ["2.0L 4-Cyl", "2.0L Turbo", "2.2L Diesel"]},
        "Stinger": {"trims": ["Base", "GT", "GT2", "GT Lounge"], "engines": ["2.0L Turbo", "3.8L V6"]},
        "Telluride": {"trims": ["LX", "S", "EX", "SX", "SX Prestige"], "engines": ["3.8L V6"]},
        "Sedona": {"trims": ["LX", "EX", "SXL", "Limited"], "engines": ["3.8L V6", "2.2L Diesel"]}
    },
    "Lamborghini": {
        "Aventador": {"trims": ["Base", "S", "SV", "SVJ"], "engines": ["6.5L V12"]},
        "Huracán": {"trims": ["Base", "Performante", "Sterrato"], "engines": ["5.2L V10"]},
        "Urus": {"trims": ["Base", "S", "Performante"], "engines": ["4.0L Twin-Turbo V8"]}
    },
    "Land Rover": {
        "Discovery": {"trims": ["SE", "HSE", "Landmark"], "engines": ["2.0L Turbo", "3.0L Supercharged", "2.0L Diesel"]},
        "Discovery Sport": {"trims": ["SE", "HSE", "R-Dynamic"], "engines": ["2.0L Turbo", "2.0L Diesel"]},
        "Range Rover": {"trims": ["Base", "Sport", "Vogue"], "engines": ["3.0L Supercharged", "5.0L V8", "3.0L Turbo Diesel"]},
        "Range Rover Evoque": {"trims": ["Base", "HSE", "R-Dynamic"], "engines": ["2.0L Turbo", "2.0L Diesel"]},
        "Range Rover Sport": {"trims": ["SE", "HSE", "SVR"], "engines": ["3.0L Supercharged", "5.0L V8", "3.0L Turbo Diesel"]},
        "Range Rover Velar": {"trims": ["Base", "HSE", "R-Dynamic"], "engines": ["2.0L Turbo", "3.0L Supercharged", "2.0L Diesel"]}
    },
    "Lexus": {
        "ES": {"trims": ["250", "300h", "350h", "F"], "engines": ["2.5L 4-Cyl", "2.5L Hybrid", "3.5L Hybrid"]},
        "GS": {"trims": ["350", "450h", "F"], "engines": ["3.5L V6", "3.5L Hybrid"]},
        "IS": {"trims": ["300", "350", "500", "F"], "engines": ["2.0L Turbo", "3.5L V6", "5.0L V8"]},
        "GX": {"trims": ["460", "550"], "engines": ["4.6L V8", "5.7L V8"]},
        "LX": {"trims": ["570"], "engines": ["5.7L V8"]},
        "LS": {"trims": ["500", "500h", "F"], "engines": ["3.5L Twin-Turbo", "3.5L Hybrid"]},
        "NX": {"trims": ["250", "350", "350h", "450h+"], "engines": ["2.5L 4-Cyl", "3.5L V6", "Hybrid 2.5L"]},
        "RX": {"trims": ["350", "450h", "450h+", "500h"], "engines": ["3.5L V6", "3.5L Hybrid"]},
        "UX": {"trims": ["200", "250h", "250h AWD"], "engines": ["2.0L 4-Cyl", "Hybrid 2.5L"]}
    },
    "Lincoln": {
        "Aviator": {"trims": ["Premiere", "Select", "Reserve", "Black Label"], "engines": ["3.0L Twin-Turbo", "2.5L Plug-in Hybrid"]},
        "Corsair": {"trims": ["Premiere", "Select", "Reserve"], "engines": ["2.3L Turbo", "2.0L Turbo", "2.5L Plug-in Hybrid"]},
        "MKZ": {"trims": ["Premiere", "Select", "Reserve", "Black Label"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "Navigator": {"trims": ["Premiere", "Select", "Reserve", "Black Label"], "engines": ["3.5L Twin-Turbo"]},
        "Continental": {"trims": ["Base", "Black Label"], "engines": ["3.7L V6", "3.0L Twin-Turbo"]}
    },
    "Lucid": {
        "Air": {"trims": ["Pure", "Touring", "Grand Touring", "Sapphire"], "engines": ["Electric Motor Single", "Electric Motor Dual", "Electric Motor Tri"]}
    },
    "Maserati": {
        "Ghibli": {"trims": ["Base", "S", "Trofeo"], "engines": ["3.0L Twin-Turbo", "3.8L V8"]},
        "Levante": {"trims": ["Base", "S", "Trofeo"], "engines": ["3.0L Twin-Turbo", "3.8L V8"]},
        "Quattroporte": {"trims": ["Base", "S", "Trofeo"], "engines": ["3.0L Twin-Turbo", "3.8L V8"]},
        "MC20": {"trims": ["Base"], "engines": ["3.0L Twin-Turbo V6"]}
    },
    "Mazda": {
        "CX-3": {"trims": ["Sport", "Touring", "Grand Touring"], "engines": ["2.0L 4-Cyl"]},
        "CX-30": {"trims": ["Base", "Select", "Preferred", "Premium"], "engines": ["2.0L 4-Cyl", "1.3L Turbo", "2.5L Turbo"]},
        "CX-50": {"trims": ["Base", "Select", "Preferred", "Premium"], "engines": ["2.5L 4-Cyl", "2.5L Turbo"]},
        "CX-5": {"trims": ["Base", "Select", "Preferred", "Premium"], "engines": ["2.5L 4-Cyl", "2.5L Turbo"]},
        "CX-9": {"trims": ["Base", "Select", "Preferred", "Premium"], "engines": ["2.5L Turbo"]},
        "Mazda2": {"trims": ["Sport", "Select", "Preferred"], "engines": ["1.5L 4-Cyl"]},
        "Mazda3": {"trims": ["Base", "Select", "Preferred", "Premium"], "engines": ["2.0L 4-Cyl", "2.5L 4-Cyl", "2.5L Turbo"]},
        "Mazda6": {"trims": ["Base", "Select", "Preferred", "Premium"], "engines": ["2.5L 4-Cyl", "2.5L Turbo"]},
        "MX-5 Miata": {"trims": ["Sport", "Club", "Grand Touring"], "engines": ["2.0L 4-Cyl", "2.5L 4-Cyl"]}
    },
    "McLaren": {
        "570GT": {"trims": ["Base"], "engines": ["3.8L Twin-Turbo V8"]},
        "570S": {"trims": ["Base"], "engines": ["3.8L Twin-Turbo V8"]},
        "650S": {"trims": ["Base"], "engines": ["3.8L Twin-Turbo V8"]},
        "720S": {"trims": ["Base", "Performance"], "engines": ["4.0L Twin-Turbo V8"]},
        "765LT": {"trims": ["Base"], "engines": ["4.0L Twin-Turbo V8"]}
    },
    "Mercedes-Benz": {
        "A-Class": {"trims": ["A220", "A250", "AMG A35", "AMG A45"], "engines": ["2.0L Turbo", "2.0L Turbo"]},
        "C-Class": {"trims": ["C300", "C300 4MATIC", "C43 AMG", "C63 AMG"], "engines": ["2.0L Turbo", "4.0L Twin-Turbo"]},
        "E-Class": {"trims": ["E350", "E450", "E53 AMG", "E63 AMG"], "engines": ["2.0L Turbo", "3.0L Turbo", "4.0L Twin-Turbo"]},
        "S-Class": {"trims": ["S500", "S580", "AMG S63"], "engines": ["3.0L Twin-Turbo", "4.0L Twin-Turbo"]},
        "G-Class": {"trims": ["G550", "AMG G63"], "engines": ["4.0L Twin-Turbo"]},
        "GLC": {"trims": ["GLC300", "GLC43 AMG", "GLC63 AMG"], "engines": ["2.0L Turbo", "4.0L Twin-Turbo"]},
        "GLE": {"trims": ["GLE350", "GLE450", "GLE53 AMG"], "engines": ["2.0L Turbo", "3.0L Turbo", "4.0L Twin-Turbo"]},
        "GLS": {"trims": ["GLS450", "GLS580", "AMG GLS63"], "engines": ["3.0L Turbo", "4.0L Twin-Turbo"]}
    },
    "Mini": {
        "Clubman": {"trims": ["Base", "Cooper", "Cooper S"], "engines": ["1.5L Turbo", "1.5L Turbo", "2.0L Turbo"]},
        "Countryman": {"trims": ["Base", "Cooper", "Cooper S"], "engines": ["1.5L Turbo", "2.0L Turbo"]},
        "Hardtop": {"trims": ["Base", "Cooper", "Cooper S"], "engines": ["1.5L Turbo", "2.0L Turbo"]}
    },
    "Mitsubishi": {
        "Eclipse": {"trims": ["Base", "Cross"], "engines": ["1.5L Turbo", "3.0L MIVEC"]},
        "Outlander": {"trims": ["ES", "SEL", "Limited", "Hybrid"], "engines": ["2.4L 4-Cyl", "3.0L V6", "Hybrid"]},
        "Lancer": {"trims": ["ES", "SEL", "Ralliart"], "engines": ["2.0L 4-Cyl", "2.0L Turbo"]},
        "Mirage": {"trims": ["Base", "ES", "SEL"], "engines": ["1.2L 3-Cyl"]}
    },
    "Nissan": {
        "Altima": {"trims": ["S", "SV", "SL", "Platinum", "SR Turbo"], "engines": ["2.5L 4-Cyl", "3.5L V6", "2.0L Turbo"]},
        "Leaf": {"trims": ["S", "SV", "Plus", "SL"], "engines": ["Electric Motor 62kWh", "Electric Motor 110kWh"]},
        "Maxima": {"trims": ["S", "SV", "SL", "Platinum"], "engines": ["3.5L V6"]},
        "Murano": {"trims": ["S", "SV", "SL", "Platinum", "Hybrid"], "engines": ["3.5L V6", "Hybrid 3.5L"]},
        "Pathfinder": {"trims": ["S", "SV", "SL", "Platinum"], "engines": ["3.5L V6"]},
        "Rogue": {"trims": ["S", "SV", "SL", "Platinum"], "engines": ["2.5L 4-Cyl"]},
        "Sentra": {"trims": ["S", "SV", "SR", "SL"], "engines": ["2.0L 4-Cyl"]},
        "Z": {"trims": ["Base", "Performance"], "engines": ["3.0L Twin-Turbo V6"]}
    },
    "Polestar": {
        "1": {"trims": ["Base"], "engines": ["3.0L Twin-Turbo Hybrid"]},
        "2": {"trims": ["Standard Range", "Long Range", "Performance"], "engines": ["Electric Motor Single", "Electric Motor Dual"]},
        "3": {"trims": ["Base", "Performance"], "engines": ["Electric Motor Dual"]},
        "4": {"trims": ["Base", "Performance"], "engines": ["Electric Motor Dual"]}
    },
    "Porsche": {
        "911": {"trims": ["Carrera", "Carrera S", "Carrera 4", "Turbo"], "engines": ["3.4L Twin-Turbo", "3.8L Twin-Turbo"]},
        "Cayenne": {"trims": ["Base", "S", "Turbo", "E-Hybrid"], "engines": ["3.0L Turbo", "4.0L Twin-Turbo"]},
        "Macan": {"trims": ["Base", "S", "Turbo"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "Panamera": {"trims": ["Base", "S", "Turbo", "E-Hybrid"], "engines": ["3.0L Twin-Turbo", "4.0L Twin-Turbo"]}
    },
    "Ram": {
        "1500": {"trims": ["Tradesman", "SLT", "Laramie", "Rebel", "Limited", "Tungsten"], "engines": ["3.6L V6", "5.7L V8", "3.0L EcoDiesel"]},
        "2500": {"trims": ["Tradesman", "Power Wagon", "SLT", "Laramie", "Limited"], "engines": ["6.4L V8", "6.7L Cummins Diesel"]},
        "3500": {"trims": ["Tradesman", "SLT", "Laramie"], "engines": ["6.4L V8", "6.7L Cummins Diesel"]}
    },
    "Renault": {
        "Clio": {"trims": ["Base", "Interactive"], "engines": ["1.2L Turbo", "1.0L Turbo"]},
        "Espace": {"trims": ["Base", "Dynamique"], "engines": ["1.6L Turbo", "1.5L Diesel"]},
        "Megane": {"trims": ["Base", "Dynamique"], "engines": ["1.2L Turbo", "1.5L Diesel"]}
    },
    "Rivian": {
        "R1S": {"trims": ["Dual Motor", "Quad Motor", "Tri Motor"], "engines": ["Electric Motor Dual", "Electric Motor Quad"]},
        "R1T": {"trims": ["Dual Motor", "Quad Motor", "Tri Motor"], "engines": ["Electric Motor Dual", "Electric Motor Quad"]}
    },
    "Rolls-Royce": {
        "Ghost": {"trims": ["Base", "Black Badge"], "engines": ["6.75L Twin-Turbo V12"]},
        "Phantom": {"trims": ["Base", "Black Badge"], "engines": ["6.75L Twin-Turbo V12"]},
        "Cullinan": {"trims": ["Base", "Black Badge"], "engines": ["6.75L Twin-Turbo V12"]}
    },
    "Saab": {
        "9-3": {"trims": ["Base", "Sport"], "engines": ["2.0L Turbo", "2.8L V6"]},
        "9-5": {"trims": ["Base", "Aero"], "engines": ["2.3L Turbo", "3.0L V6"]}
    },
    "Subaru": {
        "Ascent": {"trims": ["Base", "Premium", "Limited", "Touring"], "engines": ["2.4L Turbo"]},
        "BRZ": {"trims": ["Base", "Premium", "Limited"], "engines": ["2.4L Boxer"]},
        "Crosstrek": {"trims": ["Base", "Premium", "Sport", "Limited"], "engines": ["2.0L Boxer", "2.5L Turbo"]},
        "Forester": {"trims": ["Base", "Premium", "Sport", "Limited", "Touring"], "engines": ["2.5L Boxer", "2.0L Turbo"]},
        "Impreza": {"trims": ["Base", "Premium", "Sport", "Limited"], "engines": ["2.0L Boxer"]},
        "Legacy": {"trims": ["Base", "Premium", "Sport", "Limited", "Touring"], "engines": ["2.5L Boxer"]},
        "Outback": {"trims": ["Base", "Premium", "Sport", "Limited", "Touring"], "engines": ["2.5L Boxer"]},
        "WRX": {"trims": ["Base", "Premium", "STI", "Limited"], "engines": ["2.0L Turbo Boxer", "2.5L Turbo Boxer"]}
    },
    "Suzuki": {
        "Swift": {"trims": ["Base", "VXi", "ZXi"], "engines": ["1.2L 4-Cyl"]},
        "Vitara": {"trims": ["Base", "SZ5"], "engines": ["1.6L 4-Cyl", "1.4L Turbo"]},
        "S-Cross": {"trims": ["Base", "ZXi"], "engines": ["1.3L Turbo", "1.5L"]}
    },
    "Tata": {
        "Nexon": {"trims": ["XE", "XM", "EV"], "engines": ["1.2L Turbo", "1.5L Diesel"]},
        "Harrier": {"trims": ["XE", "XM"], "engines": ["2.0L Diesel", "1.5L Turbo"]}
    },
    "Tesla": {
        "Model 3": {"trims": ["Standard Range", "Long Range", "Performance", "Plaid"], "engines": ["Electric Motor Single", "Electric Motor Dual", "Electric Motor Tri"]},
        "Model S": {"trims": ["Long Range", "Performance", "Plaid"], "engines": ["Electric Motor Dual", "Electric Motor Tri"]},
        "Model X": {"trims": ["Long Range", "Performance", "Plaid"], "engines": ["Electric Motor Dual", "Electric Motor Tri"]},
        "Model Y": {"trims": ["RWD", "Long Range", "Performance"], "engines": ["Electric Motor Single", "Electric Motor Dual"]}
    },
    "Toyota": {
        "Camry": {"trims": ["LE", "SE", "XLE", "TRD", "Hybrid LE", "Hybrid SE", "Hybrid XLE"], "engines": ["2.5L 4-Cyl", "3.5L V6", "2.5L Hybrid"]},
        "Corolla": {"trims": ["L", "LE", "SE", "XLE", "GR", "Hybrid LE", "Hybrid SE"], "engines": ["1.8L 4-Cyl", "2.0L 4-Cyl", "2.0L Hybrid"]},
        "GR Supra": {"trims": ["2.0", "3.0"], "engines": ["2.0L Turbo", "3.0L Twin-Turbo"]},
        "RAV4": {"trims": ["LE", "XLE", "Adventure", "TRD", "Prime LE", "Prime XLE"], "engines": ["2.5L 4-Cyl", "2.5L Hybrid", "2.5L Plug-in Hybrid"]},
        "Highlander": {"trims": ["L", "LE", "XLE", "Limited", "Platinum", "Hybrid LE"], "engines": ["3.5L V6", "3.5L Hybrid"]},
        "Prius": {"trims": ["LE", "XLE", "Limited", "Prime LE", "Prime XLE"], "engines": ["1.8L Hybrid", "1.8L Plug-in Hybrid"]},
        "4Runner": {"trims": ["SR5", "TRD", "TRD Pro", "Limited"], "engines": ["4.0L V6"]},
        "Tacoma": {"trims": ["SR", "SR5", "TRD", "Limited"], "engines": ["2.7L 4-Cyl", "3.5L V6"]},
        "Tundra": {"trims": ["SR", "SR5", "Limited", "Platinum"], "engines": ["3.4L Twin-Turbo", "5.7L V8"]},
        "Sienna": {"trims": ["LE", "XLE", "Limited", "Platinum", "Hybrid"], "engines": ["2.5L Hybrid"]}
    },
    "Volkswagen": {
        "Golf": {"trims": ["S", "SE", "SEL", "GTI", "R"], "engines": ["1.5L Turbo", "2.0L Turbo", "2.0L TSI"]},
        "Jetta": {"trims": ["S", "SE", "SEL", "GLI"], "engines": ["1.5L Turbo", "1.4L Turbo", "2.0L Turbo"]},
        "Passat": {"trims": ["S", "SE", "SEL", "GLI"], "engines": ["1.8L Turbo", "2.0L Turbo", "3.6L V6"]},
        "Tiguan": {"trims": ["S", "SE", "SEL", "R-Line"], "engines": ["1.4L Turbo", "2.0L Turbo"]},
        "Atlas": {"trims": ["S", "SE", "SEL", "R-Line"], "engines": ["2.0L Turbo", "3.6L V6"]},
        "ID.4": {"trims": ["Standard", "Pro", "Pro Max"], "engines": ["Electric Motor Single", "Electric Motor Dual"]},
        "ID.5": {"trims": ["Standard", "Pro", "Pro Max"], "engines": ["Electric Motor Single", "Electric Motor Dual"]}
    },
    "Volvo": {
        "S60": {"trims": ["Momentum", "Inscription", "R-Design", "Polestar"], "engines": ["2.0L Turbo", "2.0L Turbo Hybrid"]},
        "S90": {"trims": ["Momentum", "Inscription", "R-Design"], "engines": ["2.0L Turbo", "2.0L Turbo Hybrid"]},
        "XC40": {"trims": ["Momentum", "Inscription", "R-Design", "Recharge"], "engines": ["2.0L Turbo", "2.0L Turbo Hybrid"]},
        "XC60": {"trims": ["Momentum", "Inscription", "R-Design", "Polestar", "Recharge"], "engines": ["2.0L Turbo", "2.0L Turbo Hybrid"]},
        "XC90": {"trims": ["Momentum", "Inscription", "R-Design", "Recharge"], "engines": ["2.0L Turbo", "2.0L Turbo Hybrid"]}
    },
    "Xpeng": {
        "G9": {"trims": ["Base", "Plus", "Max"], "engines": ["Electric Motor Single", "Electric Motor Dual"]},
        "P7": {"trims": ["Base", "Plus", "Max"], "engines": ["Electric Motor Single", "Electric Motor Dual"]},
        "P8": {"trims": ["Base", "Plus", "Max"], "engines": ["Electric Motor Single", "Electric Motor Dual"]}
    }
}

@app.get("/")
def root():
    return {"status": "ready"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes():
    return sorted(list(CAR_DATABASE.keys()))

@app.get("/api/cars/models")
def get_models(make: str):
    if make not in CAR_DATABASE:
        return []
    return sorted(list(CAR_DATABASE[make].keys()))

@app.get("/api/cars/trims")
def get_trims(make: str, model: str):
    if make not in CAR_DATABASE or model not in CAR_DATABASE[make]:
        return []
    return sorted(CAR_DATABASE[make][model].get("trims", []))

@app.get("/api/cars/engines")
def get_engines(make: str, model: str):
    if make not in CAR_DATABASE or model not in CAR_DATABASE[make]:
        return []
    return sorted(CAR_DATABASE[make][model].get("engines", []))

@app.get("/api/cars/colors")
def get_colors():
    return sorted(COLORS)

@app.get("/api/cars/decode-vin")
def decode_vin(vin: str):
    """Decode VIN using NHTSA API"""
    try:
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

@app.post("/api/leads/webhook/lead_received")
def lead_received(data: dict):
    """Receive lead submission"""
    try:
        lead_id = f"LEAD_{data.get('vin', 'UNKNOWN')[:8]}"
        
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