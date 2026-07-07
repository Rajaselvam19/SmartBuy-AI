from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from models.models import Category
from schemas.schemas import CategoryOut

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
