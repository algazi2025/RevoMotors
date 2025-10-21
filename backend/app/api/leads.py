from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import logging

from app.database import get_db
from app.models import (
    Lead, CarListing, DealerProfile, Message, User, 
    LeadStatus, LeadSource, UserRole
)
from app.auth import get_current_user
from app.ai_provider.mock_provider import MockAIProvider

router = APIRouter()
logger = logging.getLogger(__name__)
ai_provider = MockAIProvider()

@router.get("/")
def get_dealer_leads(
    source: Optional[str] = None,  # "hot_lead" or "marketplace"
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all leads for the current dealer"""
    
    # Verify user is a dealer
    if current_user.role != UserRole.DEALER:
        raise HTTPException(status_code=403, detail="Only dealers can access leads")
    
    # Get dealer profile
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Query leads
    query = db.query(Lead, CarListing).join(
        CarListing, Lead.listing_id == CarListing.id
    ).filter(Lead.dealer_id == dealer.id)
    
    # Filter by source (hot_lead vs marketplace)
    if source == "hot_lead":
        query = query.filter(CarListing.source == LeadSource.HOT_LEAD)
    elif source == "marketplace":
        query = query.filter(CarListing.source != LeadSource.HOT_LEAD)
    
    # Filter by status
    if status:
        query = query.filter(Lead.status == status)
    
    # Order by newest first
    query = query.order_by(desc(Lead.created_at))
    
    results = query.all()
    
    # Format response
    leads = []
    for lead, listing in results:
        # Get latest message
        latest_message = db.query(Message).filter(
            Message.lead_id == lead.id
        ).order_by(desc(Message.created_at)).first()
        
        leads.append({
            "lead_id": lead.id,
            "status": lead.status.value,
            "created_at": lead.created_at.isoformat(),
            "listing": {
                "id": listing.id,
                "title": listing.title,
                "year": listing.year,
                "make": listing.make,
                "model": listing.model,
                "trim": listing.trim,
                "mileage": listing.mileage,
                "condition": listing.condition,
                "vin": listing.vin,
                "color": listing.color,
                "asking_price": listing.asking_price,
                "source": listing.source.value,
                "external_url": listing.external_url,
                "location": {
                    "city": listing.city,
                    "state": listing.state,
                    "zip_code": listing.zip_code
                },
                "seller": {
                    "name": listing.seller_name,
                    "email": listing.seller_email,
                    "phone": listing.seller_phone
                },
                "photos": listing.photos or []
            },
            "ai_estimate": {
                "estimated_value": lead.ai_estimated_value,
                "offer_low": lead.ai_offer_low,
                "offer_fair": lead.ai_offer_fair,
                "offer_high": lead.ai_offer_high,
                "rationale": lead.ai_rationale
            },
            "communication": {
                "first_contact_sent": lead.first_contact_sent,
                "last_contact_at": lead.last_contact_at.isoformat() if lead.last_contact_at else None,
                "next_followup_at": lead.next_followup_at.isoformat() if lead.next_followup_at else None,
                "latest_message": {
                    "subject": latest_message.subject if latest_message else None,
                    "body": latest_message.body if latest_message else None,
                    "sent": latest_message.sent if latest_message else False
                } if latest_message else None
            }
        })
    
    return {
        "total": len(leads),
        "leads": leads
    }

@router.get("/{lead_id}")
def get_lead_details(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific lead"""
    
    # Get dealer profile
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Get lead with listing
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.dealer_id == dealer.id
    ).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    listing = db.query(CarListing).filter(
        CarListing.id == lead.listing_id
    ).first()
    
    # Get all messages for this lead
    messages = db.query(Message).filter(
        Message.lead_id == lead_id
    ).order_by(Message.created_at).all()
    
    return {
        "lead_id": lead.id,
        "status": lead.status.value,
        "created_at": lead.created_at.isoformat(),
        "listing": {
            "id": listing.id,
            "title": listing.title,
            "year": listing.year,
            "make": listing.make,
            "model": listing.model,
            "trim": listing.trim,
            "mileage": listing.mileage,
            "condition": listing.condition,
            "vin": listing.vin,
            "color": listing.color,
            "transmission": listing.transmission,
            "fuel_type": listing.fuel_type,
            "asking_price": listing.asking_price,
            "description": listing.description,
            "source": listing.source.value,
            "external_url": listing.external_url,
            "location": {
                "city": listing.city,
                "state": listing.state,
                "zip_code": listing.zip_code
            },
            "seller": {
                "name": listing.seller_name,
                "email": listing.seller_email,
                "phone": listing.seller_phone
            },
            "photos": listing.photos or []
        },
        "ai_estimate": {
            "estimated_value": lead.ai_estimated_value,
            "offer_low": lead.ai_offer_low,
            "offer_fair": lead.ai_offer_fair,
            "offer_high": lead.ai_offer_high,
            "rationale": lead.ai_rationale
        },
        "dealer_offer": lead.dealer_offer_amount,
        "messages": [{
            "id": msg.id,
            "type": msg.message_type,
            "subject": msg.subject,
            "body": msg.body,
            "generated_by_ai": msg.generated_by_ai,
            "modified_by_dealer": msg.modified_by_dealer,
            "sent": msg.sent,
            "sent_at": msg.sent_at.isoformat() if msg.sent_at else None,
            "channel": msg.channel,
            "created_at": msg.created_at.isoformat()
        } for msg in messages]
    }

