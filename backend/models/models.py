import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from models.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    queries = relationship("SearchQuery", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)  # e.g., laptop, smartphone, etc.
    slug = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    queries = relationship("SearchQuery", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0.0)
    specs = Column(JSON, nullable=False)  # Dictionary of specifications
    image_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    availability = Column(Boolean, default=True)
    amazon_link = Column(String, nullable=True)
    stock = Column(Integer, default=10)

    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    ai_results = relationship("AIResult", back_populates="product", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)
    positive_percent = Column(Float, nullable=False)
    negative_percent = Column(Float, nullable=False)
    pros = Column(JSON, nullable=False)  # List of pros
    cons = Column(JSON, nullable=False)  # List of cons

    product = relationship("Product", back_populates="reviews")


class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    brands = Column(JSON, nullable=False)  # List of brands
    specifications = Column(String, nullable=True)
    other_preferences = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="queries")
    category = relationship("Category", back_populates="queries")
    ai_results = relationship("AIResult", back_populates="query", cascade="all, delete-orphan")


class AIResult(Base):
    __tablename__ = "ai_results"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("search_queries.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Integer, nullable=False)
    ai_analysis = Column(JSON, nullable=True)  # Detailed 5-agent analysis stored here
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    query = relationship("SearchQuery", back_populates="ai_results")
    product = relationship("Product", back_populates="ai_results")


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")
