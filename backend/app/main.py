from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import logging
import re

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
    askingPrice: Optional[int] = None
    description: Optional[str] = None

COLORS = [
    "Absolute Black Pearl", "Ashen Gray Metallic", "Audi Brilliant Black", "Black", "Black Obsidian", "Black Pearl", "Black Uni",
    "Blazing Blue Metallic", "Blizzard Blue", "Blizzard White", "Blizzard White Pearl", "Bright Silver Metallic", "Bright White",
    "Brilliant Black Metallic", "Brilliant Black Pearl", "Brilliant Silver Metallic", "Bronze Fire Metallic", "Brown Metallic",
    "Burnished Copper Metallic", "Cabo Blue Metallic", "Candy Red", "Carbonite Gray", "Carbon Gray", "Carbon Gray Metallic",
    "Carbon Steel Gray Metallic", "Cardinal Red", "Cascade Blue Metallic", "Cashmere Beige", "Cashmere Metallic", "Celestial Blue",
    "Celtic Gray Metallic", "Charcoal", "Charcoal Gray", "Charcoal Gray Metallic", "Charcoal Metallic", "Cherry Black", "Cherry Red",
    "Cherry Red Pearl", "Chestnut", "Chestnut Brown Metallic", "Chestnut Metallic", "Cinnamon", "Cinnamon Brown Metallic", "Cinnamon Metallic",
    "Citrus Burst", "Citrus Metallic", "Class Black Metallic", "Classic Red", "Classic Silver Metallic", "Clearcoat White", "Cliff Blue Metallic",
    "Cloud Gray", "Cloudy White", "Cloudy White Pearl", "Coal Black", "Coal Black Metallic", "Coal Black Pearl", "Coal Metallic",
    "Cobalt Blue", "Cobalt Blue Metallic", "Cocoa Brown", "Cocoa Brown Metallic", "Cocoa Metallic", "Code Blue Metallic", "Coffee Brown",
    "Coffee Brown Metallic", "Coliseum Gray", "Coliseum Gray Metallic", "Colonial Blue Metallic", "Colorado Blue", "Compact Gray Metallic",
    "Complex Gray Metallic", "Concord Blue", "Concord Blue Metallic", "Concord Purple Metallic", "Concord White", "Concord White Pearl",
    "Concrete", "Concrete Gray", "Concrete Gray Metallic", "Concrete Metallic", "Conifer Green Metallic", "Continental Blue", "Continental Blue Metallic",
    "Continental Brown", "Continental Brown Metallic", "Continental Gray", "Continental Gray Metallic", "Continental Metallic", "Continental Silver",
    "Continental Silver Metallic", "Continental White", "Copper", "Copper Brown Metallic", "Copper Metallic", "Coral Red", "Coral Red Pearl",
    "Cosmo Black", "Cosmic Black Metallic", "Cosmic Blue", "Cosmic Blue Metallic", "Cosmic Gray Metallic", "Cosmic Red Metallic",
    "Cosmic Silver", "Cosmic Silver Metallic", "Cosmos Gray Metallic", "Costal Gray Metallic", "Crystal Black", "Crystal Black Pearl",
    "Crystal Black Pearl Metallic", "Crystal Blue", "Crystal Blue Metallic", "Crystal Blue Pearl", "Crystal Gray", "Crystal Gray Metallic",
    "Crystal Pearl", "Crystal Red", "Crystal Red Metallic", "Crystal Red Pearl", "Crystal Silver", "Crystal Silver Metallic", "Crystal White",
    "Crystal White Pearl", "Cube Orange", "Cube Orange Metallic", "Cumulus Gray", "Cumulus Gray Metallic", "Currant Blue Metallic",
    "Cyber Gray", "Cyber Gray Metallic", "Cyber Orange", "Cyber Orange Metallic", "Cyber Red", "Cyber Silver", "Cyber Silver Metallic",
    "Cyclone Gray Metallic", "Dark Abyss Blue", "Dark Abyss Blue Metallic", "Dark Asphalt", "Dark Ash Gray", "Dark Ash Gray Metallic",
    "Dark Ash Metallic", "Dark Blue", "Dark Blue Metallic", "Dark Blue Pearl", "Dark Blue Uni", "Dark Charcoal", "Dark Charcoal Gray",
    "Dark Charcoal Gray Metallic", "Dark Charcoal Metallic", "Dark Cherry Red", "Dark Cherry Red Metallic", "Dark Fawn Metallic", "Dark French Blue",
    "Dark French Blue Metallic", "Dark Gingersnap", "Dark Gingersnap Metallic", "Dark Gray", "Dark Gray Metallic", "Dark Gray Uni",
    "Dark Graphite", "Dark Graphite Metallic", "Dark Graphite Uni", "Dark Green Metallic", "Dark Graystone", "Dark Greystone Metallic",
    "Dark Highland Gray", "Dark Highland Gray Metallic", "Dark Indigo Blue", "Dark Indigo Blue Metallic", "Dark Jacaranda Purple",
    "Dark Jacaranda Purple Metallic", "Dark Obsidian Blue", "Dark Pearl", "Dark Pearl Mica", "Dark Pearl Red", "Dark Plum Metallic",
    "Dark Purple Metallic", "Dark Red", "Dark Red Metallic", "Dark Red Pearl", "Dark Roasty Espresso Metallic", "Dark Ruby Red Metallic",
    "Dark Saddle Brown", "Dark Sage Metallic", "Dark Sapphire Blue", "Dark Sapphire Blue Metallic", "Dark Slate Blue", "Dark Slate Blue Metallic",
    "Dark Slate Gray", "Dark Slate Gray Metallic", "Dark Slate Metallic", "Dark Slate Pearl", "Dark Slate Pearl Metallic", "Dark Slate Uni",
    "Dark Steel Gray", "Dark Steel Gray Metallic", "Dark Stone Gray", "Dark Stone Gray Metallic", "Dark Titanium", "Dark Titanium Metallic",
    "Dark Titanium Tri-Coat", "Dark Toreador Red", "Dark Toreador Red Metallic", "Dark Tungsten Metallic", "Dark Veil Purple Metallic",
    "Dark Velvet Brown", "Dark Velvet Brown Metallic", "Dark Verdant Green Metallic", "Dark Warm Gray", "Dark Warm Gray Metallic",
    "Dark Warm Metallic", "Dark Warm Taupe", "Dark Warm Taupe Metallic", "Dark Weathered Gray", "Dark Weathered Gray Metallic",
    "Dark Weathered Pewter Metallic", "Dark White", "Dark White Pearl", "Darkening Gray", "Darkening Gray Metallic", "Darkness Black Pearl",
    "Darkness Black Pearl Metallic", "Darkness Obsidian", "Darkness Obsidian Pearl", "Darkness Obsidian Pearl Metallic", "Darkside Gray",
    "Darkside Gray Metallic", "Darkside Pearl", "Darkside Pearl Metallic", "Darkwood Brown", "Darkwood Brown Metallic", "Deep Amethyst",
    "Deep Amethyst Metallic", "Deep Aqua Blue", "Deep Aqua Blue Metallic", "Deep Auburn", "Deep Auburn Metallic", "Deep Azure Blue",
    "Deep Azure Blue Metallic", "Deep Blue", "Deep Blue Metallic", "Deep Blue Pearl", "Deep Blue Uni", "Deep Blueberry", "Deep Blueberry Metallic",
    "Deep Bordeaux", "Deep Bordeaux Metallic", "Deep Briar Brown", "Deep Briar Brown Metallic", "Deep Bronze", "Deep Bronze Metallic",
    "Deep Brown", "Deep Brown Metallic", "Deep Burgundy", "Deep Burgundy Metallic", "Deep Burgundy Pearl", "Deep Burner Orange",
    "Deep Burner Orange Metallic", "Deep Candy Blue", "Deep Candy Blue Metallic", "Deep Canyon Blue", "Deep Canyon Blue Metallic",
    "Deep Carmine Red", "Deep Carmine Red Metallic", "Deep Carmine Toreador Red Metallic", "Deep Cashmere Metallic", "Deep Charcoal",
    "Deep Charcoal Metallic", "Deep Cherry Red", "Deep Cherry Red Metallic", "Deep Chocolate", "Deep Chocolate Brown", "Deep Chocolate Brown Metallic",
    "Deep Chocolate Metallic", "Deep Cinnamon", "Deep Cinnamon Metallic", "Deep Cobalt", "Deep Cobalt Blue", "Deep Cobalt Blue Metallic",
    "Deep Cobalt Metallic", "Deep Coffee", "Deep Coffee Brown", "Deep Coffee Brown Metallic", "Deep Coffee Metallic", "Deep Copper",
    "Deep Copper Metallic", "Deep Cordovan", "Deep Cordovan Red", "Deep Cordovan Red Metallic", "Deep Cordovan Red Pearl", "Deep Cranberry Red",
    "Deep Cranberry Red Metallic", "Deep Cypress Green", "Deep Cypress Green Metallic", "Deep Espresso", "Deep Espresso Brown", "Deep Espresso Brown Metallic",
    "Deep Espresso Metallic", "Deep Ever Green", "Deep Ever Green Metallic", "Deep Forest Green", "Deep Forest Green Metallic", "Deep Garnet Red",
    "Deep Garnet Red Metallic", "Deep Garnet Red Pearl", "Deep Garnish Red", "Deep Garnish Red Metallic", "Deep Garnish Red Pearl", "Deep Gemini Red",
    "Deep Gemini Red Metallic", "Deep Genuine Gray", "Deep Genuine Gray Metallic", "Deep Ginger Metallic", "Deep Gingersnap Metallic",
    "Deep Gloss Black", "Deep Gloss Black Pearl", "Deep Gloss Black Pearl Metallic", "Deep Gloss Black Uni", "Deep Gold Metallic", "Deep Golden Beige",
    "Deep Golden Beige Metallic", "Deep Golden Brown", "Deep Golden Brown Metallic", "Deep Golden Metallic", "Deep Goldenrod", "Deep Goldenrod Metallic",
    "Deep Grape", "Deep Grape Metallic", "Deep Grape Purple", "Deep Grape Purple Metallic", "Deep Grapevine", "Deep Grapevine Metallic",
    "Deep Graphite", "Deep Graphite Metallic", "Deep Graphite Uni", "Deep Gray", "Deep Gray Metallic", "Deep Gray Uni", "Deep Graystone",
    "Deep Graystone Metallic", "Deep Green", "Deep Green Metallic", "Deep Green Uni", "Deep Greystone", "Deep Greystone Metallic",
    "Deep Gunmetal", "Deep Gunmetal Gray", "Deep Gunmetal Gray Metallic", "Deep Gunmetal Metallic", "Deep Hematite", "Deep Hematite Metallic",
    "Deep Hematite Pearl", "Deep Hematite Pearl Metallic", "Deep Highland Blue", "Deep Highland Blue Metallic", "Deep Highland Green",
    "Deep Highland Green Metallic", "Deep Highland Gray", "Deep Highland Gray Metallic", "Deep Highland Metallic", "Deep Highland Red",
    "Deep Highland Red Metallic", "Deep Horizon Blue", "Deep Horizon Blue Metallic", "Deep Hunter Green", "Deep Hunter Green Metallic",
    "Deep Indigo", "Deep Indigo Blue", "Deep Indigo Blue Metallic", "Deep Indigo Metallic", "Deep Indigo Pearl", "Deep Indigo Pearl Metallic",
    "Deep Inferno Orange", "Deep Inferno Orange Metallic", "Deep Inferno Red", "Deep Inferno Red Metallic", "Deep Iris Metallic", "Deep Iris Pearl",
    "Deep Iris Pearl Metallic", "Deep Iron Gray", "Deep Iron Gray Metallic", "Deep Ironstone Gray", "Deep Ironstone Gray Metallic", "Deep Ironwood",
    "Deep Ironwood Metallic", "Deep Ivory", "Deep Ivory Metallic", "Deep Ivy Green", "Deep Ivy Green Metallic", "Deep Jacaranda Purple",
    "Deep Jacaranda Purple Metallic", "Deep Jade Green", "Deep Jade Green Metallic", "Deep Jet Black", "Deep Jet Black Metallic",
    "Deep Jet Black Pearl", "Deep Jet Black Pearl Metallic", "Deep Jewel Blue", "Deep Jewel Blue Metallic", "Deep Jewel Green",
    "Deep Jewel Green Metallic", "Deep Jewel Metallic", "Deep Jewel Purple", "Deep Jewel Purple Metallic", "Deep Jewel Red",
    "Deep Jewel Red Metallic", "Deep Jewel Tone Blue", "Deep Jewel Tone Blue Metallic", "Deep Jewel White", "Deep Jewel White Pearl",
    "Ebony", "Ebony Black", "Ebony Black Pearl", "Ebony Metallic", "Ebony Pearl", "Ebony Twilight", "Eclipse Black", "Eclipse Black Metallic",
    "Eclipse Black Pearl", "Eclipse Metallic", "Ecru", "Ecru Metallic", "Ecru Pearl", "Ecru White", "Ecru White Metallic",
    "Pearl White", "Bright White", "White Diamond Pearl", "Winter White", "Platinum", "Silver", "Graphite", "Gray", "Charcoal",
    "Black", "Jet Black", "Deep Blue Metallic", "Navy Blue", "Midnight Blue Metallic", "Cobalt Blue", "Lagoon Blue Metallic",
    "Ocean Blue", "Blue Pearl", "Caribbean Blue Metallic", "Steel Blue", "Light Blue", "Teal", "Turquoise", "Cyan",
    "Red", "Crimson Red", "Ruby Red", "Deep Red", "Scarlet Red", "Fire Red", "Cherry Red", "Candy Apple Red",
    "Torch Red", "Inferno Orange", "Sunset Orange", "Burnt Orange", "Orange", "Tangerine Orange", "Bright Orange",
    "Yellow", "Pale Yellow", "Light Yellow", "Solar Yellow", "Lemon Yellow", "Golden Yellow", "Mustard Yellow",
    "Brown", "Dark Brown", "Medium Brown", "Light Brown", "Tan", "Caramel", "Chocolate Brown", "Mahogany",
    "Beige", "Cream", "Ivory", "Sand", "Champagne", "Bronze", "Copper", "Rose Gold", "Gold Metallic",
    "Green", "Dark Green", "Forest Green", "Hunter Green", "Olive Green", "Sage Green", "Lime Green", "Neon Green",
    "Teal Green", "Emerald Green", "Sea Green", "Spring Green", "Pistachio Green", "Moss Green"
]

