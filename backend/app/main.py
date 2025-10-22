from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from sqlalchemy import text, inspect

# CRITICAL: Import models BEFORE importing routers and database
from app.models import Base, User, DealerProfile, SellerProfile, CarListing, Lead, Offer, Message
from app.database import engine, SessionLocal, init_db

# Import routers AFTER models
from app.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.offers import router as offers_router
from app.api.messages import router as messages_router
from app.api.dealers import router as dealers_router
from app.api.car_database import router as car_database_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create ALL database tables
logger.info("Creating database tables...")
try:
    # This will now work because all models are imported above
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully!")
    
    # Verify tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"📋 Available tables: {tables}")
    
except Exception as e:
    logger.error(f"❌ Database error: {e}")

app = FastAPI(
    title="RevoMotors - Used Car AI Platform", 
    version="1.0.0",
    description="AI-powered used car marketplace API"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Include all API routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(offers_router, prefix="/api/offers", tags=["offers"])
app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
app.include_router(dealers_router, prefix="/api/dealers", tags=["dealers"])
app.include_router(car_database_router, prefix="/api/cars", tags=["cars"])

@app.get("/")
def root():
    return {"status": "ready", "service": "RevoMotors API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "database": "connected"}

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing PostgreSQL database...")
    try:
        init_db()
        logger.info("✅ Car database initialized!")
    except Exception as e:
        logger.warning(f"Car database already initialized: {e}")
    
    # Add missing columns to all tables
    logger.info("Verifying database columns...")
    try:
        db = SessionLocal()
        
        # Add missing columns to dealer_profiles table
        db.execute(text("""
            ALTER TABLE dealer_profiles 
            ADD COLUMN IF NOT EXISTS license_number VARCHAR(100),
            ADD COLUMN IF NOT EXISTS phone VARCHAR(50),
            ADD COLUMN IF NOT EXISTS address TEXT,
            ADD COLUMN IF NOT EXISTS city VARCHAR(100),
            ADD COLUMN IF NOT EXISTS state VARCHAR(50),
            ADD COLUMN IF NOT EXISTS zip_code VARCHAR(20),
            ADD COLUMN IF NOT EXISTS website VARCHAR(255),
            ADD COLUMN IF NOT EXISTS verification_status VARCHAR(50) DEFAULT 'pending',
            ADD COLUMN IF NOT EXISTS auto_followup_enabled BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS followup_day_1 BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS followup_day_3 BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS followup_day_7 BOOLEAN DEFAULT true
        """))
        
        # Add missing columns to leads table (AI capabilities)
        db.execute(text("""
            ALTER TABLE leads 
            ADD COLUMN IF NOT EXISTS ai_estimated_value FLOAT,
            ADD COLUMN IF NOT EXISTS ai_offer_low FLOAT,
            ADD COLUMN IF NOT EXISTS ai_offer_fair FLOAT,
            ADD COLUMN IF NOT EXISTS ai_offer_high FLOAT,
            ADD COLUMN IF NOT EXISTS ai_rationale TEXT
        """))
        
        # Add missing columns to car_listings table
        db.execute(text("""
            ALTER TABLE car_listings 
            ADD COLUMN IF NOT EXISTS photos JSON,
            ADD COLUMN IF NOT EXISTS external_url TEXT,
            ADD COLUMN IF NOT EXISTS external_listing_id VARCHAR(255),
            ADD COLUMN IF NOT EXISTS description TEXT,
            ADD COLUMN IF NOT EXISTS seller_phone VARCHAR(50),
            ADD COLUMN IF NOT EXISTS seller_email VARCHAR(255),
            ADD COLUMN IF NOT EXISTS seller_name VARCHAR(255),
            ADD COLUMN IF NOT EXISTS source VARCHAR(50),
            ADD COLUMN IF NOT EXISTS zip_code VARCHAR(20),
            ADD COLUMN IF NOT EXISTS state VARCHAR(50),
            ADD COLUMN IF NOT EXISTS city VARCHAR(100),
            ADD COLUMN IF NOT EXISTS region VARCHAR(100),
            ADD COLUMN IF NOT EXISTS fuel_type VARCHAR(50),
            ADD COLUMN IF NOT EXISTS transmission VARCHAR(50),
            ADD COLUMN IF NOT EXISTS color VARCHAR(50),
            ADD COLUMN IF NOT EXISTS vin VARCHAR(17),
            ADD COLUMN IF NOT EXISTS condition VARCHAR(50),
            ADD COLUMN IF NOT EXISTS mileage INTEGER,
            ADD COLUMN IF NOT EXISTS trim VARCHAR(100),
            ADD COLUMN IF NOT EXISTS model VARCHAR(100),
            ADD COLUMN IF NOT EXISTS make VARCHAR(100),
            ADD COLUMN IF NOT EXISTS year INTEGER,
            ADD COLUMN IF NOT EXISTS title VARCHAR(255),
            ADD COLUMN IF NOT EXISTS asking_price FLOAT
        """))
        
        # Add missing columns to messages table
        db.execute(text("""
            ALTER TABLE messages 
            ADD COLUMN IF NOT EXISTS channel VARCHAR(50),
            ADD COLUMN IF NOT EXISTS seller_replied BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS read_by_seller BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS sent_at TIMESTAMP,
            ADD COLUMN IF NOT EXISTS sent BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS modified_by_dealer BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS generated_by_ai BOOLEAN DEFAULT true,
            ADD COLUMN IF NOT EXISTS body TEXT,
            ADD COLUMN IF NOT EXISTS subject VARCHAR(500),
            ADD COLUMN IF NOT EXISTS message_type VARCHAR(50)
        """))
        
        # Add missing columns to offers table
        db.execute(text("""
            ALTER TABLE offers 
            ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending',
            ADD COLUMN IF NOT EXISTS amount DECIMAL(10, 2)
        """))
        
        # Add missing columns to dealer_documents table
        db.execute(text("""
            ALTER TABLE dealer_documents 
            ADD COLUMN IF NOT EXISTS uploaded_at TIMESTAMP,
            ADD COLUMN IF NOT EXISTS verified BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS expires_at DATE,
            ADD COLUMN IF NOT EXISTS file_url TEXT,
            ADD COLUMN IF NOT EXISTS document_name VARCHAR(255),
            ADD COLUMN IF NOT EXISTS document_type VARCHAR(100)
        """))
        
        # Add missing columns to seller_profiles table
        db.execute(text("""
            ALTER TABLE seller_profiles 
            ADD COLUMN IF NOT EXISTS phone VARCHAR(50)
        """))
        
        db.commit()
        db.close()
        logger.info("✅ All table columns verified!")
    except Exception as e:
        logger.warning(f"Column verification: {e}")
    
    # Seed car data
    try:
        from app.migrate_data import seed_database
        seed_database()
        logger.info("✅ Car database seeded!")
    except Exception as e:
        logger.info(f"Car database already seeded or error: {e}")
    
    logger.info("🚀 RevoMotors API is ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
