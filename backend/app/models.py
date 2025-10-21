from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey, JSON, DECIMAL, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    SELLER = "seller"
    DEALER = "dealer"

class LeadSource(str, enum.Enum):
    HOT_LEAD = "hot_lead"
    FACEBOOK = "facebook"
    OFFERUP = "offerup"
    CRAIGSLIST = "craigslist"
    AUTOTRADER = "autotrader"
    CARSCOM = "carscom"
    CARGURUS = "cargurus"

class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    FOLLOW_UP = "follow_up"
    NEGOTIATING = "negotiating"
    WON = "won"
    LOST = "lost"

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
    dealership_name = Column(String(255))
    license_number = Column(String(100))
    phone = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    website = Column(String(255))
    verification_status = Column(String(50), default="pending")
    
    auto_followup_enabled = Column(Boolean, default=True)
    followup_day_1 = Column(Boolean, default=True)
    followup_day_3 = Column(Boolean, default=True)
    followup_day_7 = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class DealerMarketplaceFilter(Base):
    __tablename__ = "dealer_marketplace_filters"
    
    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, ForeignKey("dealer_profiles.id"), nullable=False)
    
    makes = Column(JSON)
    models = Column(JSON)
    year_min = Column(Integer)
    year_max = Column(Integer)
    mileage_max = Column(Integer)
    price_min = Column(Float)
    price_max = Column(Float)
    
    zip_codes = Column(JSON)
    radius_miles = Column(Integer, default=50)
    
    facebook_enabled = Column(Boolean, default=True)
    offerup_enabled = Column(Boolean, default=True)
    craigslist_enabled = Column(Boolean, default=True)
    autotrader_enabled = Column(Boolean, default=False)
    carscom_enabled = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SellerProfile(Base):
    __tablename__ = "seller_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    phone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class CarListing(Base):
    __tablename__ = "car_listings"
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("seller_profiles.id"), nullable=True)
    
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    trim = Column(String(100))
    mileage = Column(Integer, nullable=False)
    condition = Column(String(50))
    vin = Column(String(17))
    color = Column(String(50))
    transmission = Column(String(50))
    fuel_type = Column(String(50))
    
    asking_price = Column(Float)
    
    region = Column(String(100))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    
    source = Column(Enum(LeadSource), default=LeadSource.HOT_LEAD)
    external_listing_id = Column(String(255))
    external_url = Column(Text)
    
    seller_name = Column(String(255))
    seller_email = Column(String(255))
    seller_phone = Column(String(50))
    
    description = Column(Text)
    photos = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("car_listings.id"), nullable=False)
    dealer_id = Column(Integer, ForeignKey("dealer_profiles.id"), nullable=False)
    
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    
    ai_estimated_value = Column(Float)
    ai_offer_low = Column(Float)
    ai_offer_fair = Column(Float)
    ai_offer_high = Column(Float)
    ai_rationale = Column(Text)
    
    dealer_offer_amount = Column(Float)
    
    first_contact_sent = Column(Boolean, default=False)
    first_contact_at = Column(DateTime)
    last_contact_at = Column(DateTime)
    next_followup_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    dealer_id = Column(Integer, ForeignKey("dealer_profiles.id"), nullable=False)
    
    message_type = Column(String(50))
    subject = Column(String(500))
    body = Column(Text, nullable=False)
    
    generated_by_ai = Column(Boolean, default=True)
    modified_by_dealer = Column(Boolean, default=False)
    
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    read_by_seller = Column(Boolean, default=False)
    seller_replied = Column(Boolean, default=False)
    
    channel = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Offer(Base):
    __tablename__ = "offers"
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    dealer_id = Column(Integer, ForeignKey("dealer_profiles.id"), nullable=False)
    
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), default="pending")
    
    created_at = Column(DateTime, default=datetime.utcnow)

class DealerDocument(Base):
    __tablename__ = "dealer_documents"
    
    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, ForeignKey("dealer_profiles.id"), nullable=False)
    
    document_type = Column(String(100))
    document_name = Column(String(255))
    file_url = Column(Text)
    
    expires_at = Column(Date)
    verified = Column(Boolean, default=False)
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)