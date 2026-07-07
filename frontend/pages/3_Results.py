import streamlit as st
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from styles import inject_custom_css, render_match_badge

# Page Configuration
st.set_page_config(
    page_title="SmartBuy AI - Recommendations",
    page_icon="🎯",
    layout="wide"
)

def get_clear_image_url(url: str) -> str:
    if "unsplash.com" in url:
        if "w=400" in url:
            return url.replace("w=400", "w=800").replace("q=80", "q=95")
    return url


inject_custom_css()

# Route protection
if not AuthHelper.is_logged_in():
    st.warning("Please log in to view this page.")
    st.switch_page("app.py")
    st.stop()

# Ensure search results exist
query_results = st.session_state.get("query_results")
if not query_results:
    st.warning("No recommendations available. Please configure your requirements first.")
    if st.button("Go to Requirements"):
        st.switch_page("pages/2_Requirements.py")
    st.stop()

# Sidebar Navigation
with st.sidebar:
    st.title("SmartBuy AI")
    st.markdown("---")
    if st.button("📊 Categories Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
    if st.button("📋 Adjust Requirements", use_container_width=True):
        st.switch_page("pages/2_Requirements.py")
    st.write("---")
    if st.button("🔓 Log Out", use_container_width=True):
        AuthHelper.logout()

# Page title
st.title("🎯 Your AI recommendations")
st.subheader("SmartBuy AI has analyzed the database and ranked the best options:")

# Extract list of products
recommendations = query_results.get("recommendations", [])

if not recommendations:
    st.info("No products matched your exact search query. Please try widening your budget or selecting fewer brands.")
else:
    # Initialize compare checkbox state list
    if "compare_list" not in st.session_state:
        st.session_state["compare_list"] = []

    # Display items in a beautiful responsive layout
    # We will display products vertically as styled horizontal rows or a grid.
    # A grid with st.columns(2) is perfect.
    
    # Top Actions Row: Compare and Podium
    top_col1, top_col2 = st.columns([2, 1])
    with top_col1:
        st.write("💡 Check items you wish to compare, then click **Compare Selected** or view the podium.")
    with top_col2:
        # Collect top 3 product IDs for default podium
        top_3_ids = [p["id"] for p in recommendations[:3]]
        if st.button("🏆 Show Top 3 Podium Winners", use_container_width=True):
            st.session_state["podium_ids"] = top_3_ids
            st.switch_page("pages/5_Winners.py")

    st.markdown("---")

    grid_cols = st.columns(2)
    for idx, p in enumerate(recommendations):
        col_index = idx % 2
        with grid_cols[col_index]:
            # Create a card layout using Markdown
            badge_html = render_match_badge(p["match_score"])
            
            st.markdown(
                f"""
                <div class="product-card">
                    <div style="display: flex; gap: 1rem; align-items: start;">
                        <img src="{get_clear_image_url(p['image_url'])}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px; border: 1px solid #E2E1F3;"/>
                        <div style="flex-grow: 1;">
                            <span style="font-size: 0.8rem; text-transform: uppercase; color: #7C3AED; font-weight: 700;">{p['brand']}</span>
                            <h4 style="margin: 0; color: #1E1B4B; font-size: 1.15rem; font-weight: 600;">{p['name']}</h4>
                            <div style="margin-top: 0.25rem; display: flex; align-items: center; gap: 0.5rem;">
                                <span style="color: #F59E0B; font-weight: bold;">⭐ {p['rating']:.1f}</span>
                                <span style="color: #6B7280; font-size: 0.85rem;">({p['review_count']} reviews)</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <span class="price-tag">₹{p['price']:.2f}</span>
                                <span class="original-price-tag">₹{p['original_price']:.2f}</span>
                                <span class="discount-badge">{p['discount_percent']:.0f}% OFF</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                {badge_html}
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; border-top: 1px solid #E2E1F3; padding-top: 0.75rem;">
                        <p style="font-size: 0.9rem; font-style: italic; color: #374151; line-height: 1.4;">
                            <strong>AI Reasoning:</strong> {p['reasoning']}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Interactive Streamlit buttons underneath each HTML card
            btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])
            with btn_col1:
                if st.button("🔍 View AI Agent Details", key=f"details_btn_{p['id']}", use_container_width=True):
                    st.session_state["selected_product_id"] = p["id"]
                    st.switch_page("pages/4_ProductDetail.py")
            with btn_col2:
                # Wishlist toggle button
                # Verify if currently in wishlist
                wish_response = APIClient.get("/api/user/wishlist")
                is_wishlisted = False
                if wish_response and wish_response.status_code == 200:
                    wishlist = wish_response.json()
                    is_wishlisted = any(w["product"]["id"] == p["id"] for w in wishlist)
                
                wish_btn_text = "❤️ Remove Wishlist" if is_wishlisted else "🤍 Add Wishlist"
                if st.button(wish_btn_text, key=f"wish_btn_{p['id']}", use_container_width=True):
                    if is_wishlisted:
                        APIClient.delete(f"/api/user/wishlist/{p['id']}")
                    else:
                        APIClient.post(f"/api/user/wishlist/{p['id']}")
                    st.rerun()
            with btn_col3:
                # Comparison list management
                is_compared = p["id"] in st.session_state["compare_list"]
                compare_checkbox = st.checkbox("Compare", value=is_compared, key=f"comp_check_{p['id']}")
                if compare_checkbox and p["id"] not in st.session_state["compare_list"]:
                    if len(st.session_state["compare_list"]) >= 3:
                        st.error("You can compare up to 3 products maximum.")
                        st.session_state["compare_list"].append(p["id"]) # temporarily append, will slice
                        st.session_state["compare_list"] = st.session_state["compare_list"][:3]
                    else:
                        st.session_state["compare_list"].append(p["id"])
                elif not compare_checkbox and p["id"] in st.session_state["compare_list"]:
                    st.session_state["compare_list"].remove(p["id"])
            
            st.write("") # small spacer

    # Bottom Actions
    st.markdown("---")
    bot_col1, bot_col2 = st.columns([2, 1])
    with bot_col1:
        st.write(f"Items selected for comparison: **{len(st.session_state['compare_list'])}** (Max 3)")
    with bot_col2:
        if st.button("⚖️ Compare Selected Items", use_container_width=True):
            if not st.session_state["compare_list"]:
                st.warning("Please select at least one product using the 'Compare' checkbox.")
            else:
                st.session_state["podium_ids"] = st.session_state["compare_list"]
                st.switch_page("pages/5_Winners.py")
