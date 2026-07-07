import streamlit as st
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from styles import inject_custom_css

# Page configuration
st.set_page_config(
    page_title="SmartBuy AI - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Inject styling
inject_custom_css()

# Protect route
if not AuthHelper.is_logged_in():
    st.warning("Please log in to access the Dashboard.")
    st.switch_page("app.py")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("SmartBuy AI")
    st.write(f"Logged in as: **{st.session_state['user']['name']}**")
    st.markdown("---")
    
    # Custom Sidebar Navigation Buttons
    if st.button("🏠 Home / Login Screen", use_container_width=True):
        st.switch_page("app.py")
        
    st.write("---")
    if st.button("🔓 Log Out", use_container_width=True):
        AuthHelper.logout()

# Main Dashboard Content
st.title("📊 Categories Dashboard")
st.subheader("Select a shopping category below to start your AI search")

# Fetch categories from API
with st.spinner("Loading categories..."):
    response = APIClient.get("/api/categories")

# Category Icon Map
ICON_MAP = {
    "mobiles": "📱",
    "laptops": "💻",
    "tablets": "📟",
    "smart-watches": "⌚",
    "headphones": "🎧",
    "cameras": "📷",
    "tvs": "📺",
    "home-appliances": "🏠",
    "kitchen-appliances": "🍳",
    "furniture": "🪑",
    "clothing": "👕",
    "shoes": "👟",
    "beauty-products": "💄",
    "grocery": "🛒",
    "books": "📚",
    "gaming": "🎮",
    "car-accessories": "🚗",
    "bike-accessories": "🚲",
    "fitness-equipment": "🏋️",
    "office-products": "💼",
    "baby-products": "🍼",
    "pet-products": "🐶",
    "medical-devices": "🩺"
}

if response and response.status_code == 200:
    categories = response.json()
    
    # Render categories in columns
    # We want a grid layout (e.g., 4 columns)
    cols = st.columns(4)
    for index, category in enumerate(categories):
        col_index = index % 4
        with cols[col_index]:
            emoji = ICON_MAP.get(category["slug"], "🛍️")
            
            # Draw a nice container with Markdown/HTML style and a button inside
            st.markdown(
                f"""
                <div class="category-card" style="margin-bottom: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{emoji}</div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: #F8FAFC; margin-bottom: 0.75rem;">{category['name']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button(f"Search {category['name']}", key=f"cat_btn_{category['id']}", use_container_width=True):
                st.session_state["selected_category"] = category
                st.switch_page("pages/2_Requirements.py")
else:
    st.error("Failed to load categories. Please check backend seed status.")
    
# Bottom section: Wishlist and Search History Summary
st.markdown("---")
st.markdown('<h3 class="section-title">👤 Your Activity Portal</h3>', unsafe_allow_html=True)

# Use beautiful tabs to present this cleanly
tab_wish, tab_hist = st.tabs(["❤️ My Wishlist Favorites", "📜 Recent Search Queries"])

with tab_wish:
    wish_response = APIClient.get("/api/user/wishlist")
    if wish_response and wish_response.status_code == 200:
        wishlist = wish_response.json()
        if not wishlist:
            st.info("Your wishlist is empty. Browse products and click the heart icon to save them!")
        else:
            for item in wishlist:
                prod = item["product"]
                col_item_left, col_item_right = st.columns([5, 1])
                with col_item_left:
                    st.markdown(f"**{prod['brand']}** {prod['name']} — <span style='color:#10B981; font-weight:bold;'>₹{prod['price']:.2f}</span>", unsafe_allow_html=True)
                with col_item_right:
                    if st.button("View Product Detail", key=f"wish_view_{prod['id']}", use_container_width=True):
                        st.session_state["selected_product_id"] = prod["id"]
                        st.switch_page("pages/4_ProductDetail.py")
    else:
        st.write("Could not retrieve wishlist.")

with tab_hist:
    hist_response = APIClient.get("/api/user/history")
    if hist_response and hist_response.status_code == 200:
        history = hist_response.json()
        if not history:
            st.info("No past search history found. Start searching above!")
        else:
            for query in history:
                st.markdown(f"🔍 Search for **{query['category']['name']}** (Budget: ₹{query['budget_min']:.0f} - ₹{query['budget_max']:.0f})")
                st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;*Specs requested: {query['specifications'] or 'None'}*")
                st.markdown('<hr style="margin:0.25rem 0; border-color:#2D254F;"/>', unsafe_allow_html=True)
    else:
        st.write("Could not retrieve search history.")
