from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey, JSON, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    SELLER = "seller"
    DEALER = "dealer"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
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