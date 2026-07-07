import streamlit as st
from utils.auth_helper import AuthHelper
from styles import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartBuy AI - Your Intelligent Shopping Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject dark theme CSS
inject_custom_css()

# Session state initialization
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None
if "query_results" not in st.session_state:
    st.session_state["query_results"] = None
if "selected_product_id" not in st.session_state:
    st.session_state["selected_product_id"] = None
if "compare_list" not in st.session_state:
    st.session_state["compare_list"] = []

# Main UI layout
st.title("🛍️ SmartBuy AI")
st.subheader("Your AI-Powered Product Recommendation & Analysis Assistant")

# Sidebar navigation / Status info
with st.sidebar:
    st.title("SmartBuy AI")
    if AuthHelper.is_logged_in():
        st.write(f"Logged in as: **{st.session_state['user']['name']}**")
        st.write(f"Email: {st.session_state['user']['email']}")
        if st.button("Log Out"):
            AuthHelper.logout()
    else:
        st.info("Please log in or register to begin your personalized shopping journey.")

# Redirect if already logged in
if AuthHelper.is_logged_in():
    st.success(f"Welcome back, {st.session_state['user']['name']}!")
    col1, col2 = st.columns(2)
    with col1:
        st.info("You are currently logged in. Click the button below to open your Dashboard.")
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
else:
    # Login & Registration Tabs
    tab1, tab2 = st.tabs(["🔐 Log In", "📝 Register New Account"])
    
    with tab1:
        col_login_left, col_login_mid, col_login_right = st.columns([1, 2, 1])
        with col_login_mid:
            st.markdown('<h3 class="section-title">Log In to Your Account</h3>', unsafe_allow_html=True)
            login_email = st.text_input("Email Address", key="login_email_input")
            login_password = st.text_input("Password", type="password", key="login_password_input")
            
            if st.button("Log In", key="login_btn", use_container_width=True):
                if not login_email or not login_password:
                    st.warning("Please fill in all fields.")
                else:
                    with st.spinner("Logging in..."):
                        if AuthHelper.login(login_email, login_password):
                            st.switch_page("pages/1_Dashboard.py")
                        
    with tab2:
        col_reg_left, col_reg_mid, col_reg_right = st.columns([1, 2, 1])
        with col_reg_mid:
            st.markdown('<h3 class="section-title">Create a SmartBuy AI Account</h3>', unsafe_allow_html=True)
            reg_name = st.text_input("Full Name", key="reg_name_input")
            reg_email = st.text_input("Email Address", key="reg_email_input")
            reg_password = st.text_input("Password", type="password", key="reg_password_input")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_input")
            
            if st.button("Create Account", key="reg_btn", use_container_width=True):
                if not reg_name or not reg_email or not reg_password:
                    st.warning("Please fill in all fields.")
                elif reg_password != reg_confirm_password:
                    st.error("Passwords do not match.")
                else:
                    with st.spinner("Registering your account..."):
                        if AuthHelper.register(reg_name, reg_email, reg_password):
                            st.info("Please switch to the '🔐 Log In' tab above to log in to your new account.")

# Dynamic Visual showcase
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🤖 Multi-Agent AI Analysis")
    st.write("We deploy specialized AI agents (Product, Review, Price, Recommendation, Decision) to perform complete research on products and summarize customer reviews for you.")
with col2:
    st.markdown("### 📉 Smart Price Tracking")
    st.write("Keep track of current vs. historic low prices, price trends, and whether products represent genuine discounts before you click buy.")
with col3:
    st.markdown("### 🏆 Podium Winners")
    st.write("Compare the top matches on a custom winners podium screen, highlighting the best choice based on specifications, budget, and overall quality ratings.")
