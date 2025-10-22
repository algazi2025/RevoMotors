"""
Car Database API - Queries from PostgreSQL database
Provides comprehensive vehicle information
Supports: Makes, Models, Trims, Years, Body Types, etc.
"""

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Make, Model, Trim, BodyType, Transmission, FuelType

router = APIRouter()


@router.get("/makes")
def get_all_makes(db: Session = Depends(get_db)):
    """Get all available car makes"""
    makes = db.query(Make).all()
    make_names = sorted([make.name for make in makes])
    return {"makes": make_names}


@router.get("/models")
def get_models_by_make(make: str = Query(..., description="Car make"), db: Session = Depends(get_db)):
    """Get all models for a specific make"""
    make_obj = db.query(Make).filter(Make.name == make).first()
    
    if not make_obj:
        return {"make": make, "models": []}
    
    models = sorted([model.name for model in make_obj.models])
    return {"make": make, "models": models}


@router.get("/trims")
def get_trims_by_model(
    make: str = Query(..., description="Car make"),
    model: str = Query(..., description="Car model"),
    db: Session = Depends(get_db)
):
    """Get all trims for a specific make/model"""
    make_obj = db.query(Make).filter(Make.name == make).first()
    
    if not make_obj:
        return {"make": make, "model": model, "trims": []}
    
    model_obj = db.query(Model).filter(
        Model.make_id == make_obj.id,
        Model.name == model
    ).first()
    
    if not model_obj:
        return {"make": make, "model": model, "trims": []}
    
    trims = sorted([trim.name for trim in model_obj.trims])
    return {"make": make, "model": model, "trims": trims}


@router.get("/years")
def get_years_by_model(
    make: str = Query(..., description="Car make"),
    model: str = Query(..., description="Car model"),
    db: Session = Depends(get_db)
):
    """Get all available years for a specific make/model"""
    make_obj = db.query(Make).filter(Make.name == make).first()
    
    if not make_obj:
        return {"make": make, "model": model, "years": []}
    
    model_obj = db.query(Model).filter(
        Model.make_id == make_obj.id,
        Model.name == model
    ).first()
    
    if not model_obj:
        return {"make": make, "model": model, "years": []}
    
    years = list(range(model_obj.year_min, model_obj.year_max + 1))
    years.sort(reverse=True)  # Most recent first
    
    return {"make": make, "model": model, "years": years}


@router.get("/details")
def get_vehicle_details(
    make: str = Query(..., description="Car make"),
    model: str = Query(..., description="Car model"),
    db: Session = Depends(get_db)
):
    """Get all details (trims, years, body types, etc.) for a specific make/model"""
    make_obj = db.query(Make).filter(Make.name == make).first()
    
    if not make_obj:
        return {"error": "Make not found"}
    
    model_obj = db.query(Model).filter(
        Model.make_id == make_obj.id,
        Model.name == model
    ).first()
    
    if not model_obj:
        return {"error": "Model not found"}
    
    years = list(range(model_obj.year_min, model_obj.year_max + 1))
    years.sort(reverse=True)
    
    return {
        "make": make,
        "model": model,
        "years": years,
        "trims": sorted([trim.name for trim in model_obj.trims]),
        "body_types": sorted([bt.name for bt in model_obj.body_types]),
        "transmissions": sorted([t.name for t in model_obj.transmissions]),
        "fuel_types": sorted([ft.name for ft in model_obj.fuel_types])
    }


@router.get("/search")
def search_vehicles(query: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    """Search for vehicles by make or model name"""
    query_lower = query.lower()
    results = []
    
    # Search by make
    makes = db.query(Make).filter(Make.name.ilike(f"%{query_lower}%")).all()
    for make in makes:
        for model in make.models:
            results.append({
                "make": make.name,
                "model": model.name,
                "label": f"{make.name} {model.name}"
            })
    
    # Search by model (if not already found by make)
    models = db.query(Model).filter(Model.name.ilike(f"%{query_lower}%")).all()
    for model in models:
        already_found = any(
            r["make"] == model.make.name and r["model"] == model.name
            for r in results
        )
        if not already_found:
            results.append({
                "make": model.make.name,
                "model": model.name,
                "label": f"{model.make.name} {model.name}"
            })
    
    return {"results": results[:20]}  # Limit to 20 results


@router.get("/all-body-types")
def get_all_body_types(db: Session = Depends(get_db)):
    """Get all unique body types"""
    body_types = db.query(BodyType).all()
    body_type_names = sorted([bt.name for bt in body_types])
    return {"body_types": body_type_names}


@router.get("/all-transmissions")
def get_all_transmissions(db: Session = Depends(get_db)):
    """Get all unique transmission types"""
    transmissions = db.query(Transmission).all()
    transmission_names = sorted([t.name for t in transmissions])
    return {"transmissions": transmission_names}


@router.get("/all-fuel-types")
def get_all_fuel_types(db: Session = Depends(get_db)):
    """Get all unique fuel types"""
    fuel_types = db.query(FuelType).all()
    fuel_type_names = sorted([ft.name for ft in fuel_types])
    return {"fuel_types": fuel_type_names}