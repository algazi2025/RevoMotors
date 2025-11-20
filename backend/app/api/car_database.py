from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test():
    return {"status": "router working"}

@router.get("/makes")
def get_makes():
    return ["Toyota", "Honda", "Ford"]