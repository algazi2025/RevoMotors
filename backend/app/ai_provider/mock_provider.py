"""Mock AI Provider for generating offers and messages"""

class MockAIProvider:
    
    def estimate_offer(self, year, make, model, mileage, condition, region, comps=None):
        """Generate AI offer estimation"""
        
        # Base value calculation (simplified)
        base_value = 20000  # Starting point
        
        # Adjust for year
        current_year = 2025
        age = current_year - year
        base_value -= (age * 1000)
        
        # Adjust for mileage
        if mileage > 100000:
            base_value -= 5000
        elif mileage > 75000:
            base_value -= 3000
        elif mileage > 50000:
            base_value -= 1500
        
        # Adjust for condition
        condition_adjustments = {
            "excellent": 1.1,
            "good": 1.0,
            "fair": 0.85,
            "poor": 0.7
        }
        base_value *= condition_adjustments.get(condition.lower(), 1.0)
        
        # Ensure minimum value
        base_value = max(base_value, 3000)
        
        # Calculate offer range
        fair_offer = base_value
        low_offer = base_value * 0.85
        max_offer = base_value * 1.15
        
        rationale = f"Based on {year} {make} {model} with {mileage:,} miles in {condition} condition. "
        rationale += f"Market analysis shows similar vehicles trading at ${fair_offer:,.0f}. "
        rationale += "This estimate considers current market demand and vehicle history."
        
        return {
            "low": round(low_offer, 2),
            "fair": round(fair_offer, 2),
            "max": round(max_offer, 2),
            "rationale": rationale
        }
    
    def generate_message(self, template, lead_data, tone="friendly"):
        """Generate AI message for dealer to send to seller"""
        
        listing = lead_data.get("listing", {})
        seller_name = lead_data.get("seller_name", "there")
        offer = lead_data.get("offer", {})
        dealer_name = lead_data.get("dealer_name", "Our Team")
        dealership_name = lead_data.get("dealership_name", "Our Dealership")
        
        vehicle = f"{listing.get('year')} {listing.get('make')} {listing.get('model')}"
        offer_amount = offer.get("amount", 0)
        
        messages = {
            "initial_contact": {
                "subject": f"Interest in Your {vehicle}",
                "body": f"""Hi {seller_name},

I hope this message finds you well! My name is {dealer_name} from {dealership_name}, and I came across your {vehicle} listing.

We're actively looking for quality vehicles like yours, and after reviewing the details, I'd love to discuss a potential purchase.

Based on our initial assessment:
• Vehicle: {vehicle}
• Mileage: {listing.get('mileage', 'N/A'):,} miles
• Our preliminary offer: ${offer_amount:,.0f}

Would you be available for a quick chat to discuss this further? I'd be happy to answer any questions and provide more details about our offer.

Looking forward to hearing from you!

Best regards,
{dealer_name}
{dealership_name}
{lead_data.get('dealer_phone', '')}"""
            },
            "follow_up_1": {
                "subject": f"Following up - {vehicle}",
                "body": f"""Hi {seller_name},

I wanted to follow up on my previous message about your {vehicle}. I understand you're probably busy, so I wanted to reach out again.

We're still very interested in your vehicle and our offer of ${offer_amount:,.0f} still stands. We can make the process quick and easy:

✓ Fast, hassle-free transaction
✓ Same-day payment available
✓ We handle all paperwork
✓ No hidden fees

Would you be open to discussing this further? Feel free to call or text me anytime.

Best,
{dealer_name}
{dealership_name}"""
            },
            "follow_up_2": {
                "subject": f"Final follow-up - {vehicle}",
                "body": f"""Hi {seller_name},

This is my final follow-up about your {vehicle}. I completely understand if you've already sold it or decided to keep it.

If you're still interested in selling, our offer of ${offer_amount:,.0f} remains available. We've had great success with similar vehicles and would love to add yours to our inventory.

No pressure at all - just wanted to make sure you had all the information you need to make the best decision.

Wishing you all the best,
{dealer_name}
{dealership_name}"""
            },
            "request_more_info": {
                "subject": f"Quick questions about your {vehicle}",
                "body": f"""Hi {seller_name},

Thank you for listing your {vehicle}! We're definitely interested, but I'd love to gather a bit more information to provide you with our best offer:

• Service history - do you have maintenance records?
• Any accidents or damage history?
• Current mechanical condition?
• Reason for selling?
• Timeline - when are you looking to sell?

Once I have these details, I can provide you with a comprehensive offer within 24 hours.

Thanks!
{dealer_name}
{dealership_name}"""
            }
        }
        
        return messages.get(template, messages["initial_contact"])
    
    def schedule_follow_ups(self, lead_id):
        """Generate follow-up schedule"""
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        
        return [
            {
                "lead_id": lead_id,
                "stage": 1,
                "scheduled_for": (now + timedelta(days=1)).isoformat(),
                "message_type": "follow_up_1"
            },
            {
                "lead_id": lead_id,
                "stage": 2,
                "scheduled_for": (now + timedelta(days=3)).isoformat(),
                "message_type": "follow_up_2"
            },
            {
                "lead_id": lead_id,
                "stage": 3,
                "scheduled_for": (now + timedelta(days=7)).isoformat(),
                "message_type": "follow_up_3"
            }
        ]