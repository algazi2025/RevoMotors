from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import logging
from app.database import get_db
from app.models import User, UserRole, DealerProfile, SellerProfile
from app import schemas

router = APIRouter()
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-prod")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def hash_password(pwd: str):
    try:
        # Ensure it's a string and truncate to 72 bytes
        pwd_str = str(pwd)
        # Truncate to 72 characters (which is safely under 72 bytes for ASCII)
        truncated = pwd_str[:72]
        logger.info(f"Hashing password of length: {len(truncated)}")
        hashed = pwd_context.hash(truncated)
        return hashed
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise

def verify_password(plain: str, hashed: str):
    try:
        plain_str = str(plain)[:72]
        return pwd_context.verify(plain_str, hashed)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

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
    try:
        logger.info(f"Signup attempt for email: {req.email}")
        
        # Validate password length
        if len(req.password) > 100:
            raise HTTPException(status_code=400, detail="Password too long (max 100 characters)")
        
        # Check if email exists
        existing_user = db.query(User).filter(User.email == req.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # Hash password
        logger.info("Hashing password...")
        hashed_pwd = hash_password(req.password)
        logger.info("Password hashed successfully")
        
        # Create user
        user = User(
            email=req.email,
            hashed_password=hashed_pwd,
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
        db.refresh(user)
        
        logger.info(f"User created successfully with ID: {user.id}")
        
        # Generate token
        token = create_token(user.id, user.role.value)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "role": user.role.value
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@router.post("/login", response_model=schemas.TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logger.info(f"Login attempt for email: {form.username}")
        
        # Find user by email
        user = db.query(User).filter(User.email == form.username).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not verify_password(form.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        logger.info(f"Login successful for user ID: {user.id}")
        
        # Generate token
        token = create_token(user.id, user.role.value)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "role": user.role.value
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")