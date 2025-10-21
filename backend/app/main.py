from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.auth import router as auth_router
from app.api import leads, offers, messages, dealers
from app.database import engine, Base

Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Used Car AI Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(offers.router, prefix="/api/offers", tags=["offers"])
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])
app.include_router(dealers.router, prefix="/api/dealers", tags=["dealers"])

@app.get("/")
def root():
    return {"status": "ready"}

@app.get("/health")
def health():
    return {"status": "healthy"}
