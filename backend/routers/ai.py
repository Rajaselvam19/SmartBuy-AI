from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict, Any
import json
from models.database import get_db
from models.models import Product, SearchQuery, AIResult, Review, User
from schemas.schemas import AIAnalyzeRequest, AIAnalyzeResponse, AIDeepAnalysisResponse, AIWinnersRequest, AIWinnerPodium
from services.auth_service import get_current_user
from services.ai_service import get_ai_recommendations, get_deep_analysis

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/analyze", response_model=AIAnalyzeResponse)
def analyze_and_recommend(
    body: AIAnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Save user query in database
    search_query = SearchQuery(
        user_id=current_user.id,
        category_id=body.category_id,
        budget_min=body.budget_min,
        budget_max=body.budget_max,
        brands=body.brands,
        specifications=body.specifications,
        other_preferences=body.other_preferences
    )
    db.add(search_query)
    db.commit()
    db.refresh(search_query)

    # 2. Filter products from database
    # Get all products in the category first
    query = db.query(Product).filter(Product.category_id == body.category_id)
    
    # Apply brand filter if specified
    if body.brands:
        query = query.filter(Product.brand.in_(body.brands))
        
    # Apply loose price filter (allow up to 20% over budget_max to give AI flexibility)
    query = query.filter(Product.price >= body.budget_min * 0.8)
    query = query.filter(Product.price <= body.budget_max * 1.2)
    
    products = query.all()
    
    # Fallback: if no products found with strict filters, broaden search to all products in the category
    if not products:
        products = db.query(Product).filter(Product.category_id == body.category_id).all()
        
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found in this category to analyze."
        )

    # 3. Call AI Service to get recommendations
    # Format products for AI service
    products_list = []
    for p in products:
        products_list.append({
            "id": p.id,
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "original_price": p.original_price,
            "discount_percent": p.discount_percent,
            "specs": p.specs,
            "rating": p.rating,
            "review_count": p.review_count
        })
        
    requirements = {
        "budget_min": body.budget_min,
        "budget_max": body.budget_max,
        "brands": body.brands,
        "specifications": body.specifications,
        "other_preferences": body.other_preferences
    }
    
    ai_recs = get_ai_recommendations(products_list, requirements)
    
    # 4. Save results to database (AIResult table) and prepare response
    # We will sort by match score descending and save top 5
    ai_recs.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    top_recs = ai_recs[:5]
    
    response_recs = []
    for rank, rec in enumerate(top_recs, start=1):
        product_id = rec["product_id"]
        match_score = rec["match_score"]
        reasoning = rec.get("reasoning", "")
        
        # Verify product exists in db
        db_prod = db.query(Product).filter(Product.id == product_id).first()
        if not db_prod:
            continue
            
        # Create AIResult record
        ai_res = AIResult(
            query_id=search_query.id,
            product_id=product_id,
            match_score=match_score,
            ai_analysis={"reasoning": reasoning}, # Simple default, will be populated on deep analysis
            rank=rank
        )
        db.add(ai_res)
        
        # Build response item (merging product details with AI results)
        prod_data = {
            "id": db_prod.id,
            "name": db_prod.name,
            "brand": db_prod.brand,
            "category_id": db_prod.category_id,
            "price": db_prod.price,
            "original_price": db_prod.original_price,
            "discount_percent": db_prod.discount_percent,
            "image_url": db_prod.image_url,
            "rating": db_prod.rating,
            "review_count": db_prod.review_count,
            "availability": db_prod.availability,
            "amazon_link": db_prod.amazon_link,
            "stock": db_prod.stock,
            "match_score": match_score,
            "reasoning": reasoning
        }
        response_recs.append(prod_data)
        
    db.commit()
    
    return {
        "query_id": search_query.id,
        "recommendations": response_recs
    }

@router.post("/deep-analysis/{product_id}", response_model=AIDeepAnalysisResponse)
def get_product_deep_analysis(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Get reviews
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    
    # Format for Claude
    prod_data = {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "original_price": product.original_price,
        "discount_percent": product.discount_percent,
        "specs": product.specs,
        "rating": product.rating,
        "review_count": product.review_count
    }
    
    reviews_data = []
    for r in reviews:
        reviews_data.append({
            "rating": r.rating,
            "positive_percent": r.positive_percent,
            "negative_percent": r.negative_percent,
            "pros": r.pros,
            "cons": r.cons
        })
        
    analysis_json = get_deep_analysis(prod_data, reviews_data)
    
    # Save the deep analysis details in the latest AIResult record for this product and user (if exists)
    # Find latest query for this user
    latest_query = db.query(SearchQuery).filter(SearchQuery.user_id == current_user.id).order_by(desc(SearchQuery.created_at)).first()
    if latest_query:
        ai_res = db.query(AIResult).filter(
            AIResult.query_id == latest_query.id,
            AIResult.product_id == product_id
        ).first()
        if ai_res:
            ai_res.ai_analysis = analysis_json
            db.commit()
            
    return analysis_json

@router.post("/winners", response_model=List[AIWinnerPodium])
def get_podium_winners(
    body: AIWinnersRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product_ids = body.product_ids
    if not product_ids:
        raise HTTPException(status_code=400, detail="Product ID list cannot be empty")
        
    # Get the latest SearchQuery for the current user to find corresponding match scores
    latest_query = db.query(SearchQuery).filter(SearchQuery.user_id == current_user.id).order_by(desc(SearchQuery.created_at)).first()
    
    podium_list = []
    for pid in product_ids:
        prod = db.query(Product).filter(Product.id == pid).first()
        if not prod:
            continue
            
        # Default match score if not found in database AIResult for latest query
        match_score = int(prod.rating * 20)  # e.g., 4.5 rating -> 90 score
        reasoning = "Top rated product based on specifications and quality reviews."
        
        if latest_query:
            ai_res = db.query(AIResult).filter(
                AIResult.query_id == latest_query.id,
                AIResult.product_id == pid
            ).first()
            if ai_res:
                match_score = ai_res.match_score
                if ai_res.ai_analysis and "reasoning" in ai_res.ai_analysis:
                    reasoning = ai_res.ai_analysis["reasoning"]
                elif ai_res.ai_analysis and "decision_agent" in ai_res.ai_analysis:
                    reasoning = ai_res.ai_analysis["decision_agent"].get("verdict", reasoning)
                    
        podium_list.append({
            "product": prod,
            "match_score": match_score,
            "reasoning": reasoning
        })
        
    # Sort by match score descending
    podium_list.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Format response with ranks (up to top 3)
    response = []
    for idx, item in enumerate(podium_list[:3]):
        response.append({
            "rank": idx + 1,
            "product": item["product"],
            "match_score": item["match_score"],
            "reasoning": item["reasoning"]
        })
        
    return response
