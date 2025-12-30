import streamlit as st
import pandas as pd
import joblib
from difflib import get_close_matches

# Load model and data
model = joblib.load("Karachi_house_Prediction.pkl")
neighborhoods = joblib.load("neighborhoods.pkl")
MAE = 3300000

def format_price_pkr(price):
    """Format price in Pakistani Rupees"""
    if price >= 1e7:
        return f"{price/1e7:.2f} Crore PKR"
    else:
        return f"{price/1e5:.2f} Lakh PKR"

def find_matching_neighborhoods(search_term, neighborhood_list, max_matches=5):
    """Find neighborhoods that match the search term"""
    if not search_term:
        return neighborhood_list
    
    search_term = search_term.lower().strip()
    
    # Exact matches (case-insensitive)
    exact_matches = [n for n in neighborhood_list if search_term in n.lower()]
    
    # If we have exact matches, return them
    if exact_matches:
        return exact_matches
    
    # Otherwise, use fuzzy matching
    close_matches = get_close_matches(
        search_term, 
        neighborhood_list, 
        n=max_matches, 
        cutoff=0.4
    )
    
    return close_matches if close_matches else neighborhood_list

# Page configuration
st.set_page_config(
    page_title="Karachi House Price Predictor",
    layout="wide"
)

# Custom CSS for compact styling with background
st.markdown("""
    <style>
    /* Background image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=1920&h=1080&fit=crop&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Semi-transparent overlay for better readability */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.85);
        z-index: -1;
    }
    
    /* Reduce padding and margins */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
        background-color: rgba(255, 255, 255, 0.75);
        border-radius: 10px;
        padding: 2rem;
    }
    h1 {
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
        color: #1a1a1a !important;
    }
    h2 {
        font-size: 1.5rem !important;
        margin-top: 0.5rem !important;
        color: #2a2a2a !important;
    }
    h3 {
        font-size: 1.2rem !important;
        color: #3a3a3a !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #2196F3;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
        font-weight: bold;
    }
    
    /* Animated results container */
    .result-container {
        animation: slideIn 0.5s ease-out;
        border-left: 4px solid #2196F3;
        padding-left: 1rem;
        margin-top: 1rem;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Metric animations */
    @keyframes countUp {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.9);
        }
        50% {
            transform: translateY(-5px) scale(1.05);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }
    
    /* Apply animation to metrics */
    [data-testid="stMetric"] {
        animation: countUp 0.6s ease-out;
    }
    
    [data-testid="stMetric"]:nth-child(1) {
        animation-delay: 0.1s;
    }
    
    [data-testid="stMetric"]:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    [data-testid="stMetric"]:nth-child(3) {
        animation-delay: 0.3s;
    }
    
    /* Metric value animation on hover */
    [data-testid="stMetricValue"] {
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover [data-testid="stMetricValue"] {
        animation: pulse 0.5s ease-in-out;
    }
    
    /* Watermark */
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: rgba(0, 0, 0, 0.3);
        font-size: 11px;
        font-weight: 600;
        z-index: 9999;
        pointer-events: none;
    }
    
    /* Make text more readable */
    .stMarkdown, .stText {
        font-size: 15px !important;
        color: #1a1a1a !important;
    }
    
    /* Compact metrics */
    [data-testid="stMetricValue"] {
        font-size: 20px !important;
        color: #1a1a1a !important;
    }
    
    /* FIXED: Input fields - force black text on PC and mobile */
    .stTextInput input, 
    .stNumberInput input, 
    .stSelectbox select {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Dropdown text color fix */
    .stSelectbox div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    
    /* LIGHT/DARK MODE: Labels always visible */
    [data-testid="stWidgetLabel"] {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        .watermark {
            color: rgba(255, 255, 255, 0.3);
        }
        
        .stTextInput input, 
        .stNumberInput input, 
        .stSelectbox select {
            background-color: rgba(50, 50, 50, 0.95) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        
        .stSelectbox div[data-baseweb="select"] span {
            color: #ffffff !important;
        }
        
        [data-testid="stWidgetLabel"] {
            color: #ffffff !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #ffffff !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Watermark HTML (moved outside CSS block)
st.markdown('<div class="watermark">© Muhammad Mujtaba</div>', unsafe_allow_html=True)

# Header
st.title("Karachi House Price Predictor")

# Main layout - two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Property Details")
    
    size = st.number_input(
        "Size (Square Yards)",
        min_value=50,
        max_value=700,
        value=125,
        step=25
    )
    
    search_term = st.text_input(
        "Search Neighborhood",
        placeholder="Type to search..."
    )
    
    filtered_neighborhoods = find_matching_neighborhoods(search_term, neighborhoods)
    
    if search_term and len(filtered_neighborhoods) < len(neighborhoods):
        st.caption(f"Found {len(filtered_neighborhoods)} match(es)")
    
    neighborhood = st.selectbox(
        "Select Neighborhood",
        options=filtered_neighborhoods
    )
    
    bedrooms = st.number_input(
        "Number of Bedrooms",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )
    
    predict_clicked = st.button("Predict Price")

with col2:
    st.subheader("Prediction Results")
    
    if predict_clicked:
        # Create animated container for results
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        input_df = pd.DataFrame({
            "Size": [size],
            "Neighborhood": [neighborhood],
            "Bedrooms": [bedrooms]
        })
        
        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)
        
        lower = max(prediction - MAE, 0)
        upper = prediction + MAE
        
        st.metric("Estimated Value", format_price_pkr(prediction))
        st.metric("Lower Range", format_price_pkr(lower))
        st.metric("Upper Range", format_price_pkr(upper))
        
        st.info(f"For a {size} sq yd property with {bedrooms} bedroom(s) in {neighborhood}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Enter property details and click 'Predict Price' to see results")
        st.caption(f"Model Accuracy (MAE): {format_price_pkr(MAE)}")