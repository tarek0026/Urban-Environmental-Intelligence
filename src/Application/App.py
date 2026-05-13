import streamlit as st
import pandas as pd
import joblib

# ============================================================================
# PAGE CONFIGURATION & STYLING
# ============================================================================
st.set_page_config(
    page_title="Air Quality Dashboard | PM2.5 Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean and professional design
custom_css = """
<style>
    /* Color palette */
    :root {
        --dark-green: #1B4332;
        --teal: #2A9D8F;
        --light-bg: #F8F9FA;
        --card-gray: #E8EAED;
        --text-dark: #2C3E50;
    }
    
    /* Overall page */
    .main {
        background: #F8F9FA;
    }
    
    /* Main title */
    .main-title {
        color: #1B4332;
        font-size: 2.2em;
        font-weight: 700;
        text-align: center;
        margin: 0.5rem 0 0.3rem 0;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #2A9D8F;
        font-size: 0.95em;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Section headers */
    .section-header {
        color: #1B4332;
        font-size: 1.1em;
        font-weight: 600;
        margin: 1rem 0 0.7rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #2A9D8F;
    }
    
    /* Result metric card */
    .result-metric {
        background: white;
        border: 1px solid #E8EAED;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .result-value {
        font-size: 2.2em;
        font-weight: 700;
        color: #1B4332;
        margin: 0.5rem 0;
    }
    
    .result-label {
        font-size: 0.9em;
        color: #666;
        margin: 0;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.95em;
        margin-top: 0.5rem;
    }
    
    .status-good {
        background: #D4EDDA;
        color: #155724;
        border: 1px solid #C3E6CB;
    }
    
    .status-moderate {
        background: #FFF3CD;
        color: #856404;
        border: 1px solid #FFEEBA;
    }
    
    .status-sensitive {
        background: #FFE5CC;
        color: #B84600;
        border: 1px solid #FFD9B3;
    }
    
    .status-unhealthy {
        background: #F8D7DA;
        color: #721C24;
        border: 1px solid #F5C6CB;
    }
    
    .status-hazardous {
        background: #E8CCCC;
        color: #6B1C1C;
        border: 1px solid #D99999;
    }
    
    /* Recommendation box */
    .rec-box {
        background: white;
        border-left: 4px solid #2A9D8F;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.8rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    .rec-title {
        font-weight: 600;
        color: #1B4332;
        margin-bottom: 0.4rem;
        font-size: 0.95em;
    }
    
    .rec-content {
        color: #2C3E50;
        font-size: 0.9em;
        line-height: 1.5;
    }
    
    /* Sidebar */
    .sidebar-box {
        background: white;
        border-left: 4px solid #2A9D8F;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        font-size: 0.9em;
    }
    
    .sidebar-title {
        font-size: 0.95em;
        font-weight: 600;
        color: #1B4332;
        margin-bottom: 0.6rem;
    }
    
    /* Input labels */
    label {
        color: #1B4332 !important;
        font-weight: 500;
        font-size: 0.9em !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1B4332 0%, #2A9D8F 100%);
        color: white;
        border: none;
        padding: 0.8rem;
        font-size: 1em;
        font-weight: 600;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(27, 67, 50, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0F2818 0%, #1E7F6F 100%);
        box-shadow: 0 3px 8px rgba(27, 67, 50, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.85em;
        padding: 1.5rem 1rem;
        margin-top: 2rem;
        border-top: 1px solid #E8EAED;
        background: #F8F9FA;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("---")
    
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown("**PM2.5 Prediction System** - AI-powered air quality forecasting using Random Forest Regression with 10 environmental indicators.", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📊 Model Info</div>', unsafe_allow_html=True)
    st.markdown("**Algorithm:** Random Forest\n**Features:** 10 indicators\n**Output:** PM2.5 (µg/m³)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📈 PM2.5 Scale</div>', unsafe_allow_html=True)
    st.markdown("""
    🟢 **Good:** 0–12 µg/m³
    🟡 **Moderate:** 12–35
    🟠 **Sensitive:** 35–55
    🔴 **Unhealthy:** 55–150
    ☠️ **Hazardous:** 150+
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="main-title">🌍 Air Quality Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict PM2.5 pollution levels using Machine Learning</div>', unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("../../Models/pm25_model_pollution.pkl")

model = load_model()

# ============================================================================
# INPUT FORM
# ============================================================================

col1, col2 = st.columns(2)

# Location Information
with col1:
    st.markdown('<div class="section-header">📍 Location</div>', unsafe_allow_html=True)
    City = st.selectbox(
        "Select City",
        ["Cairo", "Dubai", "London", "New York", "Tokyo", "Paris", "Nairobi"],
        key="city_select",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-header">🌤️ Season</div>', unsafe_allow_html=True)
    Season = st.selectbox(
        "Select Season",
        ["Winter", "Spring", "Summer", "Autumn"],
        key="season_select",
        label_visibility="collapsed"
    )

# Pollution Indicators
st.markdown('<div class="section-header">💨 Pollution Indicators</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    PM10 = st.number_input("PM10", value=50.0, min_value=0.0, max_value=500.0, step=1.0)
with col2:
    NO2 = st.number_input("NO2", value=20.0, min_value=0.0, max_value=300.0, step=0.5)
with col3:
    CO = st.number_input("CO", value=1.0, min_value=0.0, max_value=50.0, step=0.1)
with col4:
    SO2 = st.number_input("SO2", value=10.0, min_value=0.0, max_value=300.0, step=0.5)

# Weather Conditions
st.markdown('<div class="section-header">🌡️ Weather Conditions</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    Temperature_mean = st.number_input("Temperature (°C)", value=25.0, min_value=-50.0, max_value=60.0, step=0.5)
with col2:
    Humidity = st.number_input("Humidity (%)", value=60.0, min_value=0.0, max_value=100.0, step=1.0)
with col3:
    Wind_speed = st.number_input("Wind Speed (km/h)", value=5.0, min_value=0.0, max_value=100.0, step=0.5)
with col4:
    st.empty()

# Environmental Factors
st.markdown('<div class="section-header">🌳 Environmental Factors</div>', unsafe_allow_html=True)
Green_Space = st.number_input("Green Space Coverage (%)", value=40.0, min_value=0.0, max_value=100.0, step=1.0)

# ============================================================================
# PREDICTION BUTTON
# ============================================================================
st.markdown("---")
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    predict_button = st.button("🔮 PREDICT PM2.5", key="predict_btn", use_container_width=True)

# ============================================================================
# PREDICTION RESULTS
# ============================================================================
if predict_button:
    # Prepare input data - EXACTLY matching model features
    input_data = pd.DataFrame({
        'PM10': [PM10],
        'NO2': [NO2],
        'CO': [CO],
        'SO2': [SO2],
        'Green_Space': [Green_Space],
        'Temperature_mean': [Temperature_mean],
        'Humidity': [Humidity],
        'Wind_speed': [Wind_speed],
        'City': [City],
        'Season': [Season]
    })
    
    # Get prediction
    prediction = model.predict(input_data)[0]
    
    st.markdown("---")
    st.markdown('<div class="section-header">📈 Results</div>', unsafe_allow_html=True)
    
    # Determine air quality category
    if prediction <= 12:
        category = "Good"
        emoji = "🟢"
        status_class = "status-good"
        health_rec = "Air quality is satisfactory. Outdoor activities are safe for everyone."
        activity = "✅ Safe for outdoor exercise"
    elif prediction <= 35:
        category = "Moderate"
        emoji = "🟡"
        status_class = "status-moderate"
        health_rec = "Air quality is acceptable. Sensitive groups may limit prolonged outdoor exposure."
        activity = "⚠️ Sensitive individuals should limit outdoor activities"
    elif prediction <= 55:
        category = "Unhealthy for Sensitive Groups"
        emoji = "🟠"
        status_class = "status-sensitive"
        health_rec = "Sensitive groups should reduce outdoor activities."
        activity = "🚫 Sensitive groups should avoid strenuous outdoor activities"
    elif prediction <= 150:
        category = "Unhealthy"
        emoji = "🔴"
        status_class = "status-unhealthy"
        health_rec = "Everyone should limit outdoor activities. Use N95 masks if going outside."
        activity = "🏠 Minimize outdoor activities; use air purifiers"
    else:
        category = "Hazardous"
        emoji = "☠️"
        status_class = "status-hazardous"
        health_rec = "Avoid all outdoor activities. Stay indoors with filtered air."
        activity = "🏠 Stay indoors; use air purifiers and filters"
    
    # Results layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="result-metric">', unsafe_allow_html=True)
        st.markdown('<div class="result-label">PM2.5 Level</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-value">{prediction:.1f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-label">µg/m³</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="result-label">Status</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-badge {status_class}">{emoji} {category}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="result-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="result-label">City</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-value" style="font-size: 1.5em;">{City}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations
    st.markdown('<div class="rec-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-title">💡 Health Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-content">{health_rec}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="rec-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-title">🏃 Activity Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-content">{activity}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Environmental insights
    st.markdown('<div class="rec-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="rec-title">🌍 Environmental Insights</div>', unsafe_allow_html=True)
    
    insights = []
    if Green_Space >= 50:
        insights.append("✓ Excellent green space coverage supports better air quality")
    elif Green_Space >= 30:
        insights.append("✓ Good green space presence helps mitigate pollution")
    else:
        insights.append("⚠ Limited green space; more vegetation needed")
    
    if Wind_speed >= 8:
        insights.append("✓ Strong winds effectively disperse pollutants")
    elif Wind_speed >= 3:
        insights.append("✓ Moderate winds support natural pollutant dispersion")
    else:
        insights.append("⚠ Low wind speed may allow pollutant accumulation")
    
    st.markdown(f'<div class="rec-content">{"<br>".join(insights)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input summary
    with st.expander("📋 View Input Parameters"):
        summary_data = pd.DataFrame({
            'Parameter': ['PM10', 'NO2', 'CO', 'SO2', 'Green Space', 'Temperature', 'Humidity', 'Wind Speed', 'City', 'Season'],
            'Value': [f"{PM10:.1f}", f"{NO2:.1f}", f"{CO:.1f}", f"{SO2:.1f}", f"{Green_Space:.1f}%", f"{Temperature_mean:.1f}°C", f"{Humidity:.1f}%", f"{Wind_speed:.1f}", City, Season]
        })
        st.dataframe(summary_data, use_container_width=True, hide_index=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    <strong>🌿 Air Quality Prediction Dashboard</strong><br>
    Developed with Machine Learning & Streamlit | Random Forest Regression Model
</div>
""", unsafe_allow_html=True)