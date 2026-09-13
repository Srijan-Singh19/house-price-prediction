import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(
    "house_price_model.pkl/house_price_model.pkl"
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="HouseWise | Bengaluru Property Analyzer",
    page_icon="🏠",
    layout="centered"
)

# --------------------------------------------------
# STYLES
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 720px;
}

/* Header */
.hw-header {
    text-align: center;
    margin-bottom: 0.25rem;
}

.hw-eyebrow {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
    color: #8a8f98;
    margin-bottom: 6px;
}

.hw-title {
    font-size: 34px;
    font-weight: 800;
    color: #1a1a2e;
    margin: 0;
    letter-spacing: -0.5px;
}

.hw-subtitle {
    font-size: 15px;
    color: #6b7280;
    margin-top: 6px;
    margin-bottom: 2rem;
}

/* Section card */
.hw-card {
    background-color: #ffffff;
    border: 1px solid #eef0f2;
    border-radius: 14px;
    padding: 24px 24px 8px 24px;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.hw-section-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9199a3;
    margin-bottom: 4px;
}

.hw-section-desc {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 1rem;
}

/* Result card */
.hw-result {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #1a1a2e;
    border-radius: 14px;
    padding: 28px 24px;
    text-align: center;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}

.hw-result-label {
    color: #9199a3;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.hw-result-price {
    color: #1a1a2e;
    font-size: 40px;
    font-weight: 800;
    line-height: 1.1;
}

.hw-result-sub {
    color: #6b7280;
    font-size: 14px;
    margin-top: 10px;
}

.hw-result-sub b {
    color: #1a1a2e;
}

/* Metrics row */
.hw-metric-label {
    font-size: 12px;
    color: #9199a3;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 700;
    margin-bottom: 2px;
}

/* Footer */
.hw-footer {
    text-align: center;
    font-size: 12px;
    color: #a1a5ad;
    margin-top: 1rem;
}

/* Button */
div.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 0.6rem 0;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hw-header">
    <div class="hw-eyebrow">Property Valuation Tool</div>
    <div class="hw-title">🏠 HouseWise</div>
    <div class="hw-subtitle">Estimate Bengaluru property prices in seconds</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PROPERTY INPUT
# --------------------------------------------------

locations = [
    "Whitefield",
    "Hebbal",
    "Sarjapur Road",
    "Marathahalli",
    "Electronic City",
    "Indira Nagar",
    "Rajaji Nagar",
    "Malleswaram",
    "Koramangala"
]

st.markdown('<div class="hw-card">', unsafe_allow_html=True)
st.markdown('<div class="hw-section-label">Property Details</div>', unsafe_allow_html=True)
st.markdown('<div class="hw-section-desc">Fill in the specifics below to get an instant price estimate.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    location = st.selectbox("Location", locations)
    total_sqft = st.number_input(
        "Total Area (sq.ft)",
        min_value=300.0,
        max_value=50000.0,
        value=1500.0,
        step=50.0
    )

with col2:
    bhk = st.number_input(
        "BHK",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )
    bath = st.number_input(
        "Bathrooms",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

st.write("")
predict = st.button("Predict Price", type="primary", width="stretch")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if predict:

    # Feature engineering
    sqft_per_bhk = total_sqft / bhk

    # Prepare input
    input_data = pd.DataFrame([{
        "location": location,
        "total_sqft": total_sqft,
        "bath": bath,
        "bhk": bhk,
        "sqft_per_bhk": sqft_per_bhk
    }])

    # Model prediction
    prediction = model.predict(input_data)[0]

    # Price per square foot
    estimated_price_per_sqft = (
        prediction * 100000
    ) / total_sqft

    # Result card
    st.markdown(f"""
    <div class="hw-result">
        <div class="hw-result-label">Estimated Property Price</div>
        <div class="hw-result-price">₹ {prediction:.2f} Lakhs</div>
        <div class="hw-result-sub">Price per sq.ft: <b>₹ {estimated_price_per_sqft:,.0f}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # Model info
    st.markdown('<div class="hw-card">', unsafe_allow_html=True)
    st.markdown('<div class="hw-section-label">Model Performance</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="hw-metric-label">R² Score</div>', unsafe_allow_html=True)
        st.markdown("**0.577**")
    with m2:
        st.markdown('<div class="hw-metric-label">MAE</div>', unsafe_allow_html=True)
        st.markdown("**₹32.07 L**")
    with m3:
        st.markdown('<div class="hw-metric-label">Model</div>', unsafe_allow_html=True)
        st.markdown("**Random Forest**")

    st.caption("Prediction generated using a trained Random Forest regression model.")
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="hw-footer">HouseWise · Bengaluru House Price Prediction · Data Science Project</div>',
    unsafe_allow_html=True
)