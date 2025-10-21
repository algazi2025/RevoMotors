from fastapi import APIRouter, HTTPException, Depends
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
    # Truncate to 72 bytes for bcrypt compatibility
    if isinstance(pwd, str):
        pwd = pwd.encode('utf-8')[:400].decode('utf-8', errors='ignore')
    return pwd_context.hash(pwd)

def verify_password(plain, hashed):
    if isinstance(plain, str):
        plain = plain.encode('utf-8')[:400].decode('utf-8', errors='ignore')
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
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/signup", response_model=schemas.TokenResponse)
def signup(req: schemas.SignupRequest, db: Session = Depends(get_db)):
    # Check if email exists
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    user = User(
        email=req.email,
        hashed_password=hash_password(req.password),
        first_name=req.first_name,
        last_name=req.last_name,
        role=UserRole(req.role)
    )
    db.add(user)
    db.flush()
    
    # Create profile based on role
    if user.role == UserRole.DEALER:
        db.add(DealerProfile(user_id=user.id, company_name=req.first_name))
    else:
        db.add(SellerProfile(user_id=user.id))
    
    db.commit()
    
    # Generate token
    token = create_token(user.id, user.role.value)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role.value
    }

@router.post("/login", response_model=schemas.TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == form.username).first()
    
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate token
    token = create_token(user.id, user.role.value)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role.value
    }