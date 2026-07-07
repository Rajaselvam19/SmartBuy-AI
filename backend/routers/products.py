from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from models.database import get_db
from models.models import Product, Category
from schemas.schemas import ProductOut, ProductDetailOut

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=List[ProductOut])
def get_products(
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
        
    if brand:
        query = query.filter(Product.brand.ilike(brand))
        
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
        
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    return query.all()

@router.get("/{product_id}", response_model=ProductDetailOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/similar", response_model=List[ProductOut])
def get_similar_products(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Find similar price range (+/- 25%) products in the same category (excluding current product)
    min_p = product.price * 0.75
    max_p = product.price * 1.25
    
    similar = db.query(Product).filter(
        and_(
            Product.category_id == product.category_id,
            Product.id != product.id,
            Product.price >= min_p,
            Product.price <= max_p
        )
    ).limit(5).all()
    
    # If not enough similar products, fall back to just same category excluding current product
    if len(similar) < 3:
        more_similar = db.query(Product).filter(
            and_(
                Product.category_id == product.category_id,
                Product.id != product.id
            )
        ).limit(5).all()
        # Merge without duplicates
        existing_ids = {s.id for s in similar}
        for p in more_similar:
            if p.id not in existing_ids:
                similar.append(p)
                if len(similar) >= 5:
                    break
                    
    return similar