@router.post("/{lead_id}/generate-message")
def generate_message(
    lead_id: int,
    message_type: str,  # "initial_contact" or "follow_up_1", etc.
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI message for a lead"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.dealer_id == dealer.id
    ).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    listing = db.query(CarListing).filter(
        CarListing.id == lead.listing_id
    ).first()
    
    # Check if message already exists
    existing_message = db.query(Message).filter(
        Message.lead_id == lead_id,
        Message.message_type == message_type,
        Message.sent == False
    ).first()
    
    if existing_message:
        return {
            "message_id": existing_message.id,
            "subject": existing_message.subject,
            "body": existing_message.body,
            "generated_by_ai": existing_message.generated_by_ai
        }
    
    # Generate new message using AI
    message_data = ai_provider.generate_message(
        template=message_type,
        lead_data={
            "listing": {
                "year": listing.year,
                "make": listing.make,
                "model": listing.model,
                "mileage": listing.mileage
            },
            "seller_name": listing.seller_name or "there",
            "offer": {
                "amount": lead.ai_offer_fair or lead.dealer_offer_amount
            },
            "dealer_name": f"{current_user.first_name} {current_user.last_name}",
            "dealership_name": dealer.company_name
        },
        tone="friendly"
    )
    
    # Save message
    new_message = Message(
        lead_id=lead_id,
        dealer_id=dealer.id,
        message_type=message_type,
        subject=message_data.get("subject", ""),
        body=message_data.get("body", ""),
        generated_by_ai=True,
        channel="email"
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return {
        "message_id": new_message.id,
        "subject": new_message.subject,
        "body": new_message.body,
        "generated_by_ai": new_message.generated_by_ai
    }

@router.post("/{lead_id}/send-message")
def send_message(
    lead_id: int,
    message_id: int,
    updated_body: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to the seller (dealer clicks 'Send')"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.dealer_id == dealer.id
    ).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.lead_id == lead_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # If dealer modified the message
    if updated_body and updated_body != message.body:
        message.body = updated_body
        message.modified_by_dealer = True
    
    # Mark as sent
    message.sent = True
    message.sent_at = datetime.utcnow()
    
    # Update lead
    if not lead.first_contact_sent:
        lead.first_contact_sent = True
        lead.first_contact_at = datetime.utcnow()
    
    lead.last_contact_at = datetime.utcnow()
    lead.status = LeadStatus.CONTACTED
    
    # TODO: Actually send email/SMS here using SendGrid, Twilio, etc.
    logger.info(f"Message sent to seller for lead {lead_id}")
    
    db.commit()
    
    return {
        "success": True,
        "message": "Message sent successfully",
        "sent_at": message.sent_at.isoformat()
    }

@router.put("/{lead_id}/update-offer")
def update_offer(
    lead_id: int,
    offer_amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dealer updates the offer amount"""
    
    dealer = db.query(DealerProfile).filter(
        DealerProfile.user_id == current_user.id
    ).first()
    
    lead = db.query(Lead).filter(
        Lead.id == lead_id,
        Lead.dealer_id == dealer.id
    ).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead.dealer_offer_amount = offer_amount
    lead.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "lead_id": lead_id,
        "dealer_offer_amount": offer_amount
    }

@router.post("/webhook/lead_received")
def receive_lead_webhook(payload: dict, db: Session = Depends(get_db)):
    """Webhook to receive new car listings (from marketplaces or direct submissions)"""
    
    logger.info(f"Received lead webhook: {payload}")
    
    # Determine source
    source = LeadSource.HOT_LEAD
    if payload.get("marketplace"):
        source = LeadSource[payload["marketplace"].upper()] if payload["marketplace"].upper() in LeadSource.__members__ else LeadSource.HOT_LEAD
    
    # Create car listing
    listing = CarListing(
        title=payload.get("title", f"{payload['year']} {payload['make']} {payload['model']}"),
        year=payload["year"],
        make=payload["make"],
        model=payload["model"],
        trim=payload.get("trim"),
        mileage=payload["mileage"],
        condition=payload.get("condition", "good"),
        vin=payload.get("vin"),
        color=payload.get("color"),
        transmission=payload.get("transmission"),
        fuel_type=payload.get("fuel_type"),
        asking_price=payload.get("price") or payload.get("asking_price"),
        region=payload.get("region"),
        city=payload.get("city"),
        state=payload.get("state"),
        zip_code=payload.get("zip_code"),
        source=source,
        external_listing_id=payload.get("external_id"),
        external_url=payload.get("url"),
        seller_name=payload.get("seller_contact_name"),
        seller_email=payload.get("seller_contact_email"),
        seller_phone=payload.get("seller_contact_phone"),
        description=payload.get("description"),
        photos=payload.get("photos", [])
    )
    
    db.add(listing)
    db.flush()
    
    # Generate AI estimate
    ai_estimate = ai_provider.estimate_offer(
        year=listing.year,
        make=listing.make,
        model=listing.model,
        mileage=listing.mileage,
        condition=listing.condition or "good",
        region=listing.region or "normal"
    )
    
    # Find matching dealers (simplified - match all verified dealers for now)
    # TODO: Implement proper filter matching
    dealers = db.query(DealerProfile).filter(
        DealerProfile.verification_status == "verified"
    ).all()
    
    created_leads = []
    
    for dealer in dealers:
        # Create lead for each matching dealer
        lead = Lead(
            listing_id=listing.id,
            dealer_id=dealer.id,
            status=LeadStatus.NEW,
            ai_estimated_value=ai_estimate.get("fair"),
            ai_offer_low=ai_estimate.get("low"),
            ai_offer_fair=ai_estimate.get("fair"),
            ai_offer_high=ai_estimate.get("max"),
            ai_rationale=ai_estimate.get("rationale", "")
        )
        db.add(lead)
        db.flush()
        
        created_leads.append(lead.id)
    
    db.commit()
    
    return {
        "status": "received",
        "listing_id": listing.id,
        "leads_created": len(created_leads),
        "ai_draft_offer": ai_estimate
    }