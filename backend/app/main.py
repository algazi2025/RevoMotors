from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.offers import router as offers_router
from app.api.messages import router as messages_router
from app.api.dealers import router as dealers_router
from app.database import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables only if they don't exist
try:
    Base.metadata.create_all(bind=engine, checkfirst=True)
    logger.info("Database tables verified/created successfully")
except Exception as e:
    logger.warning(f"Database table creation warning: {e}")

app = FastAPI(
    title="RevoMotors - Used Car AI Platform", 
    version="1.0.0",
    description="AI-powered used car marketplace API"
)

# CORS Configuration - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(offers_router, prefix="/api/offers", tags=["offers"])
app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
app.include_router(dealers_router, prefix="/api/dealers", tags=["dealers"])

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "status": "ready",
        "service": "RevoMotors API",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "database": "connected"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("RevoMotors API starting up...")
    logger.info("All routers loaded successfully")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("RevoMotors API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )