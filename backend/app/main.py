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

@app.get("/")
def root():
    return {"status": "ready", "service": "RevoMotors API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/cars/makes")
def get_makes():
    return ["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi", "Volkswagen", "Chevrolet", "Ford", "Nissan"]

@app.get("/api/cars/models")
def get_models(make: str):
    models = {
        "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Prius"],
        "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
        "Ford": ["F-150", "Focus", "Mustang", "Explorer", "Edge"],
        "BMW": ["3 Series", "5 Series", "X5", "X3", "X1"],
        "Mercedes": ["C-Class", "E-Class", "GLC", "A-Class", "S-Class"],
        "Audi": ["A4", "A6", "Q5", "Q7", "A3"],
        "Volkswagen": ["Jetta", "Passat", "Golf", "Tiguan", "Atlas"],
        "Chevrolet": ["Malibu", "Cruze", "Traverse", "Equinox", "Blazer"],
        "Nissan": ["Altima", "Sentra", "Rogue", "Murano", "Pathfinder"],
    }
    return models.get(make, [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)