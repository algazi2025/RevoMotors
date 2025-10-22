from app.database import init_db, SessionLocal
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# CRITICAL: Import models BEFORE importing routers and database
from app.models import Base, User, DealerProfile, SellerProfile, CarListing, Lead, Offer, Message
from app.database import engine

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
    from sqlalchemy import inspect
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
        init_db()  # Create car database tables
        logger.info("✅ Car database initialized!")
    except Exception as e:
        logger.warning(f"Car database already initialized: {e}")
    
    # Seed car data
   # try:
    #    from app.migrate_data import seed_database
     #   seed_database()
      #  logger.info("✅ Car database seeded!")
    #except Exception as e:
     #   logger.info(f"Car database already seeded or error: {e}")
    
    logger.info("🚀 RevoMotors API is ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)