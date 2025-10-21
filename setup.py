#!/usr/bin/env python3
"""
Setup script - Creates all project files automatically
Run this: python setup.py
"""

import os
from pathlib import Path

def create_folder(path):
    """Create folder if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created folder: {path}")

def create_file(path, content):
    """Create file with content"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created file: {path}")

print("=" * 60)
print("Creating Project Structure".center(60))
print("=" * 60)

# Create folders
print("\n📁 Creating folders...")
create_folder("backend/app/api")
create_folder("backend/app/ai_provider")
create_folder("frontend/pages/seller")
create_folder("frontend/pages/dealer/leads")
create_folder("infra")

# Backend __init__.py files
print("\n🐍 Creating backend files...")
create_file("backend/app/__init__.py", "")
create_file("backend/app/api/__init__.py", "from . import leads, offers, messages, dealers")
create_file("backend/app/ai_provider/__init__.py", "")

# Backend main.py
main_py = """from fastapi import FastAPI
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
"""
create_file("backend/app/main.py", main_py)

# Database
database_py = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/usedcar")
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
create_file("backend/app/database.py", database_py)

# Models
models_py = """from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey, JSON, DECIMAL, Date, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    SELLER = "seller"
    DEALER = "dealer"

class User(Base):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_email", "email"),)
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.SELLER)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class DealerProfile(Base):
    __tablename__ = "dealer_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    company_name = Column(String(255), nullable=False)
    verification_status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class SellerProfile(Base):
    __tablename__ = "seller_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CarListing(Base):
    __tablename__ = "car_listings"
    __table_args__ = (Index("ix_car_listings_seller_id", "seller_id"),)
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("seller_profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    mileage = Column(Integer, nullable=False)
    condition = Column(String(50))
    region = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (Index("ix_leads_dealer_id", "dealer_id"),)
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("car_listings.id"), nullable=False)
    dealer_id = Column(Integer, ForeignKey("dealer_profiles.id"), nullable=False)
    status = Column(String(50), default="new")
    ai_draft_offer = Column(JSON)
    seller_contact_email = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    dealer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    body = Column(Text, nullable=False)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
"""
create_file("backend/app/models.py", models_py)

# Schemas
schemas_py = """from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    SELLER = "seller"
    DEALER = "dealer"

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str

class LeadWebhookPayload(BaseModel):
    marketplace: str
    title: str
    year: int
    make: str
    model: str
    mileage: int
    condition: str
    region: str
    seller_contact_name: str
    seller_contact_email: str
    seller_contact_phone: str

class OfferEstimateRequest(BaseModel):
    year: int
    make: str
    model: str
    mileage: int
    condition: str
    region: str

class OfferEstimate(BaseModel):
    low: float
    fair: float
    max: float
    rationale: str
"""
create_file("backend/app/schemas.py", schemas_py)

# Auth
auth_py = """from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

from app.database import get_db
from app.models import User, UserRole, DealerProfile, SellerProfile
from app import schemas

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-prod")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def hash_password(pwd):
    return pwd_context.hash(pwd)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(user_id, role):
    expire = datetime.utcnow() + timedelta(days=30)
    payload = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404)
    return user

@router.post("/signup", response_model=schemas.TokenResponse)
def signup(req: schemas.SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    user = User(email=req.email, hashed_password=hash_password(req.password), 
                first_name=req.first_name, last_name=req.last_name, role=UserRole(req.role))
    db.add(user)
    db.flush()
    if user.role == UserRole.DEALER:
        db.add(DealerProfile(user_id=user.id, company_name=req.first_name))
    else:
        db.add(SellerProfile(user_id=user.id))
    db.commit()
    token = create_token(user.id, user.role.value)
    return {"access_token": token, "token_type": "bearer", "user_id": user.id, "role": user.role.value}

@router.post("/login", response_model=schemas.TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401)
    token = create_token(user.id, user.role.value)
    return {"access_token": token, "token_type": "bearer", "user_id": user.id, "role": user.role.value}
"""
create_file("backend/app/auth.py", auth_py)

