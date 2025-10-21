from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.offers import router as offers_router
from app.api.messages import router as messages_router
from app.api.dealers import router as dealers_router
from app.database import engine, Base
from app import models  # CRITICAL: Import models to register them

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force create all database tables
try:
    logger.info("Creating database tables...")
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Create fresh tables
    logger.info("✅ Database tables created successfully!")
except Exception as e:
    logger.error(f"❌ Database error: {e}")
    raise

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
    logger.error(f"Global error: {exc}", exc_info=True)
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

@app.get("/")
def root():
    return {
        "status": "ready",
        "service": "RevoMotors API",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 RevoMotors API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 RevoMotors API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )