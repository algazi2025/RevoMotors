"""
Car Database API - Provides comprehensive vehicle information
Supports: Makes, Models, Trims, Years, Body Types, etc.
"""

from fastapi import APIRouter, Query
from typing import List, Optional
import json

router = APIRouter()

# Comprehensive car database
# In production, this would come from a real database or external API like NHTSA, Edmunds, etc.
CAR_DATABASE = {
    "Honda": {
        "models": {
            "Accord": {
                "years": list(range(1990, 2026)),
                "trims": ["LX", "Sport", "EX", "EX-L", "Touring"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic", "Manual", "CVT"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Civic": {
                "years": list(range(1990, 2026)),
                "trims": ["LX", "Sport", "EX", "EX-L", "Touring", "Si", "Type R"],
                "body_types": ["Sedan", "Coupe", "Hatchback"],
                "transmissions": ["Automatic", "Manual", "CVT"],
                "fuel_types": ["Gasoline"]
            },
            "CR-V": {
                "years": list(range(1997, 2026)),
                "trims": ["LX", "EX", "EX-L", "Touring"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic", "CVT"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Pilot": {
                "years": list(range(2003, 2026)),
                "trims": ["LX", "EX", "EX-L", "Touring", "Elite"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline"]
            },
            "Odyssey": {
                "years": list(range(1995, 2026)),
                "trims": ["LX", "EX", "EX-L", "Touring", "Elite"],
                "body_types": ["Minivan"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline"]
            }
        }
    },
    "Toyota": {
        "models": {
            "Camry": {
                "years": list(range(1990, 2026)),
                "trims": ["LE", "SE", "XLE", "XSE", "TRD"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Corolla": {
                "years": list(range(1990, 2026)),
                "trims": ["L", "LE", "SE", "XLE", "XSE"],
                "body_types": ["Sedan", "Hatchback"],
                "transmissions": ["Automatic", "Manual", "CVT"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "RAV4": {
                "years": list(range(1996, 2026)),
                "trims": ["LE", "XLE", "XLE Premium", "Adventure", "TRD Off-Road", "Limited"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Highlander": {
                "years": list(range(2001, 2026)),
                "trims": ["L", "LE", "XLE", "Limited", "Platinum"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Tacoma": {
                "years": list(range(1995, 2026)),
                "trims": ["SR", "SR5", "TRD Sport", "TRD Off-Road", "Limited", "TRD Pro"],
                "body_types": ["Pickup Truck"],
                "transmissions": ["Automatic", "Manual"],
                "fuel_types": ["Gasoline"]
            }
        }
    },
    "Ford": {
        "models": {
            "F-150": {
                "years": list(range(1990, 2026)),
                "trims": ["XL", "XLT", "Lariat", "King Ranch", "Platinum", "Limited", "Raptor"],
                "body_types": ["Pickup Truck"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid", "Electric"]
            },
            "Mustang": {
                "years": list(range(1990, 2026)),
                "trims": ["EcoBoost", "GT", "Mach 1", "Shelby GT500"],
                "body_types": ["Coupe", "Convertible"],
                "transmissions": ["Automatic", "Manual"],
                "fuel_types": ["Gasoline"]
            },
            "Explorer": {
                "years": list(range(1991, 2026)),
                "trims": ["Base", "XLT", "Limited", "ST", "Platinum"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Escape": {
                "years": list(range(2001, 2026)),
                "trims": ["S", "SE", "SEL", "Titanium"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid"]
            }
        }
    },
    "Chevrolet": {
        "models": {
            "Silverado 1500": {
                "years": list(range(1999, 2026)),
                "trims": ["WT", "Custom", "LT", "RST", "LTZ", "High Country"],
                "body_types": ["Pickup Truck"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Diesel"]
            },
            "Malibu": {
                "years": list(range(1997, 2026)),
                "trims": ["L", "LS", "LT", "Premier"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid"]
            },
            "Equinox": {
                "years": list(range(2005, 2026)),
                "trims": ["L", "LS", "LT", "Premier"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline"]
            },
            "Tahoe": {
                "years": list(range(1995, 2026)),
                "trims": ["LS", "LT", "RST", "Z71", "Premier", "High Country"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline"]
            }
        }
    },
    "Nissan": {
        "models": {
            "Altima": {
                "years": list(range(1993, 2026)),
                "trims": ["S", "SV", "SR", "SL", "Platinum"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic", "CVT"],
                "fuel_types": ["Gasoline"]
            },
            "Rogue": {
                "years": list(range(2008, 2026)),
                "trims": ["S", "SV", "SL", "Platinum"],
                "body_types": ["SUV"],
                "transmissions": ["CVT"],
                "fuel_types": ["Gasoline"]
            },
            "Sentra": {
                "years": list(range(1990, 2026)),
                "trims": ["S", "SV", "SR"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic", "Manual", "CVT"],
                "fuel_types": ["Gasoline"]
            }
        }
    },
    "BMW": {
        "models": {
            "3 Series": {
                "years": list(range(1990, 2026)),
                "trims": ["330i", "M340i", "M3"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic", "Manual"],
                "fuel_types": ["Gasoline"]
            },
            "X5": {
                "years": list(range(2000, 2026)),
                "trims": ["sDrive40i", "xDrive40i", "M50i"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Hybrid", "Diesel"]
            }
        }
    },
    "Mercedes-Benz": {
        "models": {
            "C-Class": {
                "years": list(range(1993, 2026)),
                "trims": ["C 300", "C 43 AMG", "C 63 AMG"],
                "body_types": ["Sedan"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline"]
            },
            "GLE": {
                "years": list(range(1998, 2026)),
                "trims": ["GLE 350", "GLE 450", "AMG GLE 53", "AMG GLE 63"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Diesel", "Hybrid"]
            }
        }
    },
    "Tesla": {
        "models": {
            "Model 3": {
                "years": list(range(2017, 2026)),
                "trims": ["Standard Range Plus", "Long Range", "Performance"],
                "body_types": ["Sedan"],
                "transmissions": ["Single-Speed Automatic"],
                "fuel_types": ["Electric"]
            },
            "Model Y": {
                "years": list(range(2020, 2026)),
                "trims": ["Long Range", "Performance"],
                "body_types": ["SUV"],
                "transmissions": ["Single-Speed Automatic"],
                "fuel_types": ["Electric"]
            },
            "Model S": {
                "years": list(range(2012, 2026)),
                "trims": ["Long Range", "Plaid"],
                "body_types": ["Sedan"],
                "transmissions": ["Single-Speed Automatic"],
                "fuel_types": ["Electric"]
            }
        }
    },
    "Jeep": {
        "models": {
            "Wrangler": {
                "years": list(range(1990, 2026)),
                "trims": ["Sport", "Sport S", "Sahara", "Rubicon"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic", "Manual"],
                "fuel_types": ["Gasoline", "Diesel", "Hybrid"]
            },
            "Grand Cherokee": {
                "years": list(range(1993, 2026)),
                "trims": ["Laredo", "Limited", "Overland", "Summit", "SRT", "Trackhawk"],
                "body_types": ["SUV"],
                "transmissions": ["Automatic"],
                "fuel_types": ["Gasoline", "Diesel"]
            }
        }
    },
    "Subaru": {
        "models": {
            "Outback": {
                "years": list(range(1995, 2026)),
                "trims": ["Base", "Premium", "Limited", "Touring", "Wilderness"],
                "body_types": ["Wagon"],
                "transmissions": ["CVT"],
                "fuel_types": ["Gasoline"]
            },
            "Forester": {
                "years": list(range(1998, 2026)),
                "trims": ["Base", "Premium", "Sport", "Limited", "Touring"],
                "body_types": ["SUV"],
                "transmissions": ["CVT"],
                "fuel_types": ["Gasoline"]
            }
        }
    }
}

@router.get("/makes")
def get_all_makes():
    """Get all available car makes"""
    makes = sorted(list(CAR_DATABASE.keys()))
    return {"makes": makes}

@router.get("/models")
def get_models_by_make(make: str = Query(..., description="Car make")):
    """Get all models for a specific make"""
    make_data = CAR_DATABASE.get(make)
    if not make_data:
        return {"models": []}
    
    models = sorted(list(make_data["models"].keys()))
    return {"make": make, "models": models}

@router.get("/trims")
def get_trims_by_model(
    make: str = Query(..., description="Car make"),
    model: str = Query(..., description="Car model")
):
    """Get all trims for a specific make/model"""
    make_data = CAR_DATABASE.get(make, {})
    model_data = make_data.get("models", {}).get(model, {})
    
    return {
        "make": make,
        "model": model,
        "trims": model_data.get("trims", [])
    }

@router.get("/years")
def get_years_by_model(
    make: str = Query(..., description="Car make"),
    model: str = Query(..., description="Car model")
):
    """Get all available years for a specific make/model"""
    make_data = CAR_DATABASE.get(make, {})
    model_data = make_data.get("models", {}).get(model, {})
    
    years = model_data.get("years", [])
    years.sort(reverse=True)  # Most recent first
    
    return {
        "make": make,
        "model": model,
        "years": years
    }

@router.get("/details")
def get_vehicle_details(
    make: str = Query(..., description="Car make"),
    model: str = Query(..., description="Car model")
):
    """Get all details (trims, years, body types, etc.) for a specific make/model"""
    make_data = CAR_DATABASE.get(make, {})
    model_data = make_data.get("models", {}).get(model, {})
    
    if not model_data:
        return {"error": "Vehicle not found"}
    
    years = model_data.get("years", [])
    years.sort(reverse=True)
    
    return {
        "make": make,
        "model": model,
        "years": years,
        "trims": model_data.get("trims", []),
        "body_types": model_data.get("body_types", []),
        "transmissions": model_data.get("transmissions", []),
        "fuel_types": model_data.get("fuel_types", [])
    }

@router.get("/search")
def search_vehicles(query: str = Query(..., min_length=2)):
    """Search for vehicles by make or model name"""
    query_lower = query.lower()
    results = []
    
    for make, make_data in CAR_DATABASE.items():
        # Check if make matches
        if query_lower in make.lower():
            for model in make_data["models"].keys():
                results.append({
                    "make": make,
                    "model": model,
                    "label": f"{make} {model}"
                })
        else:
            # Check if model matches
            for model in make_data["models"].keys():
                if query_lower in model.lower():
                    results.append({
                        "make": make,
                        "model": model,
                        "label": f"{make} {model}"
                    })
    
    return {"results": results[:20]}  # Limit to 20 results

@router.get("/all-body-types")
def get_all_body_types():
    """Get all unique body types"""
    body_types = set()
    for make_data in CAR_DATABASE.values():
        for model_data in make_data["models"].values():
            body_types.update(model_data.get("body_types", []))
    
    return {"body_types": sorted(list(body_types))}

@router.get("/all-transmissions")
def get_all_transmissions():
    """Get all unique transmission types"""
    transmissions = set()
    for make_data in CAR_DATABASE.values():
        for model_data in make_data["models"].values():
            transmissions.update(model_data.get("transmissions", []))
    
    return {"transmissions": sorted(list(transmissions))}

@router.get("/all-fuel-types")
def get_all_fuel_types():
    """Get all unique fuel types"""
    fuel_types = set()
    for make_data in CAR_DATABASE.values():
        for model_data in make_data["models"].values():
            fuel_types.update(model_data.get("fuel_types", []))
    
    return {"fuel_types": sorted(list(fuel_types))}