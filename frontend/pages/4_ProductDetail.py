import streamlit as st
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from styles import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartBuy AI - Product Details",
    page_icon="🔍",
    layout="wide"
)

def get_clear_image_url(url: str) -> str:
    if "unsplash.com" in url:
        if "w=400" in url:
            return url.replace("w=400", "w=800").replace("q=80", "q=95")
    return url

def select_similar_product(pid):
    st.session_state["selected_product_id"] = pid
    st.switch_page("pages/4_ProductDetail.py")



inject_custom_css()

# Route protection
if not AuthHelper.is_logged_in():
    st.warning("Please log in to view this page.")
    st.switch_page("app.py")
    st.stop()

# Ensure product selected
product_id = st.session_state.get("selected_product_id")
if not product_id:
    st.warning("No product selected. Please view details from the Results page.")
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

# Fetch product detail
with st.spinner("Fetching product details..."):
    prod_response = APIClient.get(f"/api/products/{product_id}")

if prod_response and prod_response.status_code == 200:
    product = prod_response.json()
    
    # Header display
    col_hdr1, col_hdr2 = st.columns([1, 4])
    with col_hdr1:
        st.markdown(f'<div style="display: flex; justify-content: center;"><img src="{get_clear_image_url(product["image_url"])}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 12px; border: 1px solid #E2E1F3;"/></div>', unsafe_allow_html=True)
    with col_hdr2:
        st.write(f"**{product['brand']}**")
        st.title(product["name"])
        
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Price", f"₹{product['price']:.2f}", f"-{product['discount_percent']:.0f}% Original: ₹{product['original_price']:.2f}")
        with col_stats2:
            st.metric("Rating", f"⭐ {product['rating']:.1f}", f"{product['review_count']} user reviews")
        with col_stats3:
            avail_str = "In Stock" if product["availability"] else "Out of Stock"
            st.metric("Availability", avail_str, f"Stock: {product['stock']}")

    # Tabs definition
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 Multi-Agent AI Analysis", 
        "📋 Specifications", 
        "💬 Customer Reviews", 
        "📉 Price History & Trend", 
        "🔄 Similar Products"
    ])

    # 1. AI Analysis Tab
    with tab1:
        st.subheader("🤖 SmartBuy Multi-Agent Deep Analysis")
        st.write("Specialized LLM agents have processed this product details and reviews to provide a detailed breakdown:")
        
        with st.spinner("Invoking AI agents for deep analysis (Product, Review, Price, Recommendation, Decision)..."):
            ai_response = APIClient.post(f"/api/ai/deep-analysis/{product_id}")
            
        if ai_response and ai_response.status_code == 200:
            analysis = ai_response.json()
            
            # Show agents side-by-side or stacked in styled containers
            # We will use 5 columns for the 5 agents
            agent_cols = st.columns(5)
            
            # Agent 1: Product Agent
            with agent_cols[0]:
                st.markdown(
                    """
                    <div class="agent-container">
                        <div class="agent-header-green">📦 Product Agent</div>
                        <div class="agent-body">
                            <strong style="color:#10B981;">Key Features:</strong>
                    """,
                    unsafe_allow_html=True
                )
                for pro in analysis["product_agent"]["pros"][:3]:
                    st.write(f"✅ {pro}")
                st.markdown('<hr style="margin:0.5rem 0; border-color:#2D254F;"/>', unsafe_allow_html=True)
                st.write("<strong style='color:#EF4444;'>Key Tradeoffs:</strong>", unsafe_allow_html=True)
                for con in analysis["product_agent"]["cons"][:2]:
                    st.write(f"⚠️ {con}")
                st.markdown("</div></div>", unsafe_allow_html=True)
                
            # Agent 2: Review Agent
            with agent_cols[1]:
                st.markdown(
                    f"""
                    <div class="agent-container">
                        <div class="agent-header-blue">💬 Review Agent</div>
                        <div class="agent-body">
                            <div style="font-size:0.9rem; margin-bottom:0.5rem;">
                                <strong>Positive Sentiment:</strong> <span style="color:#3B82F6;">{analysis['review_agent']['positive_pct']:.0f}%</span>
                            </div>
                            <div style="font-size:0.9rem; margin-bottom:0.75rem;">
                                <strong>Negative Sentiment:</strong> <span style="color:#EF4444;">{analysis['review_agent']['negative_pct']:.0f}%</span>
                            </div>
                            <p style="font-size:0.85rem; color:#94A3B8; font-style:italic;">
                                "{analysis['review_agent']['summary']}"
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            # Agent 3: Price Agent
            with agent_cols[2]:
                trend_color = "#10B981" if analysis["price_agent"]["trend"] == "falling" else "#EF4444" if analysis["price_agent"]["trend"] == "rising" else "#F59E0B"
                worth_str = "YES" if analysis["price_agent"]["worth_buying"] else "NO"
                st.markdown(
                    f"""
                    <div class="agent-container">
                        <div class="agent-header-purple">📉 Price Agent</div>
                        <div class="agent-body">
                            <div style="font-size:0.9rem; margin-bottom:0.5rem;">
                                <strong>Current:</strong> ₹{analysis['price_agent']['current_price']:.2f}
                            </div>
                            <div style="font-size:0.9rem; margin-bottom:0.5rem;">
                                <strong>Historic Low:</strong> ₹{analysis['price_agent']['lowest_price']:.2f}
                            </div>
                            <div style="font-size:0.9rem; margin-bottom:0.5rem;">
                                <strong>Trend:</strong> <span style="color:{trend_color}; text-transform:uppercase;">{analysis['price_agent']['trend']}</span>
                            </div>
                            <div style="font-size:0.9rem; margin-bottom:0.75rem;">
                                <strong>Worth Buying?</strong> <strong>{worth_str}</strong>
                            </div>
                            <p style="font-size:0.8rem; color:#94A3B8;">{analysis['price_agent']['note']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            # Agent 4: Recommendation Agent
            with agent_cols[3]:
                st.markdown(
                    f"""
                    <div class="agent-container">
                        <div class="agent-header-orange">💡 Rec Agent</div>
                        <div class="agent-body">
                            <p style="font-size:0.85rem; color:#F97316; font-weight:600; margin-bottom:0.5rem;">
                                {analysis['recommendation_agent']['why_this_product']}
                            </p>
                            <strong>Best For:</strong>
                    """,
                    unsafe_allow_html=True
                )
                for who in analysis["recommendation_agent"]["who_should_buy"][:2]:
                    st.write(f"👤 {who}")
                st.markdown("</div></div>", unsafe_allow_html=True)
                
            # Agent 5: Decision Agent
            with agent_cols[4]:
                score_color = "#10B981" if analysis["decision_agent"]["final_score"] >= 85 else "#F59E0B" if analysis["decision_agent"]["final_score"] >= 70 else "#EF4444"
                st.markdown(
                    f"""
                    <div class="agent-container" style="border: 2px solid {score_color};">
                        <div class="agent-header-teal">🏆 Decision Agent</div>
                        <div class="agent-body" style="text-align:center;">
                            <div style="font-size:2.5rem; font-weight:800; color:{score_color}; margin-top:0.25rem;">
                                {analysis['decision_agent']['final_score']}
                            </div>
                            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:0.5rem;">CONFIDENCE: {analysis['decision_agent']['confidence_pct']}%</div>
                            <div style="font-weight:700; font-size:1rem; text-transform:uppercase; color:#E2E8F0; margin-bottom:0.5rem;">
                                VERDICT: {analysis['decision_agent']['verdict']}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if product["amazon_link"]:
                    st.link_button("🟢 BUY NOW ON AMAZON", product["amazon_link"], use_container_width=True)
        else:
            st.error("Could not run multi-agent AI analysis. Confirm Anthropic model availability.")

    # 2. Specifications Tab
    with tab2:
        st.subheader("📋 Product Technical Specifications")
        specs = product.get("specs", {})
        if not specs:
            st.info("No detailed specifications found for this product.")
        else:
            # Render specifications as a clean table
            import pandas as pd
            df_specs = pd.DataFrame(list(specs.items()), columns=["Specification", "Value"])
            st.table(df_specs.set_index("Specification"))

    # 3. Customer Reviews Tab
    with tab3:
        st.subheader("💬 Sentiment Summary & Pros/Cons")
        reviews = product.get("reviews", [])
        if not reviews:
            st.info("No reviews currently available for this product.")
        else:
            r = reviews[0]
            col_rev1, col_rev2 = st.columns(2)
            
            with col_rev1:
                st.write("**Pros (From Customer Reviews)**")
                for pro in r["pros"]:
                    st.success(pro)
                    
            with col_rev2:
                st.write("**Cons (From Customer Reviews)**")
                for con in r["cons"]:
                    st.error(con)
                    
            st.markdown("---")
            # Sentiment breakdown
            st.write("📊 **Review Sentiment Ratio**")
            col_sent1, col_sent2 = st.columns(2)
            col_sent1.metric("Positive Reviews", f"{r['positive_percent']:.0f}%")
            col_sent2.metric("Negative Reviews", f"{r['negative_percent']:.0f}%")
            st.progress(r["positive_percent"] / 100.0)

    # 4. Price History Tab
    with tab4:
        st.subheader("📉 Price Tracking & Insights")
        col_pr1, col_pr2, col_pr3 = st.columns(3)
        with col_pr1:
            st.metric("Current Price", f"₹{product['price']:.2f}")
        with col_pr2:
            st.metric("Original List Price", f"₹{product['original_price']:.2f}")
        with col_pr3:
            st.metric("Discount Value", f"₹{product['original_price'] - product['price']:.2f} ({product['discount_percent']:.0f}% OFF)")
            
        st.markdown("---")
        st.write("💡 **Price Analyst Verdict**")
        st.info(f"This product is listed at ₹{product['price']:.2f}, representing a savings of {product['discount_percent']:.0f}% over the normal catalog price of ₹{product['original_price']:.2f}. We track historical ranges to verify if this is a genuine discount.")

    # 5. Similar Products Tab
    with tab5:
        st.subheader("🔄 Similar Products in Category")
        with st.spinner("Finding similar products..."):
            sim_response = APIClient.get(f"/api/products/{product_id}/similar")
            
        if sim_response and sim_response.status_code == 200:
            similar_list = sim_response.json()
            if not similar_list:
                st.info("No similar products found.")
            else:
                sim_cols = st.columns(len(similar_list))
                for idx, sim in enumerate(similar_list):
                    with sim_cols[idx]:
                        st.markdown(f'<div style="display: flex; justify-content: center;"><img src="{get_clear_image_url(sim["image_url"])}" style="width: 180px; height: 180px; object-fit: cover; border-radius: 8px; border: 1px solid #E2E1F3; margin-bottom: 0.5rem;"/></div>', unsafe_allow_html=True)
                        st.write(f"**{sim['brand']}** {sim['name']}")
                        st.write(f"Price: **₹{sim['price']:.2f}**")
                        st.write(f"Rating: ⭐ {sim['rating']:.1f}")
                        st.button("View Product", key=f"sim_view_{sim['id']}", on_click=select_similar_product, args=(sim['id'],), use_container_width=True)
        else:
            st.error("Failed to load similar products.")
else:
    st.error("Product details could not be loaded.")
