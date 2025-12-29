import streamlit as st
import pandas as pd
import joblib

model = joblib.load("house_price_model.pkl")
neighborhoods = joblib.load("neighborhoods.pkl")

MAE = 3300000

def format_price_pkr(price):
    if price >= 1e7:
        return f"{price/1e7:.2f} Crore PKR"
    else:
        return f"{price/1e5:.2f} Lakh PKR"

st.title("Karachi House Price Predictor")

size = st.number_input("Size (Square Yards)", 50, 700, 125)
neighborhood = st.selectbox("Neighborhood", neighborhoods)
bedrooms = st.number_input("Bedrooms", 1, 10, 3)

if st.button("Predict Price"):
    input_df = pd.DataFrame({
        "Size": [size],
        "Neighborhood": [neighborhood],
        "Bedrooms": [bedrooms]
    })

    prediction = model.predict(input_df)[0]
    prediction = max(prediction, 0)

    st.success(f"Estimated Market Value: {format_price_pkr(prediction)}")

    lower = max(prediction - MAE, 0)
    upper = prediction + MAE

    st.info(
        f"Expected Range: {format_price_pkr(lower)} to {format_price_pkr(upper)}"
    )
