import streamlit as st
import pandas as pd
import numpy as np
import pickle

# =========================
# LOAD FILES
# =========================

house_model = pickle.load(open('datasets/pipeline.pkl', 'rb'))
house_df = pickle.load(open('datasets/df_flat_house.pkl', 'rb'))

land_model = pickle.load(open('datasets/land_price_model.pkl', 'rb'))
land_df = pickle.load(open('datasets/df.pkl', 'rb'))

# =========================
# PAGE
# =========================

st.set_page_config(page_title="Property Price Predictor")

st.title("🏠 Gurgaon Property Price Predictor")

property_type = st.selectbox(
    "Select Property Type",
    ["House / Flat", "Residential Land"]
)

# ==================================================
# HOUSE / FLAT
# ==================================================

if property_type == "House / Flat":

    st.header("House / Flat Price Prediction")

    property_subtype = st.selectbox(
        "Property Type",
        sorted(house_df['property_type'].dropna().unique())
    )
    sector = st.selectbox(
        "Sector",
        sorted(house_df['sector'].dropna().unique())
    )

    bedroom = st.number_input("Bedrooms", 1, 10, 3)

    bathroom = st.number_input("Bathrooms", 1, 10, 3)

    balcony = st.selectbox(
        "Balcony",
        sorted(house_df['balcony'].dropna().unique())
    )
    servant_room = st.selectbox(
        "Servant Room",
        [0, 1]
    )

    store_room = st.selectbox(
        "Store Room",
        [0, 1]
    )
    built_up_area = st.number_input(
        "Built Up Area (sq ft)",
        min_value=200,
        value=1500
    )

    furnishing_type = st.selectbox(
        "Furnishing",
        sorted(house_df['furnishing_type'].dropna().unique())
    )

    luxury_category = st.selectbox(
        "Luxury Category",
        sorted(house_df['luxury_category'].dropna().unique())
    )

    floor_category = st.selectbox(
        "Floor Category",
        sorted(house_df['floor_category'].dropna().unique())
    )

    agePossession = st.selectbox(
        "Age Possession",
        sorted(house_df['agePossession'].dropna().unique())
    )



    if st.button("Predict House Price"):

        input_df = pd.DataFrame({
            'property_type':[property_subtype],
            'sector':[sector],
            'bedRoom':[bedroom],
            'bathroom':[bathroom],
            'balcony':[balcony],
            'built_up_area':[built_up_area],
            'agePossession':[agePossession],
            'furnishing_type':[furnishing_type],
            'luxury_category':[luxury_category],
            'floor_category':[floor_category],
            'servant room': [servant_room],
            'store room': [store_room]
        })

        pred_log = house_model.predict(input_df)

        pred_price = np.expm1(pred_log)[0]

        mae = 0.46

        lower = max(0, pred_price - mae/2)
        upper = pred_price + mae/2

        st.success(f"Predicted Price : ₹ {pred_price:.2f} Cr")

        st.info(
            f"Expected Range : ₹ {lower:.2f} Cr - ₹ {upper:.2f} Cr"
        )


# ==================================================
# LAND
# ==================================================

else:

    st.header("Residential Land Price Prediction")

    sector = st.selectbox(
        "Sector",
        sorted(land_df['sector'].dropna().unique())
    )

    area_sqft = st.number_input(
        "Plot Area (sq ft)",
        min_value=100,
        value=1000
    )

    feature = st.selectbox(
        "Feature Category",
        sorted(land_df['feature'].dropna().unique())
    )

    if st.button("Predict Land Price"):

        # sqft -> sqm
        area_sqm = area_sqft / 10.764

        input_df = pd.DataFrame({
            'sector':[sector],
            'area':[np.log1p(area_sqm)],
            'feature':[feature]
        })

        pred_log = land_model.predict(input_df)

        pred_price = np.expm1(pred_log)[0]

        mae = 0.76

        lower = max(0, pred_price - mae/2)
        upper = pred_price + mae/2

        st.success(f"Predicted Price : ₹ {pred_price:.2f} Cr")

        st.info(
            f"Expected Range : ₹ {lower:.2f} Cr - ₹ {upper:.2f} Cr"
        )