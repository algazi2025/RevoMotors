from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date
import logging

from app.database import get_db
from app.models import (
    DealerProfile, DealerMarketplaceFilter, DealerDocument, User, UserRole
)
from app.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

# ========== DEALER PROFILE ENDPOINTS ==========

@router.get("/profile")
def get_dealer_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current dealer's profile"""
    
    if current_user.role != UserRole.DEALER:
        raise HTTPException(status_code=403, detail="Only dealers can access this")
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    return {
        "id": dealer.id,
        "user_id": dealer.user_id,
        "company_name": dealer.company_name,
        "dealership_name": dealer.dealership_name,
        "license_number": dealer.license_number,
        "phone": dealer.phone,
        "address": dealer.address,
        "city": dealer.city,
        "state": dealer.state,
        "zip_code": dealer.zip_code,
        "website": dealer.website,
        "verification_status": dealer.verification_status,
        "communication_preferences": {
            "auto_followup_enabled": dealer.auto_followup_enabled,
            "followup_day_1": dealer.followup_day_1,
            "followup_day_3": dealer.followup_day_3,
            "followup_day_7": dealer.followup_day_7
        },
        "created_at": dealer.created_at.isoformat()
    }

@router.put("/profile")
def update_dealer_profile(
    company_name: Optional[str] = None,
    dealership_name: Optional[str] = None,
    license_number: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    website: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update dealer profile"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Update fields if provided
    if company_name: dealer.company_name = company_name
    if dealership_name: dealer.dealership_name = dealership_name
    if license_number: dealer.license_number = license_number
    if phone: dealer.phone = phone
    if address: dealer.address = address
    if city: dealer.city = city
    if state: dealer.state = state
    if zip_code: dealer.zip_code = zip_code
    if website: dealer.website = website
    
    db.commit()
    db.refresh(dealer)
    
    return {
        "success": True,
        "message": "Profile updated successfully"
    }

# ========== COMMUNICATION PREFERENCES ==========

@router.put("/communication-preferences")
def update_communication_preferences(
    auto_followup_enabled: Optional[bool] = None,
    followup_day_1: Optional[bool] = None,
    followup_day_3: Optional[bool] = None,
    followup_day_7: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update dealer's communication/follow-up preferences"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Update preferences
    if auto_followup_enabled is not None:
        dealer.auto_followup_enabled = auto_followup_enabled
    if followup_day_1 is not None:
        dealer.followup_day_1 = followup_day_1
    if followup_day_3 is not None:
        dealer.followup_day_3 = followup_day_3
    if followup_day_7 is not None:
        dealer.followup_day_7 = followup_day_7
    
    db.commit()
    
    return {
        "success": True,
        "message": "Communication preferences updated",
        "preferences": {
            "auto_followup_enabled": dealer.auto_followup_enabled,
            "followup_day_1": dealer.followup_day_1,
            "followup_day_3": dealer.followup_day_3,
            "followup_day_7": dealer.followup_day_7
        }
    }

# ========== MARKETPLACE FILTERS ==========

@router.get("/filters")
def get_marketplace_filters(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dealer's marketplace filters"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    filters = db.query(DealerMarketplaceFilter).filter(
        DealerMarketplaceFilter.dealer_id == dealer.id,
        DealerMarketplaceFilter.is_active == True
    ).all()
    
    return {
        "total": len(filters),
        "filters": [{
            "id": f.id,
            "vehicle_filters": {
                "makes": f.makes or [],
                "models": f.models or [],
                "year_min": f.year_min,
                "year_max": f.year_max,
                "mileage_max": f.mileage_max,
                "price_min": f.price_min,
                "price_max": f.price_max
            },
            "location_filters": {
                "zip_codes": f.zip_codes or [],
                "radius_miles": f.radius_miles
            },
            "marketplaces": {
                "facebook": f.facebook_enabled,
                "offerup": f.offerup_enabled,
                "craigslist": f.craigslist_enabled,
                "autotrader": f.autotrader_enabled,
                "carscom": f.carscom_enabled
            },
            "is_active": f.is_active,
            "created_at": f.created_at.isoformat()
        } for f in filters]
    }

@router.post("/filters")
def create_marketplace_filter(
    makes: Optional[List[str]] = None,
    models: Optional[List[str]] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    mileage_max: Optional[int] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    zip_codes: Optional[List[str]] = None,
    radius_miles: int = 50,
    facebook_enabled: bool = True,
    offerup_enabled: bool = True,
    craigslist_enabled: bool = True,
    autotrader_enabled: bool = False,
    carscom_enabled: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new marketplace filter"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Create filter
    new_filter = DealerMarketplaceFilter(
        dealer_id=dealer.id,
        makes=makes or [],
        models=models or [],
        year_min=year_min,
        year_max=year_max,
        mileage_max=mileage_max,
        price_min=price_min,
        price_max=price_max,
        zip_codes=zip_codes or [],
        radius_miles=radius_miles,
        facebook_enabled=facebook_enabled,
        offerup_enabled=offerup_enabled,
        craigslist_enabled=craigslist_enabled,
        autotrader_enabled=autotrader_enabled,
        carscom_enabled=carscom_enabled,
        is_active=True
    )
    
    db.add(new_filter)
    db.commit()
    db.refresh(new_filter)
    
    return {
        "success": True,
        "message": "Filter created successfully",
        "filter_id": new_filter.id
    }

@router.put("/filters/{filter_id}")
def update_marketplace_filter(
    filter_id: int,
    makes: Optional[List[str]] = None,
    models: Optional[List[str]] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    mileage_max: Optional[int] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    zip_codes: Optional[List[str]] = None,
    radius_miles: Optional[int] = None,
    facebook_enabled: Optional[bool] = None,
    offerup_enabled: Optional[bool] = None,
    craigslist_enabled: Optional[bool] = None,
    autotrader_enabled: Optional[bool] = None,
    carscom_enabled: Optional[bool] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update existing marketplace filter"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    filter_obj = db.query(DealerMarketplaceFilter).filter(
        DealerMarketplaceFilter.id == filter_id,
        DealerMarketplaceFilter.dealer_id == dealer.id
    ).first()
    
    if not filter_obj:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    # Update fields
    if makes is not None: filter_obj.makes = makes
    if models is not None: filter_obj.models = models
    if year_min is not None: filter_obj.year_min = year_min
    if year_max is not None: filter_obj.year_max = year_max
    if mileage_max is not None: filter_obj.mileage_max = mileage_max
    if price_min is not None: filter_obj.price_min = price_min
    if price_max is not None: filter_obj.price_max = price_max
    if zip_codes is not None: filter_obj.zip_codes = zip_codes
    if radius_miles is not None: filter_obj.radius_miles = radius_miles
    if facebook_enabled is not None: filter_obj.facebook_enabled = facebook_enabled
    if offerup_enabled is not None: filter_obj.offerup_enabled = offerup_enabled
    if craigslist_enabled is not None: filter_obj.craigslist_enabled = craigslist_enabled
    if autotrader_enabled is not None: filter_obj.autotrader_enabled = autotrader_enabled
    if carscom_enabled is not None: filter_obj.carscom_enabled = carscom_enabled
    if is_active is not None: filter_obj.is_active = is_active
    
    db.commit()
    
    return {
        "success": True,
        "message": "Filter updated successfully"
    }

@router.delete("/filters/{filter_id}")
def delete_marketplace_filter(
    filter_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete marketplace filter"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    filter_obj = db.query(DealerMarketplaceFilter).filter(
        DealerMarketplaceFilter.id == filter_id,
        DealerMarketplaceFilter.dealer_id == dealer.id
    ).first()
    
    if not filter_obj:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    db.delete(filter_obj)
    db.commit()
    
    return {
        "success": True,
        "message": "Filter deleted successfully"
    }

# ========== DOCUMENTS ==========

@router.get("/documents")
def get_dealer_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all dealer documents"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    documents = db.query(DealerDocument).filter(
        DealerDocument.dealer_id == dealer.id
    ).all()
    
    return {
        "total": len(documents),
        "documents": [{
            "id": doc.id,
            "document_type": doc.document_type,
            "document_name": doc.document_name,
            "file_url": doc.file_url,
            "expires_at": doc.expires_at.isoformat() if doc.expires_at else None,
            "verified": doc.verified,
            "uploaded_at": doc.uploaded_at.isoformat()
        } for doc in documents]
    }

@router.post("/documents")
def upload_dealer_document(
    document_type: str,
    document_name: str,
    file_url: str,  # In production, handle actual file upload
    expires_at: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload dealer document (license, insurance, etc.)"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Create document record
    document = DealerDocument(
        dealer_id=dealer.id,
        document_type=document_type,
        document_name=document_name,
        file_url=file_url,
        expires_at=expires_at,
        verified=False
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "success": True,
        "message": "Document uploaded successfully",
        "document_id": document.id
    }

@router.delete("/documents/{document_id}")
def delete_dealer_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete dealer document"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    document = db.query(DealerDocument).filter(
        DealerDocument.id == document_id,
        DealerDocument.dealer_id == dealer.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()
    
    return {
        "success": True,
        "message": "Document deleted successfully"
    }

# ========== DASHBOARD STATS ==========

@router.get("/stats")
def get_dealer_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dealer dashboard statistics"""
    
    from app.models import Lead, LeadStatus, LeadSource, CarListing
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Get total leads
    total_leads = db.query(Lead).filter(Lead.dealer_id == dealer.id).count()
    
    # Get hot leads count
    hot_leads = db.query(Lead).join(CarListing).filter(
        Lead.dealer_id == dealer.id,
        CarListing.source == LeadSource.HOT_LEAD
    ).count()
    
    # Get marketplace leads count
    marketplace_leads = db.query(Lead).join(CarListing).filter(
        Lead.dealer_id == dealer.id,
        CarListing.source != LeadSource.HOT_LEAD
    ).count()
    
    # Get new leads (not contacted yet)
    new_leads = db.query(Lead).filter(
        Lead.dealer_id == dealer.id,
        Lead.status == LeadStatus.NEW
    ).count()
    
    # Get contacted leads
    contacted_leads = db.query(Lead).filter(
        Lead.dealer_id == dealer.id,
        Lead.status == LeadStatus.CONTACTED
    ).count()
    
    # Get won deals
    won_deals = db.query(Lead).filter(
        Lead.dealer_id == dealer.id,
        Lead.status == LeadStatus.WON
    ).count()
    
    return {
        "total_leads": total_leads,
        "hot_leads": hot_leads,
        "marketplace_leads": marketplace_leads,
        "new_leads": new_leads,
        "contacted_leads": contacted_leads,
        "won_deals": won_deals,
        "conversion_rate": round((won_deals / total_leads * 100) if total_leads > 0 else 0, 2)
    }