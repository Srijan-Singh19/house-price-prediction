import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("house_price_model.pkl")

# Page settings
st.set_page_config(
    page_title="HouseWise",
    page_icon="🏠",
    layout="centered"
)

# Title
st.title("🏠 HOUSEWISE")
st.subheader("Bengaluru Property Analyzer")

st.write("Enter the property details to estimate its market price.")

# Location
location = st.selectbox(
    "Location",
    [
        "Whitefield",
        "Hebbal",
        "Sarjapur Road",
        "Marathahalli",
        "Electronic City",
        "Indira Nagar",
        "Rajaji Nagar",
        "Malleswaram",
        "Koramangala",
        "Other"
    ]
)

# Property details
total_sqft = st.number_input(
    "Total Area (sq.ft)",
    min_value=300.0,
    max_value=50000.0,
    value=1500.0,
    step=50.0
)

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

# Prediction
if st.button("🔮 PREDICT PRICE", type="primary", width="stretch"):

    # Feature engineering
    sqft_per_bhk = total_sqft / bhk

    # Create input
    input_data = pd.DataFrame([{
        "location": location,
        "total_sqft": total_sqft,
        "bath": bath,
        "bhk": bhk,
        "sqft_per_bhk": sqft_per_bhk
    }])

    # Predict
    prediction = model.predict(input_data)[0]

    # Result
    st.success("Prediction generated successfully!")

    st.markdown("### 💰 Estimated Price")

    st.metric(
        label="HouseWise Estimate",
        value=f"₹ {prediction:.2f} Lakhs"
    )

    st.caption(
        "This estimate is generated using the trained Random Forest model."
    )