# API routers
create_file("backend/app/api/leads.py", "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\ndef get_leads():\n    return []")
create_file("backend/app/api/offers.py", "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\ndef get_offers():\n    return []")
create_file("backend/app/api/messages.py", "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\ndef get_messages():\n    return []")
create_file("backend/app/api/dealers.py", "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\ndef get_dealers():\n    return []")

# Mock AI provider
ai_py = """from datetime import datetime

class MockAIProvider:
    def estimate_offer(self, year, make, model, mileage, condition, region, comps=None):
        age = datetime.now().year - year
        base = max(3000, 25000 - age * 2000)
        fair = base
        return {"low": round(fair * 0.7, 2), "fair": round(fair, 2), "max": round(fair * 1.15, 2), 
                "rationale": f"{year} {make} {model}"}

ai_provider = MockAIProvider()
"""
create_file("backend/app/ai_provider/mock_provider.py", ai_py)

# Backend config files
print("\n⚙️  Creating backend config...")
create_file("backend/requirements.txt", """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
gunicorn==21.2.0
""")

create_file("backend/Dockerfile", """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]
""")

create_file("backend/.env.example", """DATABASE_URL=postgresql://user:password@localhost:5432/usedcar
JWT_SECRET=your-secret-key
AI_PROVIDER=mock
""")

# Frontend files
print("\n⚛️  Creating frontend files...")
create_file("frontend/package.json", """{
  "name": "used-car-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  }
}
""")

create_file("frontend/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2020",
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
""")

create_file("frontend/next.config.js", "module.exports = {reactStrictMode: true}")

create_file("frontend/Dockerfile", """FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
""")

create_file("frontend/.env.example", "NEXT_PUBLIC_API_URL=http://localhost:8000")

create_file("frontend/pages/_app.tsx", "export default function App({Component, pageProps}) {return <Component {...pageProps} />}")

create_file("frontend/pages/index.tsx", """import Link from 'next/link'
export default function Home() {
  return (
    <div style={{padding: '2rem', textAlign: 'center'}}>
      <h1>Used Car AI Platform</h1>
      <Link href="/seller/landing"><button>I'm a Seller</button></Link>
      <Link href="/dealer/landing"><button>I'm a Dealer</button></Link>
    </div>
  )
}
""")

create_file("frontend/pages/seller/landing.tsx", "export default function SellerLanding() {return <div style={{padding: '2rem'}}><h1>Seller Landing</h1></div>}")
create_file("frontend/pages/seller/list-car.tsx", "export default function ListCar() {return <div style={{padding: '2rem'}}><h1>List Car</h1></div>}")
create_file("frontend/pages/dealer/landing.tsx", "export default function DealerLanding() {return <div style={{padding: '2rem'}}><h1>Dealer Landing</h1></div>}")
create_file("frontend/pages/dealer/dashboard.tsx", "export default function Dashboard() {return <div style={{padding: '2rem'}}><h1>Dashboard</h1></div>}")
create_file("frontend/pages/dealer/leads/[id].tsx", "export default function LeadDetail() {return <div style={{padding: '2rem'}}><h1>Lead</h1></div>}")

# Infrastructure
print("\n🏗️  Creating infrastructure...")
docker_compose_content = """version: '3.9'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: usedcar
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ../backend
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/usedcar
      JWT_SECRET: secret-key-change
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build:
      context: ../frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"

volumes:
  postgres_data:
"""
create_file("infra/docker-compose.yml", docker_compose_content)
create_file("infra/Procfile", "web: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app.main:app")

# Root files
print("\n📄 Creating root files...")
create_file("README.md", """# Used Car AI Platform

AI-powered marketplace for used car sales.

## Quick Start
cd infra
docker-compose up --build

## Features
- Seller listing
- Dealer registration
- Real-time messaging
- AI offer estimation
""")

print("\n" + "=" * 60)
print("✅ Project Setup Complete!".center(60))
print("=" * 60)
print("\nNext steps:")
print("  1. git add .")
print("  2. git commit -m 'Add all project files'")
print("  3. git push")