MAKES_BY_YEAR = {
    "Toyota": (1936, 2025), "Honda": (1959, 2025), "Ford": (1908, 2025), "Chevrolet": (1911, 2025),
    "BMW": (1916, 2025), "Mercedes-Benz": (1901, 2025), "Nissan": (1933, 2025), "Hyundai": (1986, 2025),
    "Kia": (1992, 2025), "Jeep": (1941, 2025), "Audi": (1968, 2025), "Lexus": (1989, 2025),
    "Subaru": (1958, 2025), "Mazda": (1960, 2025), "Volvo": (1927, 2025), "Porsche": (1948, 2025),
    "Dodge": (1914, 2025), "GMC": (1912, 2025), "Cadillac": (1902, 2025), "Lincoln": (1917, 2025),
    "Infiniti": (1989, 2025), "Genesis": (2015, 2025), "Chrysler": (1924, 2025), "Tesla": (2008, 2025),
    "Ram": (2010, 2025), "Buick": (1903, 2025), "Acura": (1986, 2025), "Jaguar": (1935, 2025),
    "Land Rover": (1948, 2025), "Mitsubishi": (1917, 2025), "Suzuki": (1955, 2025), "Mini": (1959, 2025),
    "Lamborghini": (1963, 2025), "Ferrari": (1947, 2025), "Maserati": (1926, 2025),
}

MODELS_DATABASE = {
    "Toyota": [("Camry", 1983, 2025), ("Corolla", 1966, 2025), ("RAV4", 1995, 2025), ("Highlander", 2001, 2025), ("Prius", 1997, 2025), ("4Runner", 1984, 2025), ("Sienna", 1997, 2025), ("Tacoma", 1995, 2025), ("Tundra", 1999, 2025)],
    "Honda": [("Accord", 1976, 2025), ("Civic", 1972, 2025), ("CR-V", 1996, 2025), ("Pilot", 2002, 2025), ("Odyssey", 1994, 2025), ("Ridgeline", 2005, 2025)],
    "Ford": [("F-150", 1997, 2025), ("Mustang", 1964, 2025), ("Explorer", 1990, 2025), ("Edge", 2006, 2025), ("Escape", 2000, 2025), ("Ranger", 1983, 2025), ("Bronco", 1966, 2025)],
    "Chevrolet": [("Silverado 1500", 1999, 2025), ("Camaro", 1966, 2025), ("Tahoe", 1995, 2025), ("Traverse", 2008, 2025), ("Malibu", 1964, 2025), ("Equinox", 2004, 2025), ("Colorado", 2004, 2025)],
    "BMW": [("3 Series", 1975, 2025), ("5 Series", 1972, 2025), ("7 Series", 1977, 2025), ("X1", 2009, 2025), ("X3", 2003, 2025), ("X5", 1999, 2025), ("X7", 2018, 2025), ("Z4", 2002, 2025)],
    "Mercedes-Benz": [("C-Class", 1993, 2025), ("E-Class", 1995, 2025), ("S-Class", 1954, 2025), ("GLC", 2015, 2025), ("GLE", 2015, 2025), ("G-Class", 1979, 2025)],
    "Nissan": [("Altima", 1992, 2025), ("Maxima", 1981, 2025), ("Rogue", 2006, 2025), ("Sentra", 1982, 2025), ("Pathfinder", 1986, 2025), ("Murano", 2002, 2025), ("Leaf", 2010, 2025), ("Z", 1969, 2025)],
    "Hyundai": [("Sonata", 1985, 2025), ("Elantra", 1990, 2025), ("Tucson", 2004, 2025), ("Kona", 2017, 2025), ("Santa Fe", 2000, 2025), ("Palisade", 2018, 2025), ("Venue", 2019, 2025)],
    "Kia": [("Sportage", 1995, 2025), ("Sorento", 2002, 2025), ("Forte", 2009, 2025), ("Sedona", 2001, 2025), ("Stinger", 2017, 2025), ("Niro", 2016, 2025), ("Rio", 2000, 2025), ("K5", 2021, 2025)],
    "Jeep": [("Wrangler", 1987, 2025), ("Cherokee", 1974, 2025), ("Grand Cherokee", 1992, 2025), ("Compass", 2006, 2025), ("Renegade", 2014, 2025), ("Gladiator", 2019, 2025)],
    "Audi": [("A3", 1996, 2025), ("A4", 1994, 2025), ("A5", 2007, 2025), ("A6", 1997, 2025), ("A7", 2010, 2025), ("Q3", 2011, 2025), ("Q5", 2008, 2025), ("Q7", 2005, 2025)],
    "Lexus": [("ES", 1989, 2025), ("IS", 1998, 2025), ("GS", 1991, 2025), ("LS", 1989, 2025), ("RX", 1998, 2025), ("NX", 2014, 2025), ("GX", 2002, 2025), ("UX", 2018, 2025), ("LX", 1996, 2025)],
    "Subaru": [("Outback", 1995, 2025), ("Legacy", 1989, 2025), ("Impreza", 1992, 2025), ("Crosstrek", 2012, 2025), ("Forester", 1997, 2025), ("Ascent", 2018, 2025), ("BRZ", 2012, 2025), ("WRX", 2001, 2025)],
    "Mazda": [("Mazda3", 2003, 2025), ("Mazda6", 2002, 2025), ("CX-5", 2012, 2025), ("CX-3", 2013, 2025), ("CX-9", 2006, 2025), ("MX-5 Miata", 1989, 2025), ("CX-30", 2019, 2025), ("CX-50", 2022, 2025), ("Mazda2", 2014, 2025)],
    "Volvo": [("S60", 2000, 2025), ("S90", 2016, 2025), ("XC60", 2008, 2025), ("XC90", 2002, 2025), ("XC40", 2018, 2025)],
    "Porsche": [("911", 1963, 2025), ("Cayenne", 2002, 2025), ("Macan", 2014, 2025), ("Panamera", 2009, 2025), ("Taycan", 2020, 2025)],
    "Dodge": [("Charger", 1966, 2025), ("Challenger", 1970, 2025), ("Durango", 1998, 2025), ("Journey", 2009, 2025), ("Caravan", 1984, 2021)],
    "GMC": [("Sierra 1500", 1999, 2025), ("Yukon", 1992, 2025), ("Acadia", 2007, 2025), ("Canyon", 2015, 2025), ("Terrain", 2010, 2025)],
    "Cadillac": [("CT4", 2019, 2025), ("CT5", 2019, 2025), ("Escalade", 1999, 2025), ("XT4", 2018, 2025), ("XT5", 2016, 2025), ("XT6", 2019, 2025)],
    "Lincoln": [("Aviator", 2019, 2025), ("Corsair", 2019, 2025), ("Navigator", 1997, 2025), ("Continental", 2016, 2020)],
    "Infiniti": [("Q50", 2013, 2025), ("Q60", 2016, 2025), ("QX50", 2018, 2025), ("QX60", 2013, 2025), ("QX80", 2010, 2025), ("Q70", 2013, 2025), ("Q30", 2015, 2022)],
    "Genesis": [("G70", 2017, 2025), ("G80", 2015, 2025), ("G90", 2015, 2025), ("GV60", 2022, 2025), ("GV70", 2021, 2025), ("GV80", 2020, 2025)],
    "Chrysler": [("300", 2004, 2025), ("Pacifica", 2017, 2025), ("Prowler", 1997, 2002)],
    "Tesla": [("Model 3", 2017, 2025), ("Model S", 2012, 2025), ("Model X", 2015, 2025), ("Model Y", 2020, 2025)],
    "Ram": [("1500", 2002, 2025), ("2500", 2010, 2025), ("3500", 2010, 2025)],
    "Buick": [("Regal", 1973, 2025), ("LaCrosse", 2004, 2025), ("Encore", 2012, 2025), ("Enclave", 2007, 2025), ("Envision", 2016, 2025)],
    "Acura": [("ILX", 2013, 2025), ("TLX", 2014, 2025), ("RDX", 2006, 2025), ("MDX", 2001, 2025)],
    "Jaguar": [("F-Type", 2013, 2025), ("XE", 2015, 2025), ("XF", 2008, 2025), ("I-Pace", 2018, 2025)],
    "Land Rover": [("Range Rover", 1970, 2025), ("Range Rover Sport", 2005, 2025), ("Discovery", 1989, 2025), ("Defender", 1948, 2025)],
    "Mitsubishi": [("Outlander", 2002, 2025), ("Mirage", 1978, 2025), ("Lancer", 1973, 2025)],
    "Suzuki": [("Vitara", 1988, 2025), ("Swift", 2004, 2025), ("S-Cross", 2013, 2025)],
    "Mini": [("Cooper", 2001, 2025), ("Clubman", 2007, 2025), ("Countryman", 2010, 2025)],
}

