# SmartBuy AI - Full-Stack AI-Powered Shopping Assistant

SmartBuy AI is a complete, full-stack shopping assistant web application built 100% in Python. It features a FastAPI backend REST API, a Streamlit multi-page frontend, a SQLAlchemy/SQLite database, JWT authentication, and Anthropic Claude integration for recommendations and multi-agent analysis.

---

## 📁 Project Structure

```
/smartbuy_ai
  /backend
    main.py                       # FastAPI application entry point
    seed_data.py                  # Database populate script for mock laptops & categories
    requirements.txt              # Backend library dependencies
    /models
      database.py                 # SQLAlchemy engine and session setup
      models.py                   # SQLAlchemy ORM models
    /schemas
      schemas.py                  # Pydantic data validation models
    /routers
      auth.py                     # Authentication endpoints
      categories.py               # Categories endpoints
      products.py                 # Products search and details endpoints
      ai.py                       # LLM recommend, deep-analysis, and winners endpoints
      user.py                     # Wishlist and history query endpoints
    /services
      ai_service.py               # Anthropic Claude SDK client & recommendation engine
      auth_service.py             # Authentication middleware dependency
    /core
      config.py                   # Env configurations loading
      security.py                 # Password hashing & JWT helpers
  /frontend
    app.py                        # Streamlit login/register entry point
    styles.py                     # Custom dark theme CSS and progress badges
    requirements.txt              # Frontend library dependencies
    /pages
      1_Dashboard.py              # Category selection grid, wishlist & history overview
      2_Requirements.py           # User filters form (budget, brand, specs, usage)
      3_Results.py                # Recommended products list, AI reasons, wishlist addition
      4_ProductDetail.py          # 5 tabs: Multi-agent AI breakdown, specs table, reviews
      5_Winners.py                # 3D podium for top 3 & side-by-side spec comparisons
    /utils
      api_client.py               # API request wrappers with header token injects
      auth_helper.py              # Front-end login, register, logout helpers
  .env                            # Project environment parameters
```

---

## 🛠️ Setup Instructions

### Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### 1. Environment Configuration
Create or modify the `.env` file in the root directory:
```env
JWT_SECRET_KEY=7c21340bdfa357f88469ad03be3a4ff13554e2cf8649033f91deba2a4666cf6d
DATABASE_URL=sqlite:///./smartbuy_ai.db

# Replace this with your actual Anthropic API key to enable live Claude recommendations
# If left as default, the application will run in simulated fallback offline mode
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 2. Install Backend & Seed Database
Open a terminal in the `/backend` folder, install requirements, and seed the database:
```bash
cd backend
pip install -r requirements.txt
python seed_data.py
```
*(This creates `smartbuy_ai.db` in the backend folder containing 23 shopping categories and 18 high-quality laptop products with reviews, specs, discounts, and prices).*

### 3. Run Backend API Server
Start the Uvicorn FastAPI server on port 8000:
```bash
uvicorn main:app --reload
```
*(The server will reload automatically on code changes. Swagger UI is available at `http://localhost:8000/docs`).*

### 4. Install Frontend & Run Streamlit
Open a separate terminal in the `/frontend` folder, install requirements, and run the Streamlit app:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
*(The Streamlit app will start and run on `http://localhost:8501`).*

---

## 🤖 SmartBuy AI Agents Architecture

SmartBuy AI deploys 5 specialized AI agents during deep product analysis:
1. **📦 Product Agent (Green)**: Extracts exact pros, cons, and hardware features from the technical specification sheets.
2. **💬 Review Agent (Blue)**: Analyzes user review counts, performs sentiment polarity scores, and compiles a comprehensive summary of buyers' opinions.
3. **📉 Price Agent (Purple)**: Tracks catalog price drops, checks if the discount is genuine, identifies historical lows, and rates purchasing timing.
4. **💡 Recommendation Agent (Orange)**: Identifies target user demographics (e.g. students, coders, gamers) and lists matching alternative models.
5. **🏆 Decision Agent (Teal)**: Calculates a final weighted match score out of 100, presents confidence metrics, and provides a final verdict.
