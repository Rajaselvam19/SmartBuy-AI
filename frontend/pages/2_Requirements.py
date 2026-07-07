import streamlit as st
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from styles import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartBuy AI - Requirements",
    page_icon="📋",
    layout="wide"
)

inject_custom_css()

# Route protection
if not AuthHelper.is_logged_in():
    st.warning("Please log in to view this page.")
    st.switch_page("app.py")
    st.stop()

# Ensure category is selected
selected_category = st.session_state.get("selected_category")
if not selected_category:
    st.warning("Please select a category from the Dashboard first.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# Sidebar navigation
with st.sidebar:
    st.title("SmartBuy AI")
    st.write(f"Category: **{selected_category['name']}**")
    st.markdown("---")
    if st.button("📊 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
    st.write("---")
    if st.button("🔓 Log Out", use_container_width=True):
        AuthHelper.logout()

# Page title
st.title("📋 Define Your Requirements")
st.subheader(f"Finding the best match for **{selected_category['name']}**")

# Fetch available brands dynamically from products in the database
with st.spinner("Fetching available brands..."):
    products_response = APIClient.get("/api/products", params={"category_id": selected_category["id"]})
    
available_brands = []
if products_response and products_response.status_code == 200:
    prods = products_response.json()
    available_brands = sorted(list(set(p["brand"] for p in prods)))

if not available_brands:
    st.warning("⚠️ No products or brands are currently seeded in the database for this category.")

# Form layout
with st.form("requirements_form"):
    st.markdown("#### Enter your shopping preferences:")
    
    # 1. Dynamic Budget slider in INR (₹)
    cat_slug = selected_category["slug"]
    if cat_slug == "mobiles":
        min_b, max_b, val_b, step_b = 5000, 150000, (15000, 40000), 1000
    elif cat_slug == "laptops":
        min_b, max_b, val_b, step_b = 20000, 250000, (40000, 100000), 2000
    elif cat_slug == "headphones":
        min_b, max_b, val_b, step_b = 500, 50000, (1000, 15000), 500
    else:
        min_b, max_b, val_b, step_b = 500, 300000, (2000, 50000), 1000

    budget_range = st.slider(
        "Select your Budget Range (₹)",
        min_value=min_b,
        max_value=max_b,
        value=val_b,
        step=step_b,
        help="Specify the minimum and maximum amount in Indian Rupees you are willing to spend."
    )
    
    # 2. Brand multiselect
    selected_brands = st.multiselect(
        "Preferred Brands",
        options=available_brands,
        default=[],
        help="Select one or more brands. Leave empty if you don't have a preference."
    )
    
    # 3. Technical specifications text-area
    specs_input = st.text_area(
        "Technical Specifications / Hardware Requirements",
        value="",
        max_chars=300,
        placeholder="e.g., AMOLED display, 8 GB RAM, 128 GB storage, fast charging",
        help="Detail any specific technical features, hardware, or ports you absolutely need."
    )
    
    # 4. Other preferences text-area
    other_input = st.text_area(
        "Other Preferences & Usage Needs",
        value="",
        max_chars=300,
        placeholder="e.g., Good camera and long battery life, lightweight, comfortable key travel",
        help="Describe what you will use the product for or any additional features like battery, webcam, color, etc."
    )
    
    submit_btn = st.form_submit_button("Analyze & Find Best Products 🚀")
 
if submit_btn:
    # Build API payload
    payload = {
        "category_id": selected_category["id"],
        "budget_min": float(budget_range[0]),
        "budget_max": float(budget_range[1]),
        "brands": selected_brands,
        "specifications": specs_input if specs_input.strip() else "None",
        "other_preferences": other_input if other_input.strip() else "None"
    }
    
    with st.spinner("SmartBuy AI agents are analyzing products and checking matches..."):
        response = APIClient.post("/api/ai/analyze", json_data=payload)
        
        if response and response.status_code == 200:
            results_data = response.json()
            st.session_state["query_results"] = results_data
            st.success("Analysis complete! Showing top matches.")
            st.switch_page("pages/3_Results.py")
        elif response:
            error_msg = response.json().get("detail", "Failed to run analysis.")
            st.error(f"Error: {error_msg}")
        else:
            st.error("No response from server. Please verify backend state.")
 
# Live Selection Summary columns (shown outside form so it updates live on slider movement)
st.markdown("---")
st.markdown("### 📊 Selections Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Budget Range", f"₹{budget_range[0]} - ₹{budget_range[1]}")
with col2:
    st.write("**Preferred Brands:**")
    st.write(", ".join(selected_brands) if selected_brands else "Any Brand")
with col3:
    st.write("**Category:**")
    st.write(selected_category["name"])
