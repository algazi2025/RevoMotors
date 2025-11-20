from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RevoMotors API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes():
    return ["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi"]

@app.get("/api/cars/models")
def get_models(make: str):
    models = {
        "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
        "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
        "Ford": ["F-150", "Focus", "Mustang", "Explorer"],
        "BMW": ["3 Series", "5 Series", "X5", "X3"],
        "Mercedes": ["C-Class", "E-Class", "GLC", "A-Class"],
        "Audi": ["A4", "A6", "Q5", "Q7"],
    }
    return models.get(make, [])