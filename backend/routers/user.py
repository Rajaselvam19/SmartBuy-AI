from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from models.models import Wishlist, Product, SearchQuery, User
from schemas.schemas import WishlistOut, SearchQueryOut
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/wishlist/{product_id}", status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    product_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Check if already in wishlist
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()
    if existing:
        return {"message": "Product already in wishlist"}
        
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.add(wishlist_item)
    db.commit()
    return {"message": "Product added to wishlist"}

@router.delete("/wishlist/{product_id}")
def remove_from_wishlist(
    product_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
        
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Product removed from wishlist"}

@router.get("/wishlist", response_model=List[WishlistOut])
def get_wishlist(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()

@router.get("/history", response_model=List[SearchQueryOut])
def get_history(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return db.query(SearchQuery).filter(
        SearchQuery.user_id == current_user.id
    ).order_by(SearchQuery.created_at.desc()).all()
