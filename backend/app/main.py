from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.offers import router as offers_router
from app.api.messages import router as messages_router
from app.api.dealers import router as dealers_router
from app.database import engine, Base

# Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Used Car AI Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(offers_router, prefix="/api/offers", tags=["offers"])
app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
app.include_router(dealers_router, prefix="/api/dealers", tags=["dealers"])

@app.get("/")
def root():
    return {"status": "ready"}

@app.get("/health")
def health():
    return {"status": "healthy"}