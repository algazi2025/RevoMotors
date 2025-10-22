"""
Migration script: Load comprehensive car data into PostgreSQL database
Includes all major car makes and models available in the market
Run this once to populate the database
"""

from database import SessionLocal, init_db, Make, Model, Trim, BodyType, Transmission, FuelType

# Comprehensive car database with all major makes and models
CAR_DATABASE = {
    # American Makes
    "Ford": {
        "models": {
            "F-150": {"years": list(range(1990, 2026)), "trims": ["XL", "XLT", "Lariat", "King Ranch", "Platinum", "Limited", "Raptor"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid", "Electric"]},
            "Mustang": {"years": list(range(1990, 2026)), "trims": ["EcoBoost", "GT", "Mach 1", "Shelby GT500"], "body_types": ["Coupe", "Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Explorer": {"years": list(range(1991, 2026)), "trims": ["Base", "XLT", "Limited", "ST", "Platinum"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Escape": {"years": list(range(2001, 2026)), "trims": ["S", "SE", "SEL", "Titanium"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Edge": {"years": list(range(2007, 2026)), "trims": ["SE", "SEL", "Limited", "ST"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Fusion": {"years": list(range(2006, 2020)), "trims": ["S", "SE", "SEL", "Titanium"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Focus": {"years": list(range(2000, 2019)), "trims": ["S", "SE", "SEL", "ST"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Fiesta": {"years": list(range(2010, 2019)), "trims": ["S", "SE", "SEL", "ST"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Bronco": {"years": list(range(2021, 2026)), "trims": ["Base", "Big Bend", "Black Diamond", "Wildtrak", "Raptor"], "body_types": ["SUV"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Ranger": {"years": list(range(1983, 2026)), "trims": ["XL", "XLT", "Lariat", "King Ranch", "Raptor"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Chevrolet": {
        "models": {
            "Silverado 1500": {"years": list(range(1999, 2026)), "trims": ["WT", "Custom", "LT", "RST", "LTZ", "High Country"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "Silverado 2500HD": {"years": list(range(2001, 2026)), "trims": ["WT", "Custom", "LT", "RST", "LTZ", "High Country"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "Malibu": {"years": list(range(1997, 2026)), "trims": ["L", "LS", "LT", "Premier"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Equinox": {"years": list(range(2005, 2026)), "trims": ["L", "LS", "LT", "Premier"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Tahoe": {"years": list(range(1995, 2026)), "trims": ["LS", "LT", "RST", "Z71", "Premier", "High Country"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Suburban": {"years": list(range(1992, 2026)), "trims": ["LS", "LT", "RST", "Premier", "High Country"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Traverse": {"years": list(range(2009, 2026)), "trims": ["L", "LS", "LT", "Premier", "High Country"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Blazer": {"years": list(range(2019, 2026)), "trims": ["L", "LT", "RS", "Premier", "SS"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Trailblazer": {"years": list(range(2021, 2026)), "trims": ["LS", "LT", "ACTIV", "RS"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Colorado": {"years": list(range(2004, 2026)), "trims": ["Base", "WT", "LT", "Z71", "ZR2"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline", "Diesel"]},
            "Cruze": {"years": list(range(2011, 2019)), "trims": ["L", "LS", "LT", "Premier"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Spark": {"years": list(range(2013, 2026)), "trims": ["LS", "LT", "Premier"], "body_types": ["Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "GMC": {
        "models": {
            "Sierra 1500": {"years": list(range(1999, 2026)), "trims": ["Regular Cab", "Double Cab", "Crew Cab", "SLE", "SLT", "Denali"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "Yukon": {"years": list(range(1992, 2026)), "trims": ["SL", "SLE", "SLT", "Denali"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Terrain": {"years": list(range(2010, 2026)), "trims": ["SL", "SLE", "SLT", "Denali"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Acadia": {"years": list(range(2007, 2026)), "trims": ["SL", "SLE", "SLT", "Denali"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Canyon": {"years": list(range(2004, 2026)), "trims": ["Base", "SLE", "SLT", "Denali"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline", "Diesel"]},
        }
    },
    "Dodge": {
        "models": {
            "Ram 1500": {"years": list(range(1994, 2026)), "trims": ["Regular Cab", "Quad Cab", "Crew Cab", "SL", "SLT", "Laramie"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline", "Diesel"]},
            "Charger": {"years": list(range(2006, 2024)), "trims": ["SE", "SXT", "R/T", "RT Scat Pack", "Hellcat"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Challenger": {"years": list(range(2008, 2026)), "trims": ["SRT8", "RT", "R/T Scat Pack", "Hellcat"], "body_types": ["Coupe"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Durango": {"years": list(range(2011, 2026)), "trims": ["SXT", "Limited", "R/T", "Citadel"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Journey": {"years": list(range(2009, 2023)), "trims": ["SE", "SXT", "Limited", "Crossroad"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
        }
    },
    
    # Japanese Makes
    "Honda": {
        "models": {
            "Accord": {"years": list(range(1990, 2026)), "trims": ["LX", "Sport", "EX", "EX-L", "Touring"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual", "CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Civic": {"years": list(range(1990, 2026)), "trims": ["LX", "Sport", "EX", "EX-L", "Touring", "Si", "Type R"], "body_types": ["Sedan", "Coupe", "Hatchback"], "transmissions": ["Automatic", "Manual", "CVT"], "fuel_types": ["Gasoline"]},
            "CR-V": {"years": list(range(1997, 2026)), "trims": ["LX", "EX", "EX-L", "Touring"], "body_types": ["SUV"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Pilot": {"years": list(range(2003, 2026)), "trims": ["LX", "EX", "EX-L", "Touring", "Elite"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Odyssey": {"years": list(range(1995, 2026)), "trims": ["LX", "EX", "EX-L", "Touring", "Elite"], "body_types": ["Minivan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Ridgeline": {"years": list(range(2006, 2026)), "trims": ["Sport", "RT", "RTL", "RTL-E", "Black Edition"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Fit": {"years": list(range(2007, 2026)), "trims": ["LX", "Sport", "EX"], "body_types": ["Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Insight": {"years": list(range(2010, 2026)), "trims": ["LX", "EX", "Touring"], "body_types": ["Sedan"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
        }
    },
    "Toyota": {
        "models": {
            "Camry": {"years": list(range(1990, 2026)), "trims": ["LE", "SE", "XLE", "XSE", "TRD"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Corolla": {"years": list(range(1990, 2026)), "trims": ["L", "LE", "SE", "XLE", "XSE"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual", "CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
            "RAV4": {"years": list(range(1996, 2026)), "trims": ["LE", "XLE", "XLE Premium", "Adventure", "TRD Off-Road", "Limited"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Highlander": {"years": list(range(2001, 2026)), "trims": ["L", "LE", "XLE", "Limited", "Platinum"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Tacoma": {"years": list(range(1995, 2026)), "trims": ["SR", "SR5", "TRD Sport", "TRD Off-Road", "Limited", "TRD Pro"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Tundra": {"years": list(range(2000, 2026)), "trims": ["SR", "SR5", "Limited", "Platinum"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Sienna": {"years": list(range(1998, 2026)), "trims": ["LE", "XLE", "Limited", "Platinum"], "body_types": ["Minivan"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Celica": {"years": list(range(1990, 2006)), "trims": ["ST", "GT", "GTS"], "body_types": ["Coupe"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Prius": {"years": list(range(2000, 2026)), "trims": ["Two", "Three", "Four", "Five"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Yaris": {"years": list(range(2006, 2026)), "trims": ["L", "LE", "XLE"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "4Runner": {"years": list(range(1984, 2026)), "trims": ["SR5", "Limited", "TRD Off-Road", "TRD Pro"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
        }
    },
    "Nissan": {
        "models": {
            "Altima": {"years": list(range(1993, 2026)), "trims": ["S", "SV", "SR", "SL", "Platinum"], "body_types": ["Sedan"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline"]},
            "Rogue": {"years": list(range(2008, 2026)), "trims": ["S", "SV", "SL", "Platinum"], "body_types": ["SUV"], "transmissions": ["CVT"], "fuel_types": ["Gasoline"]},
            "Sentra": {"years": list(range(1990, 2026)), "trims": ["S", "SV", "SR"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual", "CVT"], "fuel_types": ["Gasoline"]},
            "Maxima": {"years": list(range(1981, 2026)), "trims": ["S", "SV", "SL", "Platinum"], "body_types": ["Sedan"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline"]},
            "Murano": {"years": list(range(2003, 2026)), "trims": ["S", "SV", "SL", "Platinum"], "body_types": ["SUV"], "transmissions": ["Automatic", "CVT"], "fuel_types": ["Gasoline"]},
            "Pathfinder": {"years": list(range(1986, 2026)), "trims": ["S", "SV", "SL", "Platinum"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Frontier": {"years": list(range(2005, 2026)), "trims": ["S", "SV", "SL", "Pro"], "body_types": ["Pickup Truck"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Leaf": {"years": list(range(2011, 2026)), "trims": ["S", "SV", "SL", "Plus"], "body_types": ["Hatchback"], "transmissions": ["Single-Speed Automatic"], "fuel_types": ["Electric"]},
            "370Z": {"years": list(range(2009, 2023)), "trims": ["Base", "Sport", "Sport Tech"], "body_types": ["Coupe"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Mazda": {
        "models": {
            "3": {"years": list(range(2004, 2026)), "trims": ["Sport", "Select", "Preferred", "Premium"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "6": {"years": list(range(2003, 2026)), "trims": ["Sport", "Select", "Preferred", "Premium"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "CX-5": {"years": list(range(2013, 2026)), "trims": ["Sport", "Select", "Preferred", "Premium"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "CX-3": {"years": list(range(2016, 2026)), "trims": ["Sport", "Select", "Preferred", "Premium"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "CX-9": {"years": list(range(2007, 2026)), "trims": ["Sport", "Select", "Preferred", "Premium"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "MX-5": {"years": list(range(1989, 2026)), "trims": ["Sport", "Club", "Grand Touring"], "body_types": ["Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Subaru": {
        "models": {
            "Outback": {"years": list(range(1995, 2026)), "trims": ["Base", "Premium", "Limited", "Touring", "Wilderness"], "body_types": ["Wagon"], "transmissions": ["CVT"], "fuel_types": ["Gasoline"]},
            "Forester": {"years": list(range(1998, 2026)), "trims": ["Base", "Premium", "Sport", "Limited", "Touring"], "body_types": ["SUV"], "transmissions": ["CVT"], "fuel_types": ["Gasoline"]},
            "Crosstrek": {"years": list(range(2013, 2026)), "trims": ["Base", "Premium", "Sport", "Limited"], "body_types": ["SUV"], "transmissions": ["CVT", "Manual"], "fuel_types": ["Gasoline"]},
            "Impreza": {"years": list(range(1992, 2026)), "trims": ["Base", "Premium", "Sport", "Limited"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["CVT", "Manual"], "fuel_types": ["Gasoline"]},
            "Legacy": {"years": list(range(1989, 2026)), "trims": ["Base", "Premium", "Sport", "Limited"], "body_types": ["Sedan"], "transmissions": ["CVT"], "fuel_types": ["Gasoline"]},
            "WRX": {"years": list(range(2002, 2026)), "trims": ["Base", "Premium", "Limited"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "BRZ": {"years": list(range(2012, 2026)), "trims": ["Base", "Premium", "Limited"], "body_types": ["Coupe"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Mitsubishi": {
        "models": {
            "Outlander": {"years": list(range(2003, 2026)), "trims": ["ES", "SE", "SEL", "GT"], "body_types": ["SUV"], "transmissions": ["CVT", "Manual"], "fuel_types": ["Gasoline"]},
            "Lancer": {"years": list(range(1973, 2023)), "trims": ["ES", "SE", "SEL", "GT"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Mirage": {"years": list(range(2014, 2026)), "trims": ["ES", "SE", "SEL"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Eclipse Cross": {"years": list(range(2018, 2026)), "trims": ["ES", "SE", "Limited"], "body_types": ["SUV"], "transmissions": ["CVT"], "fuel_types": ["Gasoline"]},
        }
    },
    "Hyundai": {
        "models": {
            "Elantra": {"years": list(range(2000, 2026)), "trims": ["SE", "SEL", "SLT", "Ultimate"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Sonata": {"years": list(range(1989, 2026)), "trims": ["SE", "SEL", "Limited", "Ultimate"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Tucson": {"years": list(range(2005, 2026)), "trims": ["SE", "SEL", "Limited", "Ultimate"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Santa Fe": {"years": list(range(2001, 2026)), "trims": ["SE", "SEL", "Limited", "Ultimate"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Prius v": {"years": list(range(2012, 2026)), "trims": ["L", "LE", "XLE"], "body_types": ["Hatchback"], "transmissions": ["CVT"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Kona": {"years": list(range(2018, 2026)), "trims": ["SE", "SEL", "Limited", "Ultimate"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid", "Electric"]},
            "Venue": {"years": list(range(2020, 2026)), "trims": ["SE", "SEL", "Limited"], "body_types": ["SUV"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Kia": {
        "models": {
            "Forte": {"years": list(range(2010, 2026)), "trims": ["FX", "S", "EX", "SX"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Optima": {"years": list(range(2011, 2020)), "trims": ["LX", "EX", "SX"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid"]},
            "Sportage": {"years": list(range(2005, 2026)), "trims": ["LX", "S", "EX", "SX"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Sorento": {"years": list(range(2003, 2026)), "trims": ["L", "LX", "EX", "SX"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Seltos": {"years": list(range(2020, 2026)), "trims": ["LX", "S", "EX", "SX"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Telluride": {"years": list(range(2020, 2026)), "trims": ["L", "S", "EX", "SX"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Rio": {"years": list(range(2012, 2026)), "trims": ["FX", "S", "EX"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    
    # Luxury Makes
    "BMW": {
        "models": {
            "3 Series": {"years": list(range(1990, 2026)), "trims": ["330i", "M340i", "M3"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "5 Series": {"years": list(range(1997, 2026)), "trims": ["530i", "540i", "M550i"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "7 Series": {"years": list(range(1977, 2026)), "trims": ["730i", "750i", "M760i"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "X3": {"years": list(range(2004, 2026)), "trims": ["xDrive30i", "xDrive40i", "M40i"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "X5": {"years": list(range(2000, 2026)), "trims": ["sDrive40i", "xDrive40i", "M50i"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Hybrid", "Diesel"]},
            "X7": {"years": list(range(2019, 2026)), "trims": ["xDrive40i", "xDrive50i", "M60i"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Z4": {"years": list(range(2003, 2026)), "trims": ["sDrive30i", "sDrive40i", "M40i"], "body_types": ["Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Mercedes-Benz": {
        "models": {
            "C-Class": {"years": list(range(1993, 2026)), "trims": ["C 300", "C 43 AMG", "C 63 AMG"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "E-Class": {"years": list(range(1984, 2026)), "trims": ["E 350", "E 450", "AMG E 53"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "S-Class": {"years": list(range(1998, 2026)), "trims": ["S 500", "S 580", "AMG S 63"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "GLE": {"years": list(range(1998, 2026)), "trims": ["GLE 350", "GLE 450", "AMG GLE 53", "AMG GLE 63"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel", "Hybrid"]},
            "GLC": {"years": list(range(2016, 2026)), "trims": ["GLC 300", "GLC 43 AMG", "GLC 63 AMG"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "GLA": {"years": list(range(2014, 2026)), "trims": ["GLA 250", "GLA 35 AMG", "GLA 45 AMG"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "A-Class": {"years": list(range(2013, 2026)), "trims": ["A 220", "A 250", "AMG A 35"], "body_types": ["Hatchback"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
        }
    },
    "Audi": {
        "models": {
            "A3": {"years": list(range(1996, 2026)), "trims": ["Standard", "Premium", "Prestige", "S3"], "body_types": ["Sedan", "Hatchback"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "A4": {"years": list(range(1994, 2026)), "trims": ["Standard", "Premium", "Prestige", "S4"], "body_types": ["Sedan"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "A6": {"years": list(range(1994, 2026)), "trims": ["Standard", "Premium", "Prestige", "S6"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Q3": {"years": list(range(2012, 2026)), "trims": ["Standard", "Premium", "Prestige", "SQ3"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Q5": {"years": list(range(2008, 2026)), "trims": ["Standard", "Premium", "Prestige", "SQ5"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Q7": {"years": list(range(2006, 2026)), "trims": ["Standard", "Premium", "Prestige", "SQ7"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
        }
    },
    "Porsche": {
        "models": {
            "911": {"years": list(range(1963, 2026)), "trims": ["Carrera", "Carrera S", "Carrera GTS", "Turbo"], "body_types": ["Coupe", "Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Cayenne": {"years": list(range(2003, 2026)), "trims": ["Base", "S", "GTS", "Turbo"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Macan": {"years": list(range(2015, 2026)), "trims": ["Base", "S", "GTS", "Turbo"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
            "Boxster": {"years": list(range(1996, 2026)), "trims": ["Base", "S", "GTS"], "body_types": ["Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Panamera": {"years": list(range(2009, 2026)), "trims": ["Base", "S", "Turbo"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline"]},
        }
    },
    "Jaguar": {
        "models": {
            "XE": {"years": list(range(2015, 2026)), "trims": ["S", "SE", "HSE"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "XF": {"years": list(range(2008, 2026)), "trims": ["S", "SE", "HSE"], "body_types": ["Sedan"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "F-PACE": {"years": list(range(2016, 2026)), "trims": ["S", "SE", "HSE"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
        }
    },
    "Land Rover": {
        "models": {
            "Range Rover": {"years": list(range(1970, 2026)), "trims": ["SE", "HSE", "Supercharged"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "Range Rover Sport": {"years": list(range(2005, 2026)), "trims": ["SE", "HSE", "Supercharged"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "Discovery": {"years": list(range(1989, 2026)), "trims": ["SE", "HSE", "Supercharged"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
        }
    },
    
    # Electric & Hybrid
    "Tesla": {
        "models": {
            "Model 3": {"years": list(range(2017, 2026)), "trims": ["Standard Range Plus", "Long Range", "Performance"], "body_types": ["Sedan"], "transmissions": ["Single-Speed Automatic"], "fuel_types": ["Electric"]},
            "Model Y": {"years": list(range(2020, 2026)), "trims": ["Long Range", "Performance"], "body_types": ["SUV"], "transmissions": ["Single-Speed Automatic"], "fuel_types": ["Electric"]},
            "Model S": {"years": list(range(2012, 2026)), "trims": ["Long Range", "Plaid"], "body_types": ["Sedan"], "transmissions": ["Single-Speed Automatic"], "fuel_types": ["Electric"]},
            "Model X": {"years": list(range(2015, 2026)), "trims": ["Long Range", "Plaid"], "body_types": ["SUV"], "transmissions": ["Single-Speed Automatic"], "fuel_types": ["Electric"]},
            "Roadster": {"years": list(range(2008, 2012)), "trims": ["Base"], "body_types": ["Convertible"], "transmissions": ["Single-Speed Automatic"], "fuel_types": ["Electric"]},
        }
    },
    
    # Sport & Performance
    "Jeep": {
        "models": {
            "Wrangler": {"years": list(range(1990, 2026)), "trims": ["Sport", "Sport S", "Sahara", "Rubicon"], "body_types": ["SUV"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline", "Diesel", "Hybrid"]},
            "Grand Cherokee": {"years": list(range(1993, 2026)), "trims": ["Laredo", "Limited", "Overland", "Summit", "SRT", "Trackhawk"], "body_types": ["SUV"], "transmissions": ["Automatic"], "fuel_types": ["Gasoline", "Diesel"]},
            "Cherokee": {"years": list(range(1984, 2026)), "trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "body_types": ["SUV"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Compass": {"years": list(range(2007, 2026)), "trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "body_types": ["SUV"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Renegade": {"years": list(range(2015, 2026)), "trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "body_types": ["SUV"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Chevrolet": {
        "models": {
            "Corvette": {"years": list(range(1953, 2026)), "trims": ["Base", "Stingray", "Z06"], "body_types": ["Coupe", "Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
            "Camaro": {"years": list(range(1966, 2024)), "trims": ["SS", "ZL1"], "body_types": ["Coupe", "Convertible"], "transmissions": ["Automatic", "Manual"], "fuel_types": ["Gasoline"]},
        }
    },
    "Ford": {
        "models": {
            "GT": {"years": list(range(2005, 2006)), "trims": ["Base"], "body_types": ["Coupe"], "transmissions": ["Manual"], "fuel_types": ["Gasoline"]},
        }
    },
}


def seed_database():
    """Populate database with comprehensive car data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Make).count() > 0:
            print("Database already populated. Skipping seed.")
            return
        
        print("Starting comprehensive database seed...")
        total_makes = len(CAR_DATABASE)
        total_models = sum(len(make_data["models"]) for make_data in CAR_DATABASE.values())
        
        print(f"📊 Total makes: {total_makes}")
        print(f"📊 Total models: {total_models}")
        print()
        
        for make_name, make_data in CAR_DATABASE.items():
            print(f"✏️  Adding {make_name}... ({len(make_data['models'])} models)")
            
            # Create or get make
            make = db.query(Make).filter(Make.name == make_name).first()
            if not make:
                make = Make(name=make_name)
                db.add(make)
                db.flush()
            
            # Add models for this make
            for model_name, model_data in make_data["models"].items():
                model = Model(
                    name=model_name,
                    make_id=make.id,
                    year_min=min(model_data["years"]),
                    year_max=max(model_data["years"])
                )
                db.add(model)
                db.flush()
                
                # Add trims
                for trim_name in model_data["trims"]:
                    trim = db.query(Trim).filter(Trim.name == trim_name).first()
                    if not trim:
                        trim = Trim(name=trim_name)
                        db.add(trim)
                        db.flush()
                    model.trims.append(trim)
                
                # Add body types
                for body_type_name in model_data["body_types"]:
                    body_type = db.query(BodyType).filter(BodyType.name == body_type_name).first()
                    if not body_type:
                        body_type = BodyType(name=body_type_name)
                        db.add(body_type)
                        db.flush()
                    model.body_types.append(body_type)
                
                # Add transmissions
                for transmission_name in model_data["transmissions"]:
                    transmission = db.query(Transmission).filter(Transmission.name == transmission_name).first()
                    if not transmission:
                        transmission = Transmission(name=transmission_name)
                        db.add(transmission)
                        db.flush()
                    model.transmissions.append(transmission)
                
                # Add fuel types
                for fuel_type_name in model_data["fuel_types"]:
                    fuel_type = db.query(FuelType).filter(FuelType.name == fuel_type_name).first()
                    if not fuel_type:
                        fuel_type = FuelType(name=fuel_type_name)
                        db.add(fuel_type)
                        db.flush()
                    model.fuel_types.append(fuel_type)
        
        db.commit()
        print()
        print("=" * 50)
        print("✅ Database seed completed successfully!")
        print("=" * 50)
        print(f"✓ {total_makes} car makes added")
        print(f"✓ {total_models} car models added")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_database()
