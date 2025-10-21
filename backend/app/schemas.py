from pydantic import BaseModel, EmailStr
from typing import Optional
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
    gdpr_consent: Optional[bool] = False
    ccpa_consent: Optional[bool] = False

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
    price: Optional[float] = None
    trim: Optional[str] = None
    vin: Optional[str] = None
    color: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    title_status: Optional[str] = None
    accident_history: Optional[str] = None
    number_of_owners: Optional[int] = None
    asking_price: Optional[float] = None
    description: Optional[str] = None
    photos: Optional[list] = None

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