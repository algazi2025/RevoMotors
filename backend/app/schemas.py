from pydantic import BaseModel, EmailStr
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
