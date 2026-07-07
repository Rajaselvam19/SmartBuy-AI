import streamlit as st

def inject_custom_css():
    """Injects custom CSS to style the Streamlit app with a modern, premium light glassmorphism theme."""
    theme_css = """
    <style>
    /* Main app container background - gorgeous lilac to pale indigo pastel gradient */
    .stApp {
        background: linear-gradient(135deg, #F3F1FA 0%, #E7E3FC 100%) !important;
        color: #1E1B4B !important;
        font-family: 'Inter', 'Roboto', 'Segoe UI', sans-serif;
    }
    
    /* Ensure markdown text is styled correctly */
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #1E1B4B !important;
    }
    
    /* Sidebar styling - soft white glass panel with deep violet accents */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E4E3F3 !important;
        box-shadow: 4px 0 15px rgba(124, 58, 237, 0.05);
    }
    
    section[data-testid="stSidebar"] * {
        color: #312E81 !important;
    }
    
    /* Style subheaders or links in sidebar */
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #4F46E5 !important;
        font-weight: 700 !important;
    }
    
    /* Input inputs and textareas styling */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input, select {
        background-color: #FFFFFF !important;
        color: #1E1B4B !important;
        border: 1px solid #DCD7F7 !important;
        border-radius: 8px !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Buttons styling - fashionable deep violet gradient */
    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #6D28D9 0%, #4C1D95 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(124, 58, 237, 0.3) !important;
    }
    
    /* Secondary/Sidebar Buttons style */
    section[data-testid="stSidebar"] .stButton>button {
        background: #F5F3FF !important;
        color: #6D28D9 !important;
        border: 1px solid #DDD6FE !important;
        box-shadow: none !important;
    }
    
    section[data-testid="stSidebar"] .stButton>button:hover {
        background: #EDE9FE !important;
        color: #5B21B6 !important;
        transform: translateY(-1px);
    }
    
    /* Card Container - sleek glassmorphic white card with border shadows */
    .product-card {
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 16px !important;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.03), 0 4px 6px -2px rgba(124, 58, 237, 0.01);
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        border-color: #8B5CF6 !important;
        box-shadow: 0 20px 25px -5px rgba(124, 58, 237, 0.08), 0 10px 10px -5px rgba(124, 58, 237, 0.04);
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Badges */
    .match-badge {
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .match-high {
        background-color: rgba(16, 185, 129, 0.12) !important;
        color: #059669 !important;
        border: 1px solid #10B981 !important;
    }
    
    .match-mid {
        background-color: rgba(245, 158, 11, 0.12) !important;
        color: #D97706 !important;
        border: 1px solid #F59E0B !important;
    }
    
    .match-low {
        background-color: rgba(239, 68, 68, 0.12) !important;
        color: #DC2626 !important;
        border: 1px solid #EF4444 !important;
    }
    
    /* Category Button Container - clean white cards */
    .category-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E1F3 !important;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.2s ease;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    }
    
    .category-card:hover {
        border-color: #8B5CF6 !important;
        background: #F5F3FF !important;
        transform: scale(1.02);
        box-shadow: 0 10px 15px rgba(124, 58, 237, 0.06);
    }
    
    /* Custom Headers with modern underline */
    .section-title {
        color: #1E1B4B !important;
        font-weight: 700;
        border-bottom: 2.5px solid #8B5CF6 !important;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Winner Podium Container */
    .podium-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    .podium-card {
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        min-width: 180px;
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.05);
    }
    
    .podium-1 {
        background: linear-gradient(135deg, #FFFDF5 0%, #FEF3C7 100%) !important;
        border: 2px solid #F59E0B !important; /* Gold */
        height: 380px !important;
        order: 2;
    }
    
    .podium-2 {
        background: #FFFFFF !important;
        border: 1.5px solid #94A3B8 !important; /* Silver */
        height: 310px !important;
        order: 1;
    }
    
    .podium-3 {
        background: #FFFFFF !important;
        border: 1.5px solid #B45309 !important; /* Bronze */
        height: 260px !important;
        order: 3;
    }
    
    .podium-card div {
        color: #1E1B4B !important;
    }
    
    .podium-badge {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .podium-rank {
        font-weight: 800;
        font-size: 1.25rem;
        margin-bottom: 1rem;
    }
    
    /* Pricing typography styling */
    .price-tag {
        color: #10B981 !important;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .original-price-tag {
        color: #6B7280 !important;
        text-decoration: line-through;
        font-size: 1rem;
        margin-left: 0.5rem;
    }
    
    .discount-badge {
        background-color: #10B981 !important;
        color: white !important;
        font-size: 0.75rem;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        margin-left: 0.5rem;
        font-weight: 700;
    }
    
    /* Agent card headers */
    .agent-header-green {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    .agent-header-blue {
        background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    .agent-header-purple {
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    .agent-header-orange {
        background: linear-gradient(90deg, #F97316 0%, #EA580C 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    .agent-header-teal {
        background: linear-gradient(90deg, #14B8A6 0%, #0D9488 100%) !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    
    .agent-container {
        background: #FFFFFF !important;
        border: 1px solid #E2E1F3 !important;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .agent-body {
        padding: 1rem;
        color: #1E1B4B !important;
    }
    
    /* Ensure tabs text color matches theme */
    div[data-baseweb="tab-list"] button {
        color: #4F46E5 !important;
        font-weight: 600 !important;
    }
    
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #7C3AED !important;
        border-bottom-color: #7C3AED !important;
    }
    
    /* Expander elements styling */
    div[data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E1F3 !important;
        border-radius: 8px !important;
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

def render_match_badge(score: int):
    """Returns the HTML string for the colored match badge based on the AI match score."""
    if score >= 85:
        return f'<span class="match-badge match-high">AI Match: {score}%</span>'
    elif score >= 70:
        return f'<span class="match-badge match-mid">AI Match: {score}%</span>'
    else:
        return f'<span class="match-badge match-low">AI Match: {score}%</span>'
