"""
Migration script: Load comprehensive car data into PostgreSQL database
Includes ALL major car makes and models available in the market
Run this once to populate the database
"""

from sqlalchemy import text
from app.database import SessionLocal, init_db, Make, Model, Trim, BodyType, Transmission, FuelType

# COMPREHENSIVE car database with ALL major makes and models (42 makes)
CAR_DATABASE = {
    # American Makes
    "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Edge", "Fusion", "Focus", "Fiesta", "Bronco", "Ranger"],
    "Chevrolet": ["Silverado 1500", "Silverado 2500HD", "Malibu", "Equinox", "Tahoe", "Suburban", "Traverse", "Blazer", "Trailblazer", "Colorado", "Cruze", "Spark", "Corvette", "Camaro"],
    "GMC": ["Sierra 1500", "Sierra 2500HD", "Yukon", "Terrain", "Acadia", "Canyon"],
    "Dodge": ["Ram 1500", "Ram 2500", "Charger", "Challenger", "Durango", "Journey"],
    "Chrysler": ["Pacifica", "300"],
    "Ram": ["1500", "2500", "3500"],
    
    # Japanese Makes
    "Honda": ["Accord", "Civic", "CR-V", "Pilot", "Odyssey", "Ridgeline", "Fit", "Insight", "HR-V"],
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma", "Tundra", "Sienna", "Celica", "Prius", "Yaris", "4Runner", "GR86"],
    "Nissan": ["Altima", "Rogue", "Sentra", "Maxima", "Murano", "Pathfinder", "Frontier", "Leaf", "370Z", "Versa"],
    "Mazda": ["3", "6", "CX-5", "CX-3", "CX-9", "MX-5"],
    "Subaru": ["Outback", "Forester", "Crosstrek", "Impreza", "Legacy", "WRX", "BRZ", "Ascent"],
    "Mitsubishi": ["Outlander", "Lancer", "Mirage", "Eclipse Cross", "Outlander PHEV"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Kona", "Venue", "Ioniq", "Accent"],
    "Kia": ["Forte", "Optima", "Sportage", "Sorento", "Seltos", "Telluride", "Rio", "K5", "Niro"],
    "Suzuki": ["Swift", "Vitara", "S-Cross", "Jimny"],
    "Daihatsu": ["Hijet", "Copen"],
    
    # Luxury Makes
    "BMW": ["3 Series", "5 Series", "7 Series", "X1", "X3", "X5", "X7", "Z4", "i4"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLE", "GLC", "GLA", "A-Class", "EQS"],
    "Audi": ["A3", "A4", "A6", "Q3", "Q5", "Q7", "Q8", "e-tron"],
    "Porsche": ["911", "Cayenne", "Macan", "Boxster", "Panamera", "Taycan"],
    "Jaguar": ["XE", "XF", "F-PACE", "F-TYPE", "I-PACE"],
    "Land Rover": ["Range Rover", "Range Rover Sport", "Discovery", "Defender", "Range Rover Evoque"],
    "Lexus": ["ES", "RX", "GX", "LX", "IS", "NX", "LS", "UX"],
    "Infiniti": ["Q50", "Q60", "QX50", "QX60", "Q70"],
    "Acura": ["MDX", "RDX", "ILX", "TSX"],
    "Genesis": ["G70", "G80", "G90", "GV70", "GV80"],
    
    # Electric & Performance
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X", "Roadster", "Cybertruck"],
    "Rivian": ["R1T", "R1S"],
    "Lucid": ["Air", "Gravity"],
    "Polestar": ["1", "2", "3"],
    
    # Sport & Performance
    "Jeep": ["Wrangler", "Grand Cherokee", "Cherokee", "Compass", "Renegade"],
    "Alfa Romeo": ["Giulia", "Stelvio"],
    "Fiat": ["500", "500X", "500L"],
    "Volkswagen": ["Jetta", "Passat", "Golf", "Tiguan", "ID.4"],
    "Volvo": ["S60", "S90", "XC40", "XC60", "XC90"],
    "Saab": ["9-3", "9-5"],
    "Bentley": ["Continental", "Flying Spur", "Bentayga"],
    "Rolls-Royce": ["Ghost", "Phantom", "Wraith"],
    "Lamborghini": ["Huracán", "Aventador", "Urus"],
    "Ferrari": ["F8", "Roma", "SF90"],
    "Maserati": ["Ghibli", "Quattroporte", "Levante"],
    "Bugatti": ["Chiron", "Bolide"],
}


def seed_database(force=False):
    """Populate database with comprehensive car data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Make).count()
        if existing_count > 0 and not force:
            print("Database already populated. Skipping seed.")
            return
        
        print("Starting comprehensive database seed...")
        total_makes = len(CAR_DATABASE)
        total_models = sum(len(models) for models in CAR_DATABASE.values())
        
        print(f"📊 Total makes: {total_makes}")
        print(f"📊 Total models: {total_models}")
        print()
        
        for make_name, model_names in CAR_DATABASE.items():
            print(f"✏️  Adding {make_name}... ({len(model_names)} models)")
            
            # Create or get make
            make = db.query(Make).filter(Make.name == make_name).first()
            if not make:
                make = Make(name=make_name)
                db.add(make)
                db.flush()
            
            # Add models for this make
            for model_name in model_names:
                existing_model = db.query(Model).filter(
                    Model.name == model_name,
                    Model.make_id == make.id
                ).first()
                
                if not existing_model:
                    model = Model(
                        name=model_name,
                        make_id=make.id,
                        year_min=1990,
                        year_max=2026
                    )
                    db.add(model)
        
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
    db = SessionLocal()
    
    # Clear old data first (clear junction tables first due to foreign keys)
    print("🗑️  Clearing old data...")
    try:
        # Delete from junction tables first
        db.execute(text("DELETE FROM model_trims"))
        db.execute(text("DELETE FROM model_body_types"))
        db.execute(text("DELETE FROM model_transmissions"))
        db.execute(text("DELETE FROM model_fuel_types"))
        db.commit()
        
        # Now delete models and makes
        db.query(Model).delete()
        db.query(Make).delete()
        db.commit()
        print("✓ Old data cleared")
    except Exception as e:
        print(f"Error clearing: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Force seed with fresh data
    seed_database(force=True)