# 150+ MODELS WITH YEAR-SPECIFIC TRIMS
TRIMS_DATABASE = {
    # TOYOTA - 9 models
    ("Toyota", "Camry", "2023-2025"): ["LE", "SE", "XLE", "Limited", "Hybrid LE", "Hybrid SE", "Hybrid XLE", "Hybrid Limited"],
    ("Toyota", "Camry", "2018-2022"): ["LE", "SE", "XLE", "Limited", "SE Hybrid", "XLE Hybrid", "Limited Hybrid"],
    ("Toyota", "Camry", "2012-2017"): ["L", "LE", "SE", "XLE", "Limited", "Hybrid"],
    ("Toyota", "Camry", "2007-2011"): ["CE", "LE", "SE", "XLE", "Limited", "Hybrid"],
    ("Toyota", "Camry", "2000-2006"): ["CE", "LE", "SE", "XLE", "Limited"],
    
    ("Toyota", "Corolla", "2023-2025"): ["L", "LE", "SE", "XLE", "SE Hybrid", "XLE Hybrid", "GR Corolla"],
    ("Toyota", "Corolla", "2017-2022"): ["L", "LE", "S", "SE", "XSE", "XLE", "Hybrid"],
    ("Toyota", "Corolla", "2009-2016"): ["Base", "CE", "LE", "S", "XLE", "Hybrid"],
    ("Toyota", "Corolla", "2003-2008"): ["CE", "LE", "S", "XLE", "XRS"],
    ("Toyota", "Corolla", "1998-2002"): ["CE", "LE", "S", "XLE"],
    
    ("Toyota", "RAV4", "2023-2025"): ["LE", "XLE", "Adventure", "Limited", "Prime LE", "Prime XSE"],
    ("Toyota", "RAV4", "2019-2022"): ["LE", "XLE", "Adventure", "Limited", "TRD", "Hybrid LE", "Hybrid XSE"],
    ("Toyota", "RAV4", "2013-2018"): ["LE", "XLE", "Limited", "SE", "Adventure", "Hybrid"],
    ("Toyota", "RAV4", "2008-2012"): ["Base", "LE", "XLE", "Limited", "V6", "Hybrid"],
    ("Toyota", "RAV4", "2000-2007"): ["Base", "LE", "XLE", "Limited", "V6"],
    
    ("Toyota", "Highlander", "2023-2025"): ["LE", "XLE", "Limited", "Platinum", "Hybrid LE", "Hybrid XLE", "Hybrid Limited"],
    ("Toyota", "Highlander", "2017-2022"): ["L", "LE", "XLE", "Limited", "Platinum", "Hybrid"],
    ("Toyota", "Highlander", "2008-2016"): ["Base", "LE", "XLE", "Limited", "Hybrid"],
    ("Toyota", "Highlander", "2001-2007"): ["Base", "LE", "XLE", "Limited"],
    
    ("Toyota", "Prius", "2023-2025"): ["LE", "XLE", "Limited", "AWD-e", "Prime LE", "Prime XSE"],
    ("Toyota", "Prius", "2015-2022"): ["Two", "Three", "Four", "Five", "Prime", "Prime Plus"],
    ("Toyota", "Prius", "2009-2014"): ["Base", "II", "III", "IV", "V", "Plug-in Hybrid"],
    ("Toyota", "Prius", "2000-2008"): ["Base", "Standard", "Premium"],
    
    ("Toyota", "4Runner", "2023-2025"): ["SR5", "Limited", "Venture Edition", "TRD Off-Road", "TRD Pro"],
    ("Toyota", "4Runner", "2010-2022"): ["SR5", "Limited", "TRD Off-Road", "TRD Pro"],
    ("Toyota", "4Runner", "2003-2009"): ["Base", "SR5", "Limited", "TRD"],
    
    ("Toyota", "Sienna", "2021-2025"): ["LE", "XLE", "Limited", "Platinum"],
    ("Toyota", "Sienna", "2010-2020"): ["LE", "XLE", "Limited", "Platinum", "SE"],
    ("Toyota", "Sienna", "2004-2009"): ["LE", "XLE", "Limited"],
    
    ("Toyota", "Tacoma", "2023-2025"): ["SR5", "Limited", "TRD Sport", "TRD Off-Road", "TRD Pro", "Wilderness"],
    ("Toyota", "Tacoma", "2016-2022"): ["SR", "SR5", "Limited", "TRD Sport", "TRD Off-Road", "TRD Pro"],
    ("Toyota", "Tacoma", "2005-2015"): ["Regular Cab", "Double Cab", "PreRunner", "SR5", "Limited"],
    
    ("Toyota", "Tundra", "2022-2025"): ["SR5", "Limited", "TRD Sport", "TRD Off-Road", "TRD Pro", "Platinum", "1794 Edition"],
    ("Toyota", "Tundra", "2014-2021"): ["Regular Cab", "Double Cab", "CrewMax", "SR5", "Limited", "TRD", "Platinum"],
    ("Toyota", "Tundra", "2007-2013"): ["Regular Cab", "Double Cab", "CrewMax", "SR5", "Limited", "TRD"],
    
    # HONDA - 6 models
    ("Honda", "Accord", "2023-2025"): ["Sport", "EX", "EX-L", "Touring", "Hybrid EX", "Hybrid EX-L", "Hybrid Touring"],
    ("Honda", "Accord", "2018-2022"): ["Sport", "EX", "EX-L", "Touring", "Hybrid", "Hybrid EX", "Hybrid EX-L"],
    ("Honda", "Accord", "2013-2017"): ["LX", "Sport", "EX", "EX-L", "Touring", "Hybrid"],
    ("Honda", "Accord", "2008-2012"): ["LX", "LX-S", "EX", "EX-L", "EX-V6", "Hybrid"],
    ("Honda", "Accord", "2003-2007"): ["DX", "LX", "EX", "EX-V6", "Hybrid"],
    
    ("Honda", "Civic", "2022-2025"): ["LX", "Sport", "EX", "EX-L", "Touring", "Si", "Type R", "Sport Touring"],
    ("Honda", "Civic", "2016-2021"): ["LX", "Sport", "EX", "EX-T", "EX-L", "Touring", "Si", "Type R"],
    ("Honda", "Civic", "2012-2015"): ["LX", "LX-S", "EX", "EX-L", "Si", "Hybrid"],
    ("Honda", "Civic", "2006-2011"): ["DX", "DX-G", "LX", "EX", "EX-L", "Hybrid", "Si"],
    ("Honda", "Civic", "2000-2005"): ["DX", "LX", "EX", "HX", "Si", "Hybrid"],
    
    ("Honda", "CR-V", "2023-2025"): ["LX", "EX", "EX-L", "Touring", "Sport Touring", "Sport Utility"],
    ("Honda", "CR-V", "2017-2022"): ["LX", "EX", "EX-L", "Touring", "Sport Touring"],
    ("Honda", "CR-V", "2012-2016"): ["LX", "EX", "EX-L", "Touring"],
    ("Honda", "CR-V", "2007-2011"): ["LX", "EX", "EX-L", "RE"],
    ("Honda", "CR-V", "2002-2006"): ["LX", "EX", "SE", "SE AWD"],
    
    ("Honda", "Pilot", "2023-2025"): ["LX", "EX", "EX-L", "Touring", "Sport Touring", "Sport Utility"],
    ("Honda", "Pilot", "2016-2022"): ["LX", "EX", "EX-L", "Touring", "Sport Touring"],
    ("Honda", "Pilot", "2009-2015"): ["LX", "EX", "EX-L", "Touring"],
    ("Honda", "Pilot", "2003-2008"): ["LX", "EX", "EX-L"],
    
    ("Honda", "Odyssey", "2023-2025"): ["LX", "EX", "EX-L", "Touring", "Elite"],
    ("Honda", "Odyssey", "2015-2022"): ["LX", "EX", "EX-L", "Touring", "Elite"],
    ("Honda", "Odyssey", "2005-2014"): ["LX", "EX", "EX-L", "Touring"],
    
    ("Honda", "Ridgeline", "2022-2025"): ["RT", "RTS", "RTL", "RTL-E", "Black Edition"],
    ("Honda", "Ridgeline", "2017-2021"): ["RT", "RTS", "RTL", "RTL-E"],
    ("Honda", "Ridgeline", "2006-2016"): ["RT", "RTS", "RTL", "RTL-E"],
    
    # FORD - 7 models
    ("Ford", "F-150", "2023-2025"): ["Regular Cab", "SuperCrew", "SuperCab", "Lariat", "King Ranch", "Platinum", "Limited", "Raptor", "Tremor"],
    ("Ford", "F-150", "2017-2022"): ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat", "King Ranch", "Platinum", "Raptor"],
    ("Ford", "F-150", "2009-2016"): ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat", "King Ranch", "Platinum", "SVT Raptor"],
    ("Ford", "F-150", "2004-2008"): ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat", "King Ranch", "FX4"],
    
    ("Ford", "Mustang", "2023-2025"): ["EcoBoost", "EcoBoost Premium", "GT", "GT Premium", "Mach 1", "Dark Horse", "S650"],
    ("Ford", "Mustang", "2015-2022"): ["EcoBoost", "EcoBoost Premium", "GT", "GT Premium", "Bullitt", "Shelby GT500", "Mach 1"],
    ("Ford", "Mustang", "2005-2014"): ["Base", "Standard", "GT", "GT Premium", "Shelby GT500"],
    ("Ford", "Mustang", "1998-2004"): ["Coupe", "Convertible", "GT Coupe", "GT Convertible", "SVT Cobra"],
    
    ("Ford", "Explorer", "2023-2025"): ["Base", "XLT", "Limited", "ST", "Timberline", "King Ranch", "Platinum"],
    ("Ford", "Explorer", "2016-2022"): ["Base", "XLT", "Limited", "ST"],
    ("Ford", "Explorer", "2011-2015"): ["Base", "XLT", "Limited", "Sport"],
    ("Ford", "Explorer", "2006-2010"): ["XLT", "Limited", "Eddie Bauer", "Sport Trac"],
    
    ("Ford", "Edge", "2023-2025"): ["SE", "SEL", "Limited", "Titanium", "ST"],
    ("Ford", "Edge", "2015-2022"): ["SE", "SEL", "Limited", "Titanium", "Sport"],
    ("Ford", "Edge", "2007-2014"): ["SE", "SEL", "Limited", "Titanium"],
    
    ("Ford", "Escape", "2023-2025"): ["S", "SE", "SEL", "Titanium", "ST-Line"],
    ("Ford", "Escape", "2017-2022"): ["S", "SE", "SEL", "Titanium"],
    ("Ford", "Escape", "2013-2016"): ["S", "SE", "SEL", "Titanium", "EcoBoost"],
    
    ("Ford", "Ranger", "2023-2025"): ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat", "King Ranch"],
    ("Ford", "Ranger", "2019-2022"): ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat"],
    ("Ford", "Ranger", "2011-2018"): ["Regular Cab", "SuperCrew", "SuperCab", "XL", "XLT", "Lariat"],
    
    ("Ford", "Bronco", "2021-2025"): ["Outer Banks", "Black Diamond", "Badlands", "Wildtrak", "Raptor"],
    ("Ford", "Bronco", "1966-1996"): ["Base", "Custom", "XLT"],
    
    # CHEVROLET - 7 models
    ("Chevrolet", "Silverado 1500", "2022-2025"): ["WT", "LT", "RST", "High Country", "LTZ", "Duramax", "SX"],
    ("Chevrolet", "Silverado 1500", "2014-2021"): ["WT", "Reg Cab", "Double Cab", "Crew Cab", "LT", "RST", "High Country"],
    ("Chevrolet", "Silverado 1500", "2007-2013"): ["Regular Cab", "Extended Cab", "Crew Cab", "LS", "LT", "LTZ", "WT"],
    ("Chevrolet", "Silverado 1500", "1999-2006"): ["Regular Cab", "Extended Cab", "Crew Cab", "LS", "LT", "SS"],
    
    ("Chevrolet", "Camaro", "2023-2025"): ["1LT", "2LT", "3LT", "SS", "ZL1"],
    ("Chevrolet", "Camaro", "2016-2022"): ["1LT", "2LT", "3LT", "SS", "ZL1", "COPO"],
    ("Chevrolet", "Camaro", "2010-2015"): ["1LT", "2LT", "SS", "ZL1", "Z/28"],
    ("Chevrolet", "Camaro", "1993-2002"): ["Base", "Z28", "SS"],
    
    ("Chevrolet", "Tahoe", "2023-2025"): ["LS", "LT", "RST", "Premier", "High Country"],
    ("Chevrolet", "Tahoe", "2015-2022"): ["LS", "LT", "RST", "Premier", "High Country"],
    ("Chevrolet", "Tahoe", "2007-2014"): ["LS", "LT", "LTZ"],
    ("Chevrolet", "Tahoe", "1995-2006"): ["Base", "LS", "LT", "Z71"],
    
    ("Chevrolet", "Traverse", "2023-2025"): ["LS", "LT", "RS", "Premier", "High Country"],
    ("Chevrolet", "Traverse", "2018-2022"): ["LS", "LT", "RS", "Premier", "High Country"],
    ("Chevrolet", "Traverse", "2009-2017"): ["LS", "LT", "LTZ"],
    
    ("Chevrolet", "Malibu", "2023-2025"): ["LT", "RS", "Premier"],
    ("Chevrolet", "Malibu", "2016-2022"): ["L", "LS", "LT", "RS", "Premier"],
    ("Chevrolet", "Malibu", "2008-2015"): ["LS", "LT", "LTZ", "Hybrid"],
    
    ("Chevrolet", "Equinox", "2023-2025"): ["LT", "RS", "Premier"],
    ("Chevrolet", "Equinox", "2017-2022"): ["LS", "LT", "Premier"],
    ("Chevrolet", "Equinox", "2010-2016"): ["LS", "LT", "LTZ"],
    
    ("Chevrolet", "Colorado", "2023-2025"): ["WT", "LT", "Z71", "ZR2"],
    ("Chevrolet", "Colorado", "2015-2022"): ["WT", "LT", "Z71", "ZR2"],
    ("Chevrolet", "Colorado", "2004-2014"): ["Regular Cab", "Crew Cab", "LS", "LT", "Z71"],
    
    # BMW - 8 models
    ("BMW", "3 Series", "2023-2025"): ["330i", "330i xDrive", "340i", "340i xDrive", "M340i xDrive", "M3", "M3 Competition"],
    ("BMW", "3 Series", "2019-2022"): ["330i", "330i xDrive", "340i", "M340i xDrive", "M3"],
    ("BMW", "3 Series", "2012-2018"): ["320i", "328i", "340i", "M340i", "328d", "M3"],
    ("BMW", "3 Series", "2006-2011"): ["325i", "328i", "335i", "335d", "M3"],
    ("BMW", "3 Series", "1998-2005"): ["323i", "325i", "325xi", "330i", "M3"],
    
    ("BMW", "5 Series", "2023-2025"): ["530i", "530i xDrive", "540i xDrive", "M550i xDrive", "M5", "M5 Competition"],
    ("BMW", "5 Series", "2017-2022"): ["530i", "530i xDrive", "540i xDrive", "M550i xDrive", "M5"],
    ("BMW", "5 Series", "2011-2016"): ["528i", "535i", "550i", "ActiveHybrid 5", "M5"],
    ("BMW", "5 Series", "2004-2010"): ["525i", "530i", "535i", "550i", "M5"],
    
    ("BMW", "7 Series", "2023-2025"): ["740i", "740i xDrive", "750i xDrive", "M760i xDrive", "M7", "M7 Competition"],
    ("BMW", "7 Series", "2016-2022"): ["740i", "740i xDrive", "750i xDrive", "M760i xDrive", "M7"],
    ("BMW", "7 Series", "2009-2015"): ["735i", "750i", "ActiveHybrid 7", "M7"],
    ("BMW", "7 Series", "2002-2008"): ["745i", "750i", "760i", "M7"],
    
    ("BMW", "X1", "2022-2025"): ["xDrive30i", "sDrive30i", "M40i", "xDrive40i"],
    ("BMW", "X1", "2016-2021"): ["xDrive28i", "sDrive28i", "xDrive35i", "M40i"],
    ("BMW", "X1", "2009-2015"): ["sDrive28i", "xDrive28i", "xDrive35i"],
    
    ("BMW", "X3", "2023-2025"): ["xDrive30i", "sDrive30i", "xDrive40i", "M40i xDrive", "M", "M Competition"],
    ("BMW", "X3", "2017-2022"): ["xDrive30i", "xDrive40i", "M40i xDrive", "M"],
    ("BMW", "X3", "2011-2016"): ["xDrive28i", "xDrive35i", "xDrive50i", "M"],
    
    ("BMW", "X5", "2023-2025"): ["xDrive40i", "xDrive50i", "M50i xDrive", "M60i xDrive", "M", "M Competition"],
    ("BMW", "X5", "2019-2022"): ["xDrive40i", "xDrive50i", "M50i xDrive"],
    ("BMW", "X5", "2014-2018"): ["xDrive35i", "xDrive50i", "xDrive40e", "M"],
    ("BMW", "X5", "2007-2013"): ["xDrive30i", "xDrive35i", "xDrive50i", "M"],
    
    ("BMW", "X7", "2023-2025"): ["xDrive40i", "xDrive50i", "M50i xDrive", "M60i xDrive", "M", "M Competition"],
    ("BMW", "X7", "2019-2022"): ["xDrive40i", "xDrive50i", "M50i xDrive"],
    
    ("BMW", "Z4", "2023-2025"): ["sDrive30i", "M40i", "M440i xDrive", "M"],
    ("BMW", "Z4", "2018-2022"): ["sDrive30i", "M40i xDrive", "M"],
    ("BMW", "Z4", "2009-2016"): ["sDrive28i", "sDrive35i", "xDrive35i", "M"],
    
    # MERCEDES-BENZ - 6 models
    ("Mercedes-Benz", "C-Class", "2022-2025"): ["C300", "C300 4MATIC", "C43 AMG", "C63 AMG", "C63 AMG S E Performance"],
    ("Mercedes-Benz", "C-Class", "2015-2021"): ["C300", "C300 4MATIC", "C300 Cabriolet", "AMG C43", "AMG C63"],
    ("Mercedes-Benz", "C-Class", "2008-2014"): ["C250", "C300", "C300 4MATIC", "C350", "C63 AMG"],
    ("Mercedes-Benz", "C-Class", "2001-2007"): ["C230", "C240", "C280", "C320", "C55 AMG"],
    
    ("Mercedes-Benz", "E-Class", "2023-2025"): ["E350", "E350 4MATIC", "E450", "E53 AMG", "E63 AMG S E Performance"],
    ("Mercedes-Benz", "E-Class", "2017-2022"): ["E300", "E350", "E450", "AMG E53", "AMG E63"],
    ("Mercedes-Benz", "E-Class", "2010-2016"): ["E250", "E350", "E550", "E63 AMG"],
    ("Mercedes-Benz", "E-Class", "2003-2009"): ["E320", "E350", "E550", "E63 AMG"],
    
    ("Mercedes-Benz", "S-Class", "2022-2025"): ["S500", "S580", "AMG S580 e", "AMG S63 e Performance", "Maybach S580"],
    ("Mercedes-Benz", "S-Class", "2014-2021"): ["S450", "S550", "S63 AMG", "Maybach S450", "Maybach S560"],
    ("Mercedes-Benz", "S-Class", "2007-2013"): ["S550", "S63 AMG", "S65 AMG"],
    ("Mercedes-Benz", "S-Class", "1999-2006"): ["S430", "S500", "S600", "S55 AMG"],
    
    ("Mercedes-Benz", "GLC", "2023-2025"): ["GLC300", "GLC300 4MATIC", "GLC300 Cabriolet", "AMG GLC43", "AMG GLC63"],
    ("Mercedes-Benz", "GLC", "2016-2022"): ["GLC300", "GLC300 4MATIC", "AMG GLC43", "AMG GLC63"],
    ("Mercedes-Benz", "GLC", "2015-2019"): ["GLC250d", "GLC300", "GLC300 4MATIC", "AMG GLC43", "AMG GLC63"],
    
    ("Mercedes-Benz", "GLE", "2023-2025"): ["GLE350", "GLE450", "AMG GLE53", "AMG GLE63 S"],
    ("Mercedes-Benz", "GLE", "2016-2022"): ["GLE350d", "GLE450", "AMG GLE53", "AMG GLE63"],
    
    ("Mercedes-Benz", "G-Class", "2023-2025"): ["G550", "G580", "AMG G63", "AMG G63 Edition 55"],
    ("Mercedes-Benz", "G-Class", "2019-2022"): ["G550", "AMG G63"],
    ("Mercedes-Benz", "G-Class", "2012-2018"): ["G550", "G63 AMG", "G65 AMG"],
    
    # NISSAN - 8 models
    ("Nissan", "Altima", "2023-2025"): ["2.5 S", "2.5 SV", "2.5 SL", "2.5 Platinum", "2.5 SR"],
    ("Nissan", "Altima", "2019-2022"): ["S", "SV", "SL", "Platinum", "SR"],
    ("Nissan", "Altima", "2013-2018"): ["2.5 S", "2.5 SV", "2.5 SL", "3.5 SL", "3.5 Platinum"],
    
    ("Nissan", "Rogue", "2023-2025"): ["S", "SV", "SL", "Platinum", "Sport Touring"],
    ("Nissan", "Rogue", "2017-2022"): ["S", "SV", "SL", "Platinum", "Sport Touring"],
    ("Nissan", "Rogue", "2014-2016"): ["S", "SV", "SL", "Platinum"],
    
    ("Nissan", "Sentra", "2023-2025"): ["S", "SV", "SL", "Platinum", "SR"],
    ("Nissan", "Sentra", "2020-2022"): ["S", "SV", "SL", "Platinum"],
    ("Nissan", "Sentra", "2013-2019"): ["FE S", "S", "SV", "SL"],
    
    ("Nissan", "Pathfinder", "2022-2025"): ["S", "SV", "SL", "Platinum", "Rock Creek"],
    ("Nissan", "Pathfinder", "2017-2021"): ["S", "SV", "SL", "Platinum"],
    ("Nissan", "Pathfinder", "2005-2016"): ["S", "SV", "SL", "Platinum"],
    
    ("Nissan", "Murano", "2023-2025"): ["S", "SV", "SL", "Platinum", "SR"],
    ("Nissan", "Murano", "2015-2022"): ["S", "SV", "SL", "Platinum", "Hybrid"],
    
    ("Nissan", "Maxima", "2023-2025"): ["3.5 S", "3.5 SV", "3.5 SL", "3.5 Platinum", "3.5 SR"],
    ("Nissan", "Maxima", "2009-2022"): ["S", "SV", "SL", "Platinum", "SR"],
    
    ("Nissan", "Leaf", "2023-2025"): ["S", "S Plus", "SV", "SV Plus", "SL", "SL Plus"],
    ("Nissan", "Leaf", "2018-2022"): ["S", "SV", "SL", "Plus", "Pro"],
    
    ("Nissan", "Z", "2023-2025"): ["Sport Touring", "Proto Spec", "Edition 240Z", "Nismo"],
    
    # HYUNDAI - 7 models
    ("Hyundai", "Sonata", "2022-2025"): ["SE", "SEL", "Limited", "Ultimate", "SEL Hybrid", "Limited Hybrid"],
    ("Hyundai", "Sonata", "2015-2021"): ["SE", "SEL", "Sport", "Limited", "Ultimate", "Hybrid"],
    ("Hyundai", "Sonata", "2011-2014"): ["GLS", "SE", "Limited", "Hybrid"],
    
    ("Hyundai", "Elantra", "2023-2025"): ["IVT", "SEL", "Limited", "Ultimate", "N"],
    ("Hyundai", "Elantra", "2017-2022"): ["SE", "SEL", "Limited", "Ultimate"],
    ("Hyundai", "Elantra", "2011-2016"): ["GLS", "SE", "Limited", "Sport"],
    
    ("Hyundai", "Tucson", "2023-2025"): ["SE", "SEL", "Limited", "Ultimate", "N Line", "N"],
    ("Hyundai", "Tucson", "2016-2022"): ["SE", "SEL", "Limited", "Ultimate"],
    ("Hyundai", "Tucson", "2010-2015"): ["GLS", "SE", "Limited", "Sport"],
    
    ("Hyundai", "Kona", "2023-2025"): ["SE", "SEL", "Limited", "Ultimate", "N Line", "N"],
    ("Hyundai", "Kona", "2018-2022"): ["SE", "SEL", "Limited", "Ultimate"],
    
    ("Hyundai", "Santa Fe", "2023-2025"): ["SE", "SEL", "Limited", "Ultimate", "Calligraphy"],
    ("Hyundai", "Santa Fe", "2013-2022"): ["GLS", "SE", "Limited", "Ultimate"],
    
    ("Hyundai", "Palisade", "2022-2025"): ["SE", "SEL", "Limited", "Calligraphy"],
    ("Hyundai", "Palisade", "2018-2021"): ["SE", "SEL", "Limited", "Calligraphy"],
    
    ("Hyundai", "Venue", "2022-2025"): ["SE", "SEL", "Limited"],
    ("Hyundai", "Venue", "2019-2021"): ["SE", "SEL", "Limited"],
    
    # KIA - 8 models
    ("Kia", "Sportage", "2023-2025"): ["LX", "S", "EX", "SX", "SX Prestige", "X-Line"],
    ("Kia", "Sportage", "2017-2022"): ["LX", "S", "EX", "SX", "SX Prestige"],
    ("Kia", "Sportage", "2010-2016"): ["LX", "EX", "SX"],
    
    ("Kia", "Sorento", "2023-2025"): ["L", "LX", "S", "EX", "SX"],
    ("Kia", "Sorento", "2016-2022"): ["L", "LX", "S", "EX", "SX"],
    ("Kia", "Sorento", "2003-2015"): ["LX", "EX", "SX"],
    
    ("Kia", "Forte", "2023-2025"): ["FE", "LX", "S", "EX", "GT"],
    ("Kia", "Forte", "2014-2022"): ["LX", "S", "EX", "SX"],
    
    ("Kia", "Sedona", "2022-2025"): ["LX", "S", "EX", "SX", "SX Prestige"],
    ("Kia", "Sedona", "2015-2021"): ["L", "LX", "EX", "SX", "SX Limited"],
    
    ("Kia", "Stinger", "2022-2025"): ["GT-Line", "GT", "GT Limited"],
    ("Kia", "Stinger", "2018-2021"): ["GT-Line", "GT", "GT Limited"],
    
    ("Kia", "Niro", "2023-2025"): ["LX", "S", "EX", "SX", "SX Touring"],
    ("Kia", "Niro", "2016-2022"): ["LX", "EX", "SX", "SX Touring"],
    
    ("Kia", "Rio", "2023-2025"): ["S", "EX", "SX"],
    ("Kia", "Rio", "2012-2022"): ["LX", "EX", "SX"],
    
    ("Kia", "K5", "2021-2025"): ["LX", "S", "EX", "GT", "GT-Line"],
    
    # JEEP - 6 models
    ("Jeep", "Wrangler", "2023-2025"): ["Sport", "Sport S", "Unlimited", "Rubicon", "High Altitude", "Willys", "4xe"],
    ("Jeep", "Wrangler", "2018-2022"): ["Sport", "Sport S", "Unlimited", "Rubicon", "Sahara"],
    ("Jeep", "Wrangler", "2007-2017"): ["Sport", "Unlimited", "Rubicon", "Sahara", "Moab"],
    
    ("Jeep", "Cherokee", "2023-2025"): ["Sport", "Limited", "Trailhawk", "Summit"],
    ("Jeep", "Cherokee", "2014-2022"): ["Sport", "Latitude", "Limited", "Trailhawk"],
    
    ("Jeep", "Grand Cherokee", "2022-2025"): ["Laredo", "Limited", "Trailhawk", "Summit", "Summit Reserve", "Overland"],
    ("Jeep", "Grand Cherokee", "2011-2021"): ["Laredo", "Limited", "Trailhawk", "Summit"],
    ("Jeep", "Grand Cherokee", "1993-2010"): ["Laredo", "Limited", "Overland"],
    
    ("Jeep", "Compass", "2023-2025"): ["Sport", "Limited", "Trailhawk"],
    ("Jeep", "Compass", "2017-2022"): ["Sport", "Latitude", "Limited", "Trailhawk"],
    
    ("Jeep", "Renegade", "2023-2025"): ["Sport", "Limited", "Trailhawk"],
    ("Jeep", "Renegade", "2015-2022"): ["Sport", "Latitude", "Limited", "Trailhawk"],
    
    ("Jeep", "Gladiator", "2020-2025"): ["Sport", "Overland", "Rubicon", "High Altitude", "Mojave"],
    
    # AUDI - 8 models
    ("Audi", "A3", "2022-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "S3", "S3 Prestige"],
    ("Audi", "A3", "2015-2021"): ["Standard", "Premium", "Premium Plus", "Prestige"],
    
    ("Audi", "A4", "2023-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "S4"],
    ("Audi", "A4", "2009-2022"): ["Standard", "Premium", "Premium Plus", "Prestige", "S4"],
    
    ("Audi", "A5", "2020-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "S5"],
    ("Audi", "A5", "2008-2019"): ["Standard", "Premium", "Premium Plus", "Prestige", "S5"],
    
    ("Audi", "A6", "2023-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "S6"],
    ("Audi", "A6", "2012-2022"): ["Standard", "Premium", "Premium Plus", "Prestige", "S6"],
    
    ("Audi", "A7", "2022-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "S7"],
    ("Audi", "A7", "2011-2021"): ["Standard", "Premium", "Premium Plus", "Prestige", "S7"],
    
    ("Audi", "Q3", "2022-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "SQ3"],
    ("Audi", "Q3", "2015-2021"): ["Standard", "Premium", "Premium Plus", "Prestige"],
    
    ("Audi", "Q5", "2022-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "SQ5"],
    ("Audi", "Q5", "2009-2021"): ["Standard", "Premium", "Premium Plus", "Prestige"],
    
    ("Audi", "Q7", "2022-2025"): ["Standard", "Premium", "Premium Plus", "Prestige", "SQ7"],
    ("Audi", "Q7", "2006-2021"): ["Standard", "Premium", "Premium Plus", "Prestige"],
    
    # LEXUS - 9 models
    ("Lexus", "ES", "2022-2025"): ["250", "300h", "350", "F Sport", "Ultra Luxury"],
    ("Lexus", "ES", "2013-2021"): ["250", "300h", "350", "F Sport"],
    
    ("Lexus", "IS", "2021-2025"): ["300", "300h", "350", "F Sport", "500", "F"],
    ("Lexus", "IS", "2014-2020"): ["250", "350", "300h", "F Sport", "F"],
    
    ("Lexus", "GS", "2012-2020"): ["250", "350", "450h", "F Sport"],
    
    ("Lexus", "LS", "2018-2025"): ["500", "500h", "F Sport", "Ultra Luxury"],
    ("Lexus", "LS", "2006-2017"): ["460", "600h", "F Sport"],
    
    ("Lexus", "RX", "2023-2025"): ["350", "350h", "500h", "F Sport", "F Sport Performance"],
    ("Lexus", "RX", "2016-2022"): ["350", "350h", "450h L", "F Sport"],
    
    ("Lexus", "NX", "2022-2025"): ["250", "250h", "350h", "F Sport", "450h+"],
    ("Lexus", "NX", "2015-2021"): ["200t", "300h", "F Sport"],
    
    ("Lexus", "GX", "2020-2025"): ["460", "470", "F Sport", "Ultra Luxury"],
    ("Lexus", "GX", "2003-2019"): ["470", "550h", "460"],
    
    ("Lexus", "LX", "2022-2025"): ["570", "600", "Ultra Luxury"],
    ("Lexus", "LX", "2008-2021"): ["570", "600h"],
    
    ("Lexus", "UX", "2019-2025"): ["200", "250", "250h", "F Sport"],
    
    # Continue with remaining models... (SUBARU, MAZDA, VOLVO, PORSCHE, DODGE, GMC, CADILLAC, etc.)
    # For brevity, I'll add these as simplified but real data
    
    # SUBARU - 8 models
    ("Subaru", "Outback", "2023-2025"): ["Base", "Premium", "Limited", "Onyx XT"],
    ("Subaru", "Outback", "2010-2022"): ["Base", "Premium", "Limited", "XT"],
    
    ("Subaru", "Legacy", "2023-2025"): ["Base", "Premium", "Sport", "Limited", "XT"],
    ("Subaru", "Legacy", "2010-2022"): ["Base", "Premium", "Sport", "Limited"],
    
    ("Subaru", "Impreza", "2023-2025"): ["Base", "Premium", "Sport", "Limited"],
    ("Subaru", "Impreza", "2012-2022"): ["Base", "Premium", "Sport", "Limited", "WRX"],
    
    ("Subaru", "Crosstrek", "2023-2025"): ["Base", "Premium", "Sport", "Limited", "Wilderness"],
    ("Subaru", "Crosstrek", "2013-2022"): ["Base", "Premium", "Sport", "Limited"],
    
    ("Subaru", "Forester", "2023-2025"): ["Base", "Premium", "Sport", "Limited", "Wilderness"],
    ("Subaru", "Forester", "2014-2022"): ["Base", "Premium", "Sport", "Limited"],
    
    ("Subaru", "Ascent", "2019-2025"): ["Base", "Premium", "Limited", "Touring"],
    
    ("Subaru", "BRZ", "2022-2025"): ["Base", "Premium", "Limited", "Limited RA"],
    
    ("Subaru", "WRX", "2022-2025"): ["Base", "Premium", "Limited", "STI"],
    
    # MAZDA - 9 models
    ("Mazda", "Mazda3", "2023-2025"): ["2.5 S", "2.5 Preferred", "2.5 Premium Plus", "2.5 Turbo Premium Plus"],
    ("Mazda", "Mazda3", "2019-2022"): ["Select", "Preferred", "Premium", "Premium Plus"],
    
    ("Mazda", "Mazda6", "2023-2025"): ["2.5 S", "2.5 Preferred", "2.5 Premium", "2.5 Turbo Premium"],
    ("Mazda", "Mazda6", "2014-2022"): ["Sport", "Touring", "Grand Touring"],
    
    ("Mazda", "CX-5", "2023-2025"): ["2.5 S", "2.5 Preferred", "2.5 Premium Plus", "2.5 Turbo Premium Plus"],
    ("Mazda", "CX-5", "2017-2022"): ["Sport", "Touring", "Grand Touring", "Premium Plus"],
    
    ("Mazda", "CX-3", "2023-2025"): ["2.0 S", "2.0 Preferred", "2.0 Premium Plus"],
    ("Mazda", "CX-3", "2016-2022"): ["Sport", "Touring", "Grand Touring"],
    
    ("Mazda", "CX-9", "2023-2025"): ["2.5 S", "2.5 Preferred", "2.5 Premium Plus"],
    ("Mazda", "CX-9", "2016-2022"): ["Sport", "Touring", "Grand Touring"],
    
    ("Mazda", "MX-5 Miata", "2023-2025"): ["Club", "Sport", "Grand Touring", "Grand Touring Reserve"],
    ("Mazda", "MX-5 Miata", "2016-2022"): ["Club", "Sport", "Grand Touring"],
    
    ("Mazda", "CX-30", "2020-2025"): ["2.0 S", "2.0 Preferred", "2.0 Premium Plus"],
    
    ("Mazda", "CX-50", "2023-2025"): ["2.5 S", "2.5 Preferred", "2.5 Premium Plus"],
    
    ("Mazda", "Mazda2", "2022-2025"): ["2.0 S", "2.0 Preferred"],
    
    # VOLVO - 5 models
    ("Volvo", "S60", "2019-2025"): ["T5 Momentum", "T5 R-Design", "T6 Inscription", "T8 Hybrid", "Polestar"],
    ("Volvo", "S60", "2010-2018"): ["T5", "T6", "R-Design", "Inscription"],
    
    ("Volvo", "S90", "2017-2025"): ["T5 Momentum", "T5 R-Design", "T6 Inscription", "T8 Hybrid"],
    
    ("Volvo", "XC60", "2023-2025"): ["T5 Momentum", "T5 R-Design", "T6 Inscription", "T8 Hybrid", "Polestar"],
    ("Volvo", "XC60", "2009-2022"): ["T5", "T6", "R-Design", "Inscription"],
    
    ("Volvo", "XC90", "2016-2025"): ["T5 Momentum", "T5 R-Design", "T6 Inscription", "T8 Hybrid"],
    
    ("Volvo", "XC40", "2018-2025"): ["T5 Momentum", "T5 R-Design", "T8 Hybrid", "Polestar"],
    
    # PORSCHE - 5 models
    ("Porsche", "911", "2022-2025"): ["Carrera", "Carrera 4", "Carrera GTS", "Turbo", "Turbo S", "GT2 RS"],
    ("Porsche", "911", "2012-2021"): ["Carrera", "Carrera 4", "Carrera S", "Turbo", "GT2 RS"],
    
    ("Porsche", "Cayenne", "2023-2025"): ["Base", "S", "Turbo", "E-Hybrid", "Coupe"],
    ("Porsche", "Cayenne", "2011-2022"): ["Base", "S", "Turbo", "Diesel"],
    
    ("Porsche", "Macan", "2023-2025"): ["T", "GTS", "Turbo", "Electric"],
    ("Porsche", "Macan", "2015-2022"): ["Standard", "S", "Turbo"],
    
    ("Porsche", "Panamera", "2017-2025"): ["Base", "4", "4S", "Turbo", "Turbo S"],
    
    ("Porsche", "Taycan", "2020-2025"): ["RWD", "4", "4 Cross Turismo", "Turbo", "Turbo S"],
    
    # DODGE - 5 models
    ("Dodge", "Charger", "2023-2025"): ["SE", "SXT", "R/T", "Daytona", "Super Bee", "SRT"],
    ("Dodge", "Charger", "2006-2022"): ["SE", "SXT", "R/T", "Daytona", "SRT8"],
    
    ("Dodge", "Challenger", "2023-2025"): ["SXT", "R/T", "SRT", "Hellcat", "Jailbreak"],
    ("Dodge", "Challenger", "2008-2022"): ["SE", "SXT", "R/T", "SRT8", "Hellcat"],
    
    ("Dodge", "Durango", "2022-2025"): ["SXT", "Limited", "R/T", "SRT", "Citadel"],
    ("Dodge", "Durango", "1998-2021"): ["SXT", "Limited", "R/T", "SRT8"],
    
    ("Dodge", "Journey", "2009-2023"): ["SE", "SXT", "Crossroad", "Citadel", "R/T"],
    
    ("Dodge", "Caravan", "2005-2021"): ["SE", "SXT", "Limited"],
    
    # GMC - 5 models
    ("GMC", "Sierra 1500", "2023-2025"): ["WT", "Pro", "Pro Trail Boss", "SLE", "SLT", "AT4", "Denali"],
    ("GMC", "Sierra 1500", "2019-2022"): ["WT", "Reg Cab", "Double Cab", "Crew Cab", "SLE", "AT4", "Denali"],
    
    ("GMC", "Yukon", "2023-2025"): ["SLE", "SLT", "AT4", "Denali", "Denali Ultimate"],
    ("GMC", "Yukon", "2015-2022"): ["SLE", "SLT", "Denali"],
    
    ("GMC", "Acadia", "2017-2025"): ["SL", "SLE", "SLT", "Denali"],
    
    ("GMC", "Canyon", "2015-2025"): ["WR", "SLE", "SLT", "AT4", "Denali"],
    
    ("GMC", "Terrain", "2010-2025"): ["SL", "SLE", "SLT", "Denali"],
    
    # CADILLAC - 6 models
    ("Cadillac", "CT4", "2020-2025"): ["Luxury", "Premium Luxury", "Sport", "V-Series"],
    
    ("Cadillac", "CT5", "2020-2025"): ["Luxury", "Premium Luxury", "Sport", "V-Series"],
    
    ("Cadillac", "Escalade", "2021-2025"): ["Standard", "Luxury", "Premium Luxury", "Platinum", "Sport"],
    ("Cadillac", "Escalade", "2015-2020"): ["Luxury", "Premium Luxury", "Platinum"],
    
    ("Cadillac", "XT4", "2019-2025"): ["Luxury", "Premium Luxury", "Sport"],
    
    ("Cadillac", "XT5", "2017-2025"): ["Luxury", "Premium Luxury", "Sport", "Platinum"],
    
    ("Cadillac", "XT6", "2020-2025"): ["Luxury", "Premium Luxury", "Sport", "Platinum"],
    
    # LINCOLN - 4 models
    ("Lincoln", "Aviator", "2020-2025"): ["Standard", "Select", "Reserve", "Grand Touring"],
    
    ("Lincoln", "Corsair", "2020-2025"): ["Standard", "Select", "Reserve", "Grand Touring"],
    
    ("Lincoln", "Navigator", "2018-2025"): ["Standard", "Select", "Reserve", "Black Label"],
    
    ("Lincoln", "Continental", "2017-2020"): ["Standard", "Select", "Reserve", "Black Label"],
    
    # INFINITI - 7 models
    ("Infiniti", "Q50", "2022-2025"): ["Pure", "Luxe", "Sport", "Red Sport 400"],
    ("Infiniti", "Q50", "2014-2021"): ["Base", "Luxe", "Sport", "Red Sport 400"],
    
    ("Infiniti", "Q60", "2017-2025"): ["Pure", "Luxe", "Sport", "Red Sport 400"],
    
    ("Infiniti", "QX50", "2019-2025"): ["Pure", "Luxe", "Sport", "Sensory"],
    
    ("Infiniti", "QX60", "2022-2025"): ["Pure", "Luxe", "Sensory"],
    ("Infiniti", "QX60", "2013-2021"): ["Base", "Luxe", "Sensory"],
    
    ("Infiniti", "QX80", "2018-2025"): ["Monograph", "Sensory", "Luxe"],
    
    ("Infiniti", "Q70", "2014-2019"): ["Base", "Luxury", "Sport", "Hybrid"],
    
    # GENESIS - 6 models
    ("Genesis", "G70", "2021-2025"): ["Standard", "Advanced", "Prestige"],
    ("Genesis", "G70", "2017-2020"): ["Standard", "Advanced", "Prestige"],
    
    ("Genesis", "G80", "2021-2025"): ["Standard", "Advanced", "Prestige", "Sport"],
    ("Genesis", "G80", "2015-2020"): ["3.8", "5.0", "Hybrid", "Sport"],
    
    ("Genesis", "G90", "2018-2025"): ["Standard", "Advanced", "Prestige", "Sport"],
    
    ("Genesis", "GV60", "2023-2025"): ["Standard", "Advanced", "Prestige"],
    
    ("Genesis", "GV70", "2021-2025"): ["Standard", "Advanced", "Prestige"],
    
    ("Genesis", "GV80", "2021-2025"): ["Standard", "Advanced", "Prestige", "Prestige Plus"],
    
    # CHRYSLER - 3 models
    ("Chrysler", "300", "2015-2025"): ["Touring", "Limited", "C", "Platinum"],
    ("Chrysler", "300", "2005-2014"): ["Touring", "Limited", "C", "SRT8"],
    
    ("Chrysler", "Pacifica", "2018-2025"): ["L", "LX", "Limited", "Pinnacle", "Hybrid"],
    ("Chrysler", "Pacifica", "2017"): ["Touring", "Touring-L", "Limited", "Platinum"],
    
    ("Chrysler", "Prowler", "1997-2002"): ["Standard"],
    
    # TESLA - 4 models
    ("Tesla", "Model 3", "2021-2025"): ["RWD", "Long Range", "Performance"],
    ("Tesla", "Model 3", "2018-2020"): ["Standard Range", "Standard Range Plus", "Long Range", "Performance"],
    
    ("Tesla", "Model S", "2021-2025"): ["Long Range", "Plaid", "Plaid+"],
    ("Tesla", "Model S", "2012-2020"): ["60", "75", "75D", "100", "Plaid"],
    
    ("Tesla", "Model X", "2021-2025"): ["Long Range", "Plaid", "Plaid+"],
    ("Tesla", "Model X", "2015-2020"): ["60", "75", "75D", "100", "P100D"],
    
    ("Tesla", "Model Y", "2020-2025"): ["RWD", "Long Range", "Performance"],
    
    # RAM - 3 models
    ("Ram", "1500", "2019-2025"): ["Tradesman", "Lone Star", "Big Horn", "Rebel", "Limited", "Longhorn", "TRX"],
    ("Ram", "1500", "2009-2018"): ["Tradesman", "Rebel", "Big Horn", "Laramie", "Limited", "Longhorn"],
    
    ("Ram", "2500", "2020-2025"): ["Tradesman", "Big Horn", "Power Wagon", "Laramie", "Limited", "Longhorn"],
    ("Ram", "2500", "2003-2019"): ["Power Wagon", "ST", "SLT", "Laramie", "Limited"],
    
    ("Ram", "3500", "2020-2025"): ["Tradesman", "Big Horn", "Laramie", "Limited", "Longhorn"],
    ("Ram", "3500", "2003-2019"): ["ST", "SLT", "Laramie", "Limited"],
}

# TRANSMISSION TYPES BY MODEL/YEAR
TRANSMISSION_DATABASE = {
    ("Toyota", "Camry", "2023-2025"): ["Automatic CVT", "8-Speed Automatic", "Direct Shift CVT"],
    ("Toyota", "Corolla", "2023-2025"): ["CVT", "6-Speed Manual", "8-Speed Automatic"],
    ("Honda", "Accord", "2023-2025"): ["CVT", "10-Speed Automatic"],
    ("Honda", "Civic", "2022-2025"): ["CVT", "6-Speed Manual", "Continuously Variable"],
    ("Ford", "F-150", "2023-2025"): ["10-Speed Automatic", "6-Speed Automatic"],
    ("Chevrolet", "Silverado 1500", "2023-2025"): ["10-Speed Automatic", "8-Speed Automatic"],
    ("BMW", "3 Series", "2023-2025"): ["8-Speed Automatic", "Sport Automatic"],
    ("Mercedes-Benz", "C-Class", "2023-2025"): ["9-Speed Automatic", "Automatic"],
}

# DRIVE TYPES BY MODEL/YEAR
DRIVE_DATABASE = {
    ("Toyota", "Camry", "2023-2025"): ["FWD", "AWD"],
    ("Toyota", "RAV4", "2023-2025"): ["FWD", "AWD", "4WD"],
    ("Toyota", "Corolla", "2023-2025"): ["FWD", "AWD"],
    ("Honda", "Civic", "2022-2025"): ["FWD"],
    ("Honda", "CR-V", "2023-2025"): ["FWD", "AWD"],
    ("Ford", "F-150", "2023-2025"): ["RWD", "4WD"],
    ("Ford", "Explorer", "2023-2025"): ["FWD", "AWD", "4WD"],
    ("Chevrolet", "Silverado 1500", "2023-2025"): ["RWD", "4WD"],
    ("Jeep", "Wrangler", "2023-2025"): ["4WD", "RWD"],
    ("Jeep", "Cherokee", "2023-2025"): ["FWD", "AWD", "4WD"],
    ("BMW", "3 Series", "2023-2025"): ["RWD", "AWD"],
    ("BMW", "X5", "2023-2025"): ["AWD"],
    ("Mercedes-Benz", "C-Class", "2023-2025"): ["RWD", "AWD"],
    ("Nissan", "Altima", "2023-2025"): ["FWD", "AWD"],
    ("Nissan", "Rogue", "2023-2025"): ["FWD", "AWD"],
}

# ENGINE SIZES FOR 150+ MODELS
ENGINE_DATABASE = {
    ("Toyota", "Camry", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Hybrid"],
    ("Toyota", "Camry", "2015-2022"): ["2.5L 4-Cylinder", "2.5L Hybrid", "3.5L V6"],
    ("Toyota", "Corolla", "2023-2025"): ["2.0L 4-Cylinder", "1.8L Hybrid"],
    ("Toyota", "Corolla", "2014-2022"): ["1.8L 4-Cylinder", "1.8L Hybrid"],
    ("Toyota", "RAV4", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Hybrid"],
    ("Toyota", "RAV4", "2013-2022"): ["2.5L 4-Cylinder", "2.5L Hybrid"],
    ("Toyota", "Highlander", "2023-2025"): ["3.5L V6", "2.5L Hybrid"],
    ("Toyota", "Highlander", "2008-2022"): ["2.7L 4-Cylinder", "3.5L V6", "2.5L Hybrid"],
    ("Toyota", "Prius", "2023-2025"): ["1.8L Hybrid", "2.0L Plug-in Hybrid"],
    ("Toyota", "Prius", "2015-2022"): ["1.8L Hybrid", "1.8L Plug-in Hybrid"],
    ("Toyota", "4Runner", "2023-2025"): ["4.0L V6", "3.4L V6"],
    ("Toyota", "4Runner", "2010-2022"): ["4.0L V6"],
    ("Toyota", "Sienna", "2023-2025"): ["3.5L Hybrid"],
    ("Toyota", "Sienna", "2010-2020"): ["3.5L V6", "2.7L 4-Cylinder"],
    ("Toyota", "Tacoma", "2023-2025"): ["3.5L V6", "2.4L Turbo"],
    ("Toyota", "Tacoma", "2016-2022"): ["3.5L V6", "2.7L 4-Cylinder"],
    ("Toyota", "Tundra", "2022-2025"): ["3.5L Twin Turbo V6", "3.4L Twin Turbo V6", "1.7L Electric"],
    ("Toyota", "Tundra", "2014-2021"): ["4.6L V8", "5.7L V8", "3.5L V6"],
    
    ("Honda", "Accord", "2023-2025"): ["1.5L Turbo", "2.0L", "2.0L Hybrid"],
    ("Honda", "Accord", "2018-2022"): ["1.5L Turbo", "2.0L", "3.5L V6"],
    ("Honda", "Civic", "2022-2025"): ["2.0L Turbo", "1.5L Turbo"],
    ("Honda", "Civic", "2016-2021"): ["1.5L Turbo", "2.0L", "1.5L Turbo"],
    ("Honda", "CR-V", "2023-2025"): ["1.5L Turbo", "2.0L Hybrid"],
    ("Honda", "CR-V", "2017-2022"): ["1.5L Turbo", "2.0L"],
    ("Honda", "Pilot", "2023-2025"): ["3.5L V6", "2.0L Hybrid"],
    ("Honda", "Pilot", "2009-2022"): ["3.5L V6"],
    ("Honda", "Odyssey", "2023-2025"): ["3.5L V6"],
    ("Honda", "Odyssey", "2005-2022"): ["3.5L V6", "3.0L V6"],
    ("Honda", "Ridgeline", "2022-2025"): ["3.5L V6"],
    ("Honda", "Ridgeline", "2006-2021"): ["3.5L V6"],
    
    ("Ford", "F-150", "2023-2025"): ["3.3L V6", "5.0L V8", "3.5L EcoBoost", "5.0L EcoBoost", "3.0L PowerBoost Hybrid", "6.8L V10"],
    ("Ford", "F-150", "2017-2022"): ["3.5L EcoBoost", "5.0L V8", "2.7L EcoBoost", "3.3L V6"],
    ("Ford", "Mustang", "2023-2025"): ["2.3L EcoBoost", "5.0L V8"],
    ("Ford", "Mustang", "2015-2022"): ["2.3L EcoBoost", "5.0L V8"],
    ("Ford", "Explorer", "2023-2025"): ["2.3L EcoBoost", "3.0L EcoBoost", "3.3L V6"],
    ("Ford", "Explorer", "2016-2022"): ["2.3L EcoBoost", "3.0L EcoBoost"],
    ("Ford", "Edge", "2023-2025"): ["2.0L EcoBoost", "2.7L EcoBoost", "3.0L EcoBoost"],
    ("Ford", "Edge", "2007-2022"): ["2.7L V6", "3.5L V6", "3.0L EcoBoost"],
    ("Ford", "Escape", "2023-2025"): ["1.5L EcoBoost", "1.6L EcoBoost", "2.5L Hybrid"],
    ("Ford", "Escape", "2017-2022"): ["1.5L EcoBoost", "2.0L EcoBoost"],
    ("Ford", "Ranger", "2023-2025"): ["2.3L EcoBoost", "3.0L EcoBoost", "2.8L EcoBoost"],
    ("Ford", "Ranger", "2019-2022"): ["2.3L EcoBoost", "3.0L EcoBoost"],
    ("Ford", "Bronco", "2021-2025"): ["2.3L EcoBoost", "2.7L EcoBoost", "3.0L EcoBoost"],
    
    ("Chevrolet", "Silverado 1500", "2023-2025"): ["4.3L V6", "5.3L V8", "6.2L V8", "3.0L Turbo Diesel"],
    ("Chevrolet", "Silverado 1500", "2014-2022"): ["4.3L V6", "5.3L V8", "6.2L V8"],
    ("Chevrolet", "Camaro", "2023-2025"): ["2.0L Turbo", "3.6L V6", "6.2L V8"],
    ("Chevrolet", "Camaro", "2010-2022"): ["2.0L Turbo", "3.6L V6", "6.2L V8", "LS3 V8"],
    ("Chevrolet", "Tahoe", "2023-2025"): ["5.3L V8", "6.2L V8", "3.0L Diesel"],
    ("Chevrolet", "Tahoe", "2015-2022"): ["5.3L V8", "6.2L V8"],
    ("Chevrolet", "Traverse", "2023-2025"): ["3.6L V6"],
    ("Chevrolet", "Traverse", "2009-2022"): ["3.6L V6"],
    ("Chevrolet", "Malibu", "2023-2025"): ["1.5L Turbo", "1.6L Turbo"],
    ("Chevrolet", "Malibu", "2016-2022"): ["1.5L Turbo", "1.6L Turbo"],
    ("Chevrolet", "Equinox", "2023-2025"): ["1.5L Turbo", "2.0L Turbo"],
    ("Chevrolet", "Equinox", "2010-2022"): ["2.4L 4-Cylinder", "3.0L V6"],
    ("Chevrolet", "Colorado", "2023-2025"): ["2.7L Turbo", "3.6L V6", "2.8L Turbo Diesel"],
    ("Chevrolet", "Colorado", "2015-2022"): ["2.5L 4-Cylinder", "3.6L V6", "2.8L Turbo Diesel"],
    
    ("BMW", "3 Series", "2023-2025"): ["2.0L Turbo", "3.0L Turbo"],
    ("BMW", "3 Series", "2012-2022"): ["2.0L Turbo", "3.0L Turbo", "2.0L Diesel"],
    ("BMW", "5 Series", "2023-2025"): ["3.0L Turbo", "4.4L Twin Turbo", "2.0L Hybrid"],
    ("BMW", "5 Series", "2011-2022"): ["2.0L Turbo", "3.0L Turbo", "4.4L Twin Turbo"],
    ("BMW", "7 Series", "2023-2025"): ["3.0L Twin Turbo", "4.4L Twin Turbo"],
    ("BMW", "7 Series", "2009-2022"): ["3.0L Twin Turbo", "4.4L Twin Turbo"],
    ("BMW", "X1", "2022-2025"): ["2.0L Turbo"],
    ("BMW", "X1", "2009-2021"): ["2.0L Turbo", "3.0L Turbo"],
    ("BMW", "X3", "2023-2025"): ["2.0L Turbo", "3.0L Turbo"],
    ("BMW", "X3", "2011-2022"): ["2.0L Turbo", "3.0L Turbo", "2.0L Diesel"],
    ("BMW", "X5", "2023-2025"): ["3.0L Twin Turbo", "4.4L Twin Turbo"],
    ("BMW", "X5", "2007-2022"): ["3.0L Turbo", "4.4L Twin Turbo", "3.0L Diesel"],
    ("BMW", "X7", "2019-2025"): ["3.0L Twin Turbo", "4.4L Twin Turbo"],
    ("BMW", "Z4", "2023-2025"): ["2.0L Turbo", "3.0L Twin Turbo"],
    ("BMW", "Z4", "2009-2022"): ["2.0L Turbo", "3.0L Turbo"],
    
    ("Mercedes-Benz", "C-Class", "2022-2025"): ["2.0L Turbo", "2.0L Turbo Hybrid", "4.0L Biturbo"],
    ("Mercedes-Benz", "C-Class", "2015-2021"): ["2.0L Turbo", "2.0L Turbo Diesel", "4.0L Biturbo"],
    ("Mercedes-Benz", "E-Class", "2023-2025"): ["2.0L Turbo", "3.0L Turbo", "3.0L Turbo Hybrid", "4.0L Biturbo"],
    ("Mercedes-Benz", "E-Class", "2010-2022"): ["2.0L Turbo", "3.0L Turbo", "4.0L Biturbo"],
    ("Mercedes-Benz", "S-Class", "2022-2025"): ["3.0L Twin Turbo", "4.0L Biturbo", "5.0L V8 Biturbo"],
    ("Mercedes-Benz", "S-Class", "2014-2021"): ["3.0L Twin Turbo", "4.7L V8 Biturbo", "6.0L V12 Biturbo"],
    ("Mercedes-Benz", "GLC", "2023-2025"): ["2.0L Turbo", "2.0L Turbo Hybrid", "4.0L Biturbo"],
    ("Mercedes-Benz", "GLC", "2015-2022"): ["2.0L Turbo", "2.1L Turbo Diesel", "4.0L Biturbo"],
    ("Mercedes-Benz", "GLE", "2023-2025"): ["2.0L Turbo", "3.0L Turbo", "4.0L Biturbo"],
    ("Mercedes-Benz", "GLE", "2016-2022"): ["2.0L Turbo", "3.0L Turbo", "4.0L Biturbo"],
    ("Mercedes-Benz", "G-Class", "2023-2025"): ["4.0L Biturbo", "4.5L V8 Biturbo"],
    ("Mercedes-Benz", "G-Class", "2012-2022"): ["4.0L Biturbo", "5.5L V8 Biturbo"],
    
    ("Nissan", "Altima", "2023-2025"): ["2.5L 4-Cylinder"],
    ("Nissan", "Altima", "2013-2022"): ["2.5L 4-Cylinder", "3.5L V6"],
    ("Nissan", "Rogue", "2023-2025"): ["2.5L 4-Cylinder"],
    ("Nissan", "Rogue", "2014-2022"): ["2.5L 4-Cylinder"],
    ("Nissan", "Sentra", "2023-2025"): ["2.0L 4-Cylinder"],
    ("Nissan", "Sentra", "2013-2022"): ["1.8L 4-Cylinder"],
    ("Nissan", "Pathfinder", "2022-2025"): ["3.5L V6", "3.5L Hybrid"],
    ("Nissan", "Pathfinder", "2005-2021"): ["3.5L V6"],
    ("Nissan", "Murano", "2023-2025"): ["3.5L V6"],
    ("Nissan", "Murano", "2015-2022"): ["3.5L V6"],
    ("Nissan", "Maxima", "2023-2025"): ["3.5L V6"],
    ("Nissan", "Maxima", "2009-2022"): ["3.5L V6"],
    ("Nissan", "Leaf", "2023-2025"): ["Electric"],
    ("Nissan", "Leaf", "2010-2022"): ["Electric"],
    ("Nissan", "Z", "2023-2025"): ["3.0L Twin Turbo V6"],
    
    ("Hyundai", "Sonata", "2022-2025"): ["2.5L 4-Cylinder", "2.0L Turbo", "2.0L Hybrid"],
    ("Hyundai", "Sonata", "2011-2021"): ["2.0L Turbo", "2.4L 4-Cylinder"],
    ("Hyundai", "Elantra", "2023-2025"): ["2.0L 4-Cylinder", "1.6L Turbo"],
    ("Hyundai", "Elantra", "2011-2022"): ["1.8L 4-Cylinder", "2.0L Turbo"],
    ("Hyundai", "Tucson", "2023-2025"): ["2.5L 4-Cylinder", "1.6L Turbo", "2.0L Hybrid"],
    ("Hyundai", "Tucson", "2010-2022"): ["2.0L Turbo", "2.4L 4-Cylinder"],
    ("Hyundai", "Kona", "2023-2025"): ["2.0L 4-Cylinder", "1.6L Turbo", "2.0L Hybrid"],
    ("Hyundai", "Kona", "2018-2022"): ["2.0L 4-Cylinder", "1.6L Turbo"],
    ("Hyundai", "Santa Fe", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Turbo", "2.0L Turbo Hybrid"],
    ("Hyundai", "Santa Fe", "2013-2022"): ["2.4L 4-Cylinder", "2.0L Turbo"],
    ("Hyundai", "Palisade", "2022-2025"): ["3.8L V6"],
    ("Hyundai", "Palisade", "2018-2021"): ["3.8L V6"],
    ("Hyundai", "Venue", "2022-2025"): ["1.6L 4-Cylinder"],
    ("Hyundai", "Venue", "2019-2021"): ["1.6L 4-Cylinder"],
    
    ("Kia", "Sportage", "2023-2025"): ["2.5L 4-Cylinder", "2.0L Turbo"],
    ("Kia", "Sportage", "2010-2022"): ["2.0L Turbo", "2.4L 4-Cylinder"],
    ("Kia", "Sorento", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Turbo", "3.5L V6"],
    ("Kia", "Sorento", "2003-2022"): ["2.4L 4-Cylinder", "2.0L Turbo", "3.5L V6"],
    ("Kia", "Forte", "2023-2025"): ["2.0L 4-Cylinder", "1.6L Turbo"],
    ("Kia", "Forte", "2009-2022"): ["2.0L 4-Cylinder", "1.6L Turbo", "2.0L Turbo"],
    ("Kia", "Sedona", "2022-2025"): ["3.8L V6"],
    ("Kia", "Sedona", "2001-2021"): ["2.4L 4-Cylinder", "3.8L V6", "3.3L V6"],
    ("Kia", "Stinger", "2022-2025"): ["2.5L Turbo", "3.3L Turbo V6"],
    ("Kia", "Stinger", "2018-2021"): ["2.0L Turbo", "3.3L Turbo V6"],
    ("Kia", "Niro", "2023-2025"): ["2.0L 4-Cylinder", "1.6L Turbo", "1.6L Turbo Hybrid"],
    ("Kia", "Niro", "2016-2022"): ["2.0L 4-Cylinder", "1.6L Turbo Hybrid"],
    ("Kia", "Rio", "2023-2025"): ["1.6L 4-Cylinder"],
    ("Kia", "Rio", "2000-2022"): ["1.4L 4-Cylinder", "1.6L 4-Cylinder"],
    ("Kia", "K5", "2021-2025"): ["1.6L Turbo", "2.5L", "2.5L Turbo Hybrid"],
    
    ("Jeep", "Wrangler", "2023-2025"): ["2.0L Turbo", "3.6L V6", "3.0L EcoDiesel", "3.0L Turbo EcoDiesel"],
    ("Jeep", "Wrangler", "2007-2022"): ["2.5L 4-Cylinder", "3.6L V6", "3.0L EcoDiesel"],
    ("Jeep", "Cherokee", "2023-2025"): ["2.0L Turbo", "3.2L V6", "3.0L EcoDiesel"],
    ("Jeep", "Cherokee", "2014-2022"): ["2.0L Turbo", "3.2L V6", "3.0L EcoDiesel"],
    ("Jeep", "Grand Cherokee", "2022-2025"): ["3.6L V6", "3.0L EcoDiesel", "5.7L V8", "6.2L V8"],
    ("Jeep", "Grand Cherokee", "2011-2021"): ["3.6L V6", "3.0L EcoDiesel", "5.7L V8"],
    ("Jeep", "Compass", "2023-2025"): ["2.0L 4-Cylinder", "1.3L Turbo", "2.0L Hybrid"],
    ("Jeep", "Compass", "2006-2022"): ["2.0L 4-Cylinder", "2.4L 4-Cylinder"],
    ("Jeep", "Renegade", "2023-2025"): ["1.3L Turbo", "2.0L Turbo", "1.3L Turbo Hybrid"],
    ("Jeep", "Renegade", "2015-2022"): ["1.4L Turbo", "2.4L 4-Cylinder"],
    ("Jeep", "Gladiator", "2020-2025"): ["3.6L V6", "3.0L EcoDiesel"],
    
    # Continue with remaining makes (simpl simplified for brevity)
    ("Audi", "A3", "2022-2025"): ["2.0L Turbo"],
    ("Audi", "A4", "2023-2025"): ["2.0L Turbo", "2.9L Twin Turbo V6"],
    ("Audi", "A5", "2020-2025"): ["2.0L Turbo", "3.0L Turbo"],
    ("Audi", "A6", "2023-2025"): ["2.0L Turbo", "3.0L Turbo"],
    ("Audi", "A7", "2022-2025"): ["3.0L Turbo"],
    ("Audi", "Q3", "2022-2025"): ["2.0L Turbo"],
    ("Audi", "Q5", "2022-2025"): ["2.0L Turbo", "3.0L Turbo"],
    ("Audi", "Q7", "2022-2025"): ["2.0L Turbo", "3.0L Turbo"],
    
    ("Lexus", "ES", "2022-2025"): ["2.5L Hybrid", "2.0L Turbo", "3.5L V6"],
    ("Lexus", "IS", "2021-2025"): ["2.0L Turbo", "3.5L V6", "5.0L V8"],
    ("Lexus", "RX", "2023-2025"): ["2.5L Hybrid", "3.5L V6", "2.4L Turbo"],
    ("Lexus", "NX", "2022-2025"): ["2.5L Hybrid", "2.4L Turbo"],
    ("Lexus", "LS", "2018-2025"): ["3.5L Hybrid", "3.5L V6", "5.0L V8"],
    ("Lexus", "GS", "2012-2020"): ["2.5L Hybrid", "3.5L V6"],
    ("Lexus", "GX", "2020-2025"): ["4.6L V8"],
    ("Lexus", "LX", "2022-2025"): ["3.4L Twin Turbo V6", "5.0L V8"],
    ("Lexus", "UX", "2019-2025"): ["2.0L 4-Cylinder", "2.5L Hybrid"],
    
    ("Subaru", "Outback", "2023-2025"): ["2.5L 4-Cylinder", "2.4L Turbo"],
    ("Subaru", "Legacy", "2023-2025"): ["2.5L 4-Cylinder", "2.4L Turbo"],
    ("Subaru", "Impreza", "2023-2025"): ["2.0L 4-Cylinder", "2.0L Turbo"],
    ("Subaru", "Crosstrek", "2023-2025"): ["2.0L 4-Cylinder", "2.5L 4-Cylinder"],
    ("Subaru", "Forester", "2023-2025"): ["2.5L 4-Cylinder", "2.4L Turbo"],
    ("Subaru", "Ascent", "2019-2025"): ["2.4L Turbo"],
    ("Subaru", "BRZ", "2022-2025"): ["2.4L Turbo"],
    ("Subaru", "WRX", "2022-2025"): ["2.4L Turbo"],
    
    ("Mazda", "Mazda3", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Turbo"],
    ("Mazda", "Mazda6", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Turbo"],
    ("Mazda", "CX-5", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Turbo"],
    ("Mazda", "CX-3", "2023-2025"): ["2.0L 4-Cylinder"],
    ("Mazda", "CX-9", "2023-2025"): ["2.5L Turbo"],
    ("Mazda", "MX-5 Miata", "2023-2025"): ["2.0L 4-Cylinder"],
    ("Mazda", "CX-30", "2020-2025"): ["2.0L 4-Cylinder"],
    ("Mazda", "CX-50", "2023-2025"): ["2.5L 4-Cylinder", "2.5L Turbo"],
    ("Mazda", "Mazda2", "2022-2025"): ["1.5L 4-Cylinder"],
    
    ("Volvo", "S60", "2019-2025"): ["2.0L Turbo", "2.0L Twin Turbo Hybrid"],
    ("Volvo", "S90", "2017-2025"): ["2.0L Twin Turbo", "2.0L Twin Turbo Hybrid"],
    ("Volvo", "XC60", "2023-2025"): ["2.0L Turbo", "2.0L Twin Turbo Hybrid"],
    ("Volvo", "XC90", "2016-2025"): ["2.0L Twin Turbo", "2.0L Twin Turbo Hybrid"],
    ("Volvo", "XC40", "2018-2025"): ["2.0L Turbo", "2.0L Twin Turbo Hybrid"],
    
    ("Porsche", "911", "2022-2025"): ["3.0L Twin Turbo", "3.8L Twin Turbo", "2.9L Twin Turbo"],
    ("Porsche", "911", "2012-2021"): ["3.4L 6-Cylinder", "3.8L 6-Cylinder"],
    ("Porsche", "Cayenne", "2023-2025"): ["3.0L Turbo", "4.0L Twin Turbo", "3.0L Turbo Hybrid"],
    ("Porsche", "Cayenne", "2011-2022"): ["3.6L V6", "4.8L Twin Turbo V8", "3.0L Turbo Diesel"],
    ("Porsche", "Macan", "2023-2025"): ["2.0L Turbo", "2.9L Twin Turbo", "3.0L Turbo", "Electric"],
    ("Porsche", "Macan", "2015-2022"): ["2.0L Turbo", "3.0L V6", "3.6L V6"],
    ("Porsche", "Panamera", "2017-2025"): ["2.9L Twin Turbo", "4.0L Twin Turbo", "2.9L Twin Turbo Hybrid"],
    ("Porsche", "Taycan", "2020-2025"): ["Electric", "Dual Electric"],
    
    ("Dodge", "Charger", "2023-2025"): ["3.6L V6", "5.7L V8", "6.4L V8", "6.2L V8 Supercharged"],
    ("Dodge", "Charger", "2006-2022"): ["2.7L V6", "3.6L V6", "5.7L V8", "6.4L V8"],
    ("Dodge", "Challenger", "2023-2025"): ["3.6L V6", "5.7L V8", "6.2L V8 Supercharged"],
    ("Dodge", "Challenger", "2008-2022"): ["3.5L V6", "5.7L V8", "6.4L V8", "6.2L V8"],
    ("Dodge", "Durango", "2022-2025"): ["3.6L V6", "5.7L V8", "6.4L V8"],
    ("Dodge", "Durango", "1998-2021"): ["3.7L V6", "4.7L V8", "5.7L V8"],
    ("Dodge", "Journey", "2009-2023"): ["2.4L 4-Cylinder", "3.5L V6", "3.6L V6"],
    ("Dodge", "Caravan", "2005-2021"): ["2.4L 4-Cylinder", "3.3L V6", "3.6L V6"],
    
    ("GMC", "Sierra 1500", "2023-2025"): ["4.3L V6", "5.3L V8", "6.2L V8", "3.0L Turbo Diesel"],
    ("GMC", "Sierra 1500", "2019-2022"): ["4.3L V6", "5.3L V8", "6.2L V8"],
    ("GMC", "Yukon", "2023-2025"): ["5.3L V8", "6.2L V8", "3.0L Turbo Diesel"],
    ("GMC", "Yukon", "2015-2022"): ["5.3L V8", "6.2L V8"],
    ("GMC", "Acadia", "2017-2025"): ["3.6L V6"],
    ("GMC", "Canyon", "2015-2025"): ["2.8L Turbo Diesel", "3.6L V6", "2.7L Turbo"],
    ("GMC", "Terrain", "2010-2025"): ["2.4L 4-Cylinder", "2.0L Turbo", "3.0L V6"],
    
    ("Cadillac", "CT4", "2020-2025"): ["2.0L Turbo", "3.0L Twin Turbo"],
    ("Cadillac", "CT5", "2020-2025"): ["2.0L Turbo", "3.0L Twin Turbo", "3.6L V6"],
    ("Cadillac", "Escalade", "2021-2025"): ["5.7L V8", "6.2L V8"],
    ("Cadillac", "Escalade", "2015-2020"): ["5.7L V8", "6.2L V8"],
    ("Cadillac", "XT4", "2019-2025"): ["2.0L Turbo"],
    ("Cadillac", "XT5", "2017-2025"): ["2.0L Turbo", "3.6L V6"],
    ("Cadillac", "XT6", "2020-2025"): ["3.6L V6"],
    
    ("Lincoln", "Aviator", "2020-2025"): ["3.0L EcoBoost", "3.0L EcoBoost Hybrid"],
    ("Lincoln", "Corsair", "2020-2025"): ["2.0L EcoBoost", "2.3L EcoBoost", "2.0L EcoBoost Hybrid"],
    ("Lincoln", "Navigator", "2018-2025"): ["3.5L EcoBoost", "3.5L EcoBoost Hybrid"],
    ("Lincoln", "Continental", "2017-2020"): ["2.7L EcoBoost", "3.0L Twin Turbo"],
    
    ("Infiniti", "Q50", "2022-2025"): ["2.0L Turbo", "3.0L Twin Turbo"],
    ("Infiniti", "Q50", "2014-2021"): ["2.0L Turbo", "3.7L V6", "3.5L V6 Hybrid"],
    ("Infiniti", "Q60", "2017-2025"): ["2.0L Turbo", "3.0L Twin Turbo"],
    ("Infiniti", "QX50", "2019-2025"): ["2.0L Turbo", "2.0L Turbo Hybrid"],
    ("Infiniti", "QX60", "2022-2025"): ["2.0L Turbo", "2.0L Turbo Hybrid"],
    ("Infiniti", "QX60", "2013-2021"): ["3.5L V6", "2.5L Hybrid"],
    ("Infiniti", "QX80", "2018-2025"): ["5.6L V8"],
    ("Infiniti", "Q70", "2014-2019"): ["3.5L V6", "2.5L Hybrid", "3.7L V6"],
    
    ("Genesis", "G70", "2021-2025"): ["2.0L Turbo", "3.3L Twin Turbo"],
    ("Genesis", "G70", "2017-2020"): ["2.0L Turbo", "3.3L Twin Turbo"],
    ("Genesis", "G80", "2021-2025"): ["2.5L Turbo", "3.5L Twin Turbo", "2.0L Hybrid"],
    ("Genesis", "G80", "2015-2020"): ["3.8L V6", "5.0L V8", "2.0L Turbo Hybrid"],
    ("Genesis", "G90", "2018-2025"): ["3.3L Twin Turbo", "5.0L V8", "3.3L Twin Turbo Hybrid"],
    ("Genesis", "GV60", "2023-2025"): ["Electric"],
    ("Genesis", "GV70", "2021-2025"): ["2.5L Turbo", "3.5L Twin Turbo", "2.0L Turbo Hybrid"],
    ("Genesis", "GV80", "2021-2025"): ["2.5L Turbo", "3.5L Twin Turbo", "2.0L Turbo Hybrid"],
    
    ("Chrysler", "300", "2015-2025"): ["3.6L V6", "5.7L V8", "6.4L V8"],
    ("Chrysler", "300", "2005-2014"): ["2.7L V6", "3.5L V6", "5.7L V8"],
    ("Chrysler", "Pacifica", "2018-2025"): ["3.6L V6", "3.6L V6 Hybrid"],
    ("Chrysler", "Pacifica", "2017"): ["3.6L V6"],
    ("Chrysler", "Prowler", "1997-2002"): ["3.5L V6"],
    
    ("Tesla", "Model 3", "2021-2025"): ["Electric", "Dual Electric"],
    ("Tesla", "Model 3", "2018-2020"): ["Electric"],
    ("Tesla", "Model S", "2021-2025"): ["Electric", "Dual Electric"],
    ("Tesla", "Model S", "2012-2020"): ["Electric"],
    ("Tesla", "Model X", "2021-2025"): ["Electric", "Dual Electric"],
    ("Tesla", "Model X", "2015-2020"): ["Electric"],
    ("Tesla", "Model Y", "2020-2025"): ["Electric", "Dual Electric"],
    
    ("Ram", "1500", "2019-2025"): ["3.6L V6", "5.7L V8", "6.4L V8", "3.0L EcoDiesel", "3.0L Twin Turbo EcoDiesel"],
    ("Ram", "1500", "2009-2018"): ["3.7L V6", "4.7L V8", "5.7L V8", "3.0L EcoDiesel"],
    ("Ram", "2500", "2020-2025"): ["6.7L Cummins Diesel", "6.4L V8"],
    ("Ram", "2500", "2003-2019"): ["5.7L V8", "6.7L Cummins Diesel"],
    ("Ram", "3500", "2020-2025"): ["6.7L Cummins Diesel", "6.4L V8"],
    ("Ram", "3500", "2003-2019"): ["5.7L V8", "6.7L Cummins Diesel"],
}

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
    year_int = int(year or "2024")
    for (m, mo, year_range), trims in TRIMS_DATABASE.items():
        if m == make and mo == model:
            try:
                start, end = map(int, year_range.split("-"))
                if start <= year_int <= end:
                    return trims
            except:
                pass
    return ["Standard", "Premium", "Limited", "Sport"]

@app.get("/api/cars/engines")
def get_engines(make: str, model: str, year: str = None):
    year_int = int(year or "2024")
    for (m, mo, year_range), engines in ENGINE_DATABASE.items():
        if m == make and mo == model:
            try:
                start, end = map(int, year_range.split("-"))
                if start <= year_int <= end:
                    return engines
            except:
                pass
    return ["Standard", "Turbo", "Hybrid"]

@app.get("/api/cars/colors")
def get_colors():
    return COLORS

@app.get("/api/cars/decode-vin")
def decode_vin(vin: str):
    """
    Decode VIN using NHTSA API with comprehensive error handling
    """
    try:
        # Normalize and validate VIN - handle None/empty
        if not vin or not isinstance(vin, str):
            return {"error": "VIN is required"}
        
        vin = vin.strip().upper()
        
        if not vin:
            return {"error": "VIN is required"}
        
        if len(vin) != 17:
            return {"error": f"Invalid VIN - must be exactly 17 characters (got {len(vin)})"}
        
        # VIN standard excludes I, O, Q
        if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", vin):
            return {"error": "Invalid VIN - contains invalid characters (I, O, Q not allowed in VINs)"}
        
        logger.info(f"[VIN Decode] Processing: {vin}")
        
        # Call NHTSA API
        try:
            url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    results = data.get("Results", [])
                    
                    if not results:
                        logger.warning(f"[VIN Decode] No results returned from NHTSA for: {vin}")
                        return {"error": "VIN not found in NHTSA database"}
                    
                    # Extract relevant fields
                    decoded = {
                        "vin": vin,
                        "year": None,
                        "make": None,
                        "model": None,
                        "fuelType": None,
                        "bodyClass": None,
                        "series": None
                    }
                    
                    for r in results:
                        if not r or not isinstance(r, dict):
                            continue
                        
                        var = r.get("Variable") or ""
                        val = r.get("Value") or ""
                        
                        if not var or not val:
                            continue
                        
                        var = str(var).strip()
                        val = str(val).strip()
                        
                        if var == "Model Year":
                            decoded["year"] = val
                        elif var == "Make":
                            decoded["make"] = val
                        elif var == "Model":
                            decoded["model"] = val
                        elif var == "Body Class":
                            decoded["bodyClass"] = val
                        elif var == "Series":
                            decoded["series"] = val
                        elif var == "Fuel Type - Primary":
                            fuel_lower = val.lower()
                            if "gasoline" in fuel_lower:
                                decoded["fuelType"] = "Gasoline"
                            elif "diesel" in fuel_lower:
                                decoded["fuelType"] = "Diesel"
                            elif "hybrid" in fuel_lower:
                                decoded["fuelType"] = "Hybrid"
                            elif "electric" in fuel_lower or "ev" in fuel_lower:
                                decoded["fuelType"] = "Electric"
                            elif "methanol" in fuel_lower:
                                decoded["fuelType"] = "Methanol"
                            elif "ethanol" in fuel_lower or "e85" in fuel_lower:
                                decoded["fuelType"] = "Ethanol (E85)"
                            elif "lpg" in fuel_lower or "propane" in fuel_lower:
                                decoded["fuelType"] = "LPG/Propane"
                            elif "cng" in fuel_lower:
                                decoded["fuelType"] = "CNG"
                            else:
                                decoded["fuelType"] = val
                    
                    # Verify we got the essential data
                    if decoded["year"] and decoded["make"] and decoded["model"]:
                        logger.info(f"[VIN Decode] Success: {decoded['year']} {decoded['make']} {decoded['model']}")
                        # Remove None values before returning
                        return {k: v for k, v in decoded.items() if v is not None}
                    else:
                        logger.warning(f"[VIN Decode] Incomplete data for {vin}")
                        return {"error": "VIN decoded but missing required fields (year/make/model)"}
                
                except ValueError as e:
                    logger.error(f"[VIN Decode] JSON parse error: {str(e)}")
                    return {"error": "VIN decoder response format error"}
            
            elif response.status_code == 400:
                logger.warning(f"[VIN Decode] Bad VIN: {vin}")
                return {"error": "Invalid VIN format for NHTSA database"}
            
            else:
                logger.error(f"[VIN Decode] API returned status {response.status_code}")
                return {"error": f"NHTSA API error (status {response.status_code}) - Try again"}
        
        except requests.Timeout:
            logger.error(f"[VIN Decode] Timeout for {vin}")
            return {"error": "VIN decoder timeout - NHTSA service is slow, try again"}
        
        except requests.ConnectionError as e:
            logger.error(f"[VIN Decode] Connection error: {str(e)[:100]}")
            return {"error": "Cannot reach VIN decoder service - Check internet connection"}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"[VIN Decode] Request error: {str(e)[:100]}")
            return {"error": "VIN decoder service error - Please try again"}
    
    except Exception as e:
        logger.error(f"[VIN Decode] Unexpected error: {str(e)[:100]}")
        return {"error": "VIN decoder error - Please contact support"}

@app.get("/api/cars/transmissions")
def get_transmissions(make: str, model: str, year: str = None):
    year_int = int(year or "2024")
    key = (make, model, f"{year_int}-{year_int+1}")
    for (m, mo, year_range), trans in TRANSMISSION_DATABASE.items():
        if m == make and mo == model:
            try:
                start, end = map(int, year_range.split("-"))
                if start <= year_int <= end:
                    return trans
            except:
                pass
    return ["Automatic", "Manual", "CVT"]

@app.get("/api/cars/drivetypes")
def get_drive_types(make: str, model: str, year: str = None):
    year_int = int(year or "2024")
    key = (make, model, f"{year_int}-{year_int+1}")
    for (m, mo, year_range), drives in DRIVE_DATABASE.items():
        if m == make and mo == model:
            try:
                start, end = map(int, year_range.split("-"))
                if start <= year_int <= end:
                    return drives
            except:
                pass
    return ["FWD", "RWD", "AWD", "4WD"]

@app.post("/api/leads/webhook/lead_received")
def lead_received(lead: LeadData):
    try:
        errors = {}
        if lead.mileage and (lead.mileage < 0 or lead.mileage > 999999):
            errors["mileage"] = "Mileage must be between 0 and 999,999 miles"
        if lead.askingPrice and (lead.askingPrice <= 0 or lead.askingPrice > 999999):
            errors["askingPrice"] = "Price must be between $1 and $999,999"
        
        if errors:
            return {"success": False, "errors": errors}
        
        lead_id = f"LEAD_{lead.vin[:8] if lead.vin else 'NO_VIN'}"
        return {
            "success": True,
            "listing_id": lead_id,
            "ai_draft_offer": {"fair": 24500, "low": 22000, "max": 27000},
            "message": "Listing received successfully"
        }
    except Exception as e:
        return {"error": str(e)}
