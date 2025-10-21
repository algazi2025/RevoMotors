from datetime import datetime

class MockAIProvider:
    def estimate_offer(self, year, make, model, mileage, condition, region, comps=None):
        age = datetime.now().year - year
        base = max(3000, 25000 - age * 2000)
        fair = base
        return {"low": round(fair * 0.7, 2), "fair": round(fair, 2), "max": round(fair * 1.15, 2), 
                "rationale": f"{year} {make} {model}"}

ai_provider = MockAIProvider()
