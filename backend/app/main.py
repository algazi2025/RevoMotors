from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.offers import router as offers_router
from app.api.messages import router as messages_router
from app.api.dealers import router as dealers_router
from app.database import engine, Base

# CRITICAL: Create all database tables - UNCOMMENTED
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RevoMotors - Used Car AI Platform", 
    version="1.0.0",
    description="AI-powered used car marketplace API"
)

# CORS Configuration - Already correct
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
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

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    logger.info("Database tables created successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )