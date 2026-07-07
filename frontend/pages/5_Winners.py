import streamlit as st
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from styles import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartBuy AI - Podium Winners",
    page_icon="🏆",
    layout="wide"
)

inject_custom_css()

# Route protection
if not AuthHelper.is_logged_in():
    st.warning("Please log in to view this page.")
    st.switch_page("app.py")
    st.stop()

# Ensure podium product IDs exist
podium_ids = st.session_state.get("podium_ids")
if not podium_ids:
    st.warning("No products selected for comparison. Please go back to the Recommendations page.")
    if st.button("Go to Recommendations"):
        st.switch_page("pages/3_Results.py")
    st.stop()

# Sidebar Navigation
with st.sidebar:
    st.title("SmartBuy AI")
    st.markdown("---")
    if st.button("📊 Categories Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
    if st.button("🎯 Back to Results", use_container_width=True):
        st.switch_page("pages/3_Results.py")
    st.write("---")
    if st.button("🔓 Log Out", use_container_width=True):
        AuthHelper.logout()

# Page title
st.title("🏆 AI Recommendation Winners")
st.subheader("SmartBuy AI has analyzed and ranked the options on the podium:")

# Fetch podium rankings from API
with st.spinner("Ranking products..."):
    response = APIClient.post("/api/ai/winners", json_data={"product_ids": podium_ids})

if response and response.status_code == 200:
    winners = response.json()
    
    if len(winners) == 0:
        st.warning("No valid products were returned to rank.")
    else:
        # Build the HTML podium layout
        # We need to maps ranks (1, 2, 3) to their podium styles
        # Let's map winners elements
        rank_1 = next((w for w in winners if w["rank"] == 1), None)
        rank_2 = next((w for w in winners if w["rank"] == 2), None)
        rank_3 = next((w for w in winners if w["rank"] == 3), None)
        
        # Prepare HTML cards
        html_rank_1 = ""
        html_rank_2 = ""
        html_rank_3 = ""
        
        if rank_1:
            p = rank_1["product"]
            html_rank_1 = f"""<div class="podium-card podium-1">
<div class="podium-badge">🥇</div>
<div class="podium-rank" style="color:#B45309; font-weight:800;">Rank #1 (Gold)</div>
<div style="font-weight:700; color:#4F46E5; margin-bottom:0.25rem;">{p['brand']}</div>
<div style="font-size:0.95rem; font-weight:600; color:#1E1B4B; margin-bottom:0.75rem; height:45px; overflow:hidden;">{p['name']}</div>
<div style="font-size:1.4rem; font-weight:800; color:#10B981; margin-bottom:0.25rem;">₹{p['price']:.2f}</div>
<div style="font-size:0.85rem; color:#D97706; font-weight:bold; margin-bottom:1rem;">AI Match: {rank_1['match_score']}%</div>
</div>"""
            
        if rank_2:
            p = rank_2["product"]
            html_rank_2 = f"""<div class="podium-card podium-2">
<div class="podium-badge">🥈</div>
<div class="podium-rank" style="color:#4B5563; font-weight:800;">Rank #2 (Silver)</div>
<div style="font-weight:700; color:#4F46E5; margin-bottom:0.25rem;">{p['brand']}</div>
<div style="font-size:0.9rem; font-weight:600; color:#1E1B4B; margin-bottom:0.75rem; height:40px; overflow:hidden;">{p['name']}</div>
<div style="font-size:1.25rem; font-weight:700; color:#10B981; margin-bottom:0.25rem;">₹{p['price']:.2f}</div>
<div style="font-size:0.8rem; color:#D97706; font-weight:bold; margin-bottom:1rem;">AI Match: {rank_2['match_score']}%</div>
</div>"""
            
        if rank_3:
            p = rank_3["product"]
            html_rank_3 = f"""<div class="podium-card podium-3">
<div class="podium-badge">🥉</div>
<div class="podium-rank" style="color:#B45309; font-weight:800;">Rank #3 (Bronze)</div>
<div style="font-weight:700; color:#4F46E5; margin-bottom:0.25rem;">{p['brand']}</div>
<div style="font-size:0.85rem; font-weight:600; color:#1E1B4B; margin-bottom:0.75rem; height:40px; overflow:hidden;">{p['name']}</div>
<div style="font-size:1.15rem; font-weight:700; color:#10B981; margin-bottom:0.25rem;">₹{p['price']:.2f}</div>
<div style="font-size:0.75rem; color:#D97706; font-weight:bold; margin-bottom:1rem;">AI Match: {rank_3['match_score']}%</div>
</div>"""
            
        # Combine into custom podium flex row
        podium_html = f"""<div class="podium-container">
{html_rank_2}
{html_rank_1}
{html_rank_3}
</div>"""
        st.markdown(podium_html, unsafe_allow_html=True)
        
        # Interactive Detail Buttons directly beneath the podium
        st.write("")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if rank_2 and st.button("🔍 View #2 details", key="view_podium_2", use_container_width=True):
                st.session_state["selected_product_id"] = rank_2["product"]["id"]
                st.switch_page("pages/4_ProductDetail.py")
        with col_btn2:
            if rank_1 and st.button("🔥 View #1 details", key="view_podium_1", use_container_width=True):
                st.session_state["selected_product_id"] = rank_1["product"]["id"]
                st.switch_page("pages/4_ProductDetail.py")
        with col_btn3:
            if rank_3 and st.button("🔍 View #3 details", key="view_podium_3", use_container_width=True):
                st.session_state["selected_product_id"] = rank_3["product"]["id"]
                st.switch_page("pages/4_ProductDetail.py")

        # Side-by-side Specifications Comparison Table
        st.markdown("---")
        st.markdown('<h3 class="section-title">⚖️ Side-by-Side Comparison</h3>', unsafe_allow_html=True)
        
        # Compile specifications keys dynamically
        spec_keys = set()
        for w in winners:
            spec_keys.update(w["product"].get("specs", {}).keys())
        spec_keys = sorted(list(spec_keys))
        
        features = ["Brand", "Price", "Original Price", "Discount %", "Rating"] + spec_keys
        
        # Build comparison dictionary
        comp_data = {}
        comp_data["Feature"] = features
        
        for w in winners:
            p = w["product"]
            specs = p.get("specs", {})
            col_name = f"🏆 Rank #{w['rank']} ({p['brand']})"
            
            row_values = [
                p["brand"],
                f"₹{p['price']:.2f}",
                f"₹{p['original_price']:.2f}",
                f"{p['discount_percent']:.0f}%",
                f"⭐ {p['rating']:.1f} ({p['review_count']} reviews)"
            ]
            for k in spec_keys:
                row_values.append(specs.get(k, "N/A"))
                
            comp_data[col_name] = row_values
            
        import pandas as pd
        df_comp = pd.DataFrame(comp_data)
        st.table(df_comp.set_index("Feature"))

        # Footer Actions
        st.markdown("---")
        footer_col1, footer_col2 = st.columns(2)
        with footer_col1:
            if st.button("🔄 Start New Search", use_container_width=True):
                st.session_state["selected_category"] = None
                st.session_state["query_results"] = None
                st.session_state["compare_list"] = []
                st.switch_page("pages/1_Dashboard.py")
        with footer_col2:
            if st.button("📋 Go back to recommendations", use_container_width=True):
                st.switch_page("pages/3_Results.py")
else:
    st.error("Failed to load podium winners.")
