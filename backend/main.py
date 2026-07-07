from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import engine, Base
from models import models  # Ensure models are loaded for table creation
from routers import auth, categories, products, ai, user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartBuy AI - Backend API",
    description="Python + FastAPI REST API backend with SQLite database and Anthropic Claude recommendations",
    version="1.0.0"
)

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to specific domains like http://localhost:8501 in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(ai.router)
app.include_router(user.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
