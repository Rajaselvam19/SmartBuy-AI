from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    email: Optional[str] = None


# --- Category Schemas ---
class CategoryOut(BaseModel):
    id: int
    name: str
    icon_name: str
    slug: str

    class Config:
        from_attributes = True


# --- Product & Review Schemas ---
class ReviewOut(BaseModel):
    id: int
    rating: float
    positive_percent: float
    negative_percent: float
    pros: List[str]
    cons: List[str]

    class Config:
        from_attributes = True

class ProductOut(BaseModel):
    id: int
    name: str
    brand: str
    category_id: int
    price: float
    original_price: float
    discount_percent: float
    image_url: Optional[str] = None
    rating: float
    review_count: int
    availability: bool
    amazon_link: Optional[str] = None
    stock: int

    class Config:
        from_attributes = True

class ProductDetailOut(ProductOut):
    specs: Dict[str, Any]
    reviews: List[ReviewOut] = []

    class Config:
        from_attributes = True


# --- AI Router Schemas ---
class AIAnalyzeRequest(BaseModel):
    category_id: int
    budget_min: float
    budget_max: float
    brands: List[str]
    specifications: str = Field(..., max_length=300)
    other_preferences: str = Field(..., max_length=300)

class AIProductRecommendation(BaseModel):
    product_id: int
    match_score: int
    reasoning: str

class AIAnalyzeResponse(BaseModel):
    query_id: int
    recommendations: List[Dict[str, Any]]  # product details joined with score and reasoning

# Deep Analysis Subschemas
class ProductAgentData(BaseModel):
    pros: List[str]
    cons: List[str]

class ReviewAgentData(BaseModel):
    positive_pct: float
    negative_pct: float
    overall_rating: float
    summary: str

class PriceAgentData(BaseModel):
    current_price: float
    lowest_price: float
    trend: str  # "steady", "rising", or "falling"
    worth_buying: bool
    note: str

class RecommendationAgentData(BaseModel):
    why_this_product: str
    who_should_buy: List[str]
    alternatives: List[str]

class DecisionAgentData(BaseModel):
    final_score: int
    verdict: str
    confidence_pct: int

class AIDeepAnalysisResponse(BaseModel):
    product_agent: ProductAgentData
    review_agent: ReviewAgentData
    price_agent: PriceAgentData
    recommendation_agent: RecommendationAgentData
    decision_agent: DecisionAgentData


class AIWinnersRequest(BaseModel):
    product_ids: List[int]

class AIWinnerPodium(BaseModel):
    rank: int
    product: ProductOut
    match_score: int
    reasoning: Optional[str] = None


# --- User History & Wishlist Schemas ---
class SearchQueryOut(BaseModel):
    id: int
    category: CategoryOut
    budget_min: float
    budget_max: float
    brands: List[str]
    specifications: Optional[str] = None
    other_preferences: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class WishlistOut(BaseModel):
    id: int
    product: ProductOut

    class Config:
        from_attributes = True
