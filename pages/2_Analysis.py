import streamlit as st
import pandas as pd
import numpy as np
import pickle

import plotly.express as px
import plotly.graph_objects as go

from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.title("📊 Gurgaon Property Market Analysis")

df_flat = pd.read_csv("datasets/df_flat_viz.csv")
df_land = pd.read_csv("datasets/df_land_viz.csv")

with open("datasets/feature_text_flat.pkl","rb") as f:
    feature_text_flat = pickle.load(f)

with open("datasets/feature_text_land.pkl","rb") as f:
    feature_text_land = pickle.load(f)

analysis_type = st.selectbox(
    "Select Property Type",
    ["Flat/House","Land"]
)

if analysis_type == "Flat/House":

    property_filter = st.selectbox(
        "Property Category",
        ["All","Flat","House"]
    )

    if property_filter == "Flat":
        data = df_flat[df_flat["property_type"]=="flat"]

    elif property_filter == "House":
        data = df_flat[df_flat["property_type"]=="house"]

    else:
        data = df_flat.copy()

    st.subheader("📈 Market Insights")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "Avg Price",
            f"₹ {data['price'].mean():.2f} Cr"
        )

    with col2:
        st.metric(
            "Median Price",
            f"₹ {data['price'].median():.2f} Cr"
        )

    with col3:
        st.metric(
            "Avg Area",
            f"{data['built_up_area'].mean():.0f} sq ft"
        )

    with col4:
        sector = (
            data.groupby('sector')['price']
            .mean()
            .idxmax()
        )

        st.metric(
            "Top Sector",
            sector
        )
    st.subheader("🏆 Top Expensive & Cheapest Sectors")

    sector_price = (
        data.groupby("sector")["price"]
        .mean()
        .sort_values()
    )

    col1,col2 = st.columns(2)

    with col1:

        top10 = sector_price.tail(10)

        fig = px.bar(
            x=top10.values,
            y=top10.index,
            orientation="h",
            title="Most Expensive Sectors"
        )

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        cheap10 = sector_price.head(10)

        fig = px.bar(
            x=cheap10.values,
            y=cheap10.index,
            orientation="h",
            title="Most Affordable Sectors"
        )

        st.plotly_chart(fig,use_container_width=True)


    st.subheader("🏠 Flat vs House Comparison")

    compare_df = (
        df_flat
        .groupby("property_type")
        [["price","built_up_area","price_per_sqft"]]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        compare_df,
        x="property_type",
        y="price",
        color="property_type",
        title="Average Property Price"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("📉 Area vs Price")

    fig = px.scatter(
        data,
        x="built_up_area",
        y="price",
        color="property_type",
        hover_data=["sector"]
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("🗺️ Property Heat Map")

    map_df = (
        data.groupby("sector")
        .agg({
            "latitude":"mean",
            "longitude":"mean",
            "price_per_sqft":"mean",
            "built_up_area":"mean"
        })
        .reset_index()
    )

    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqft",
        size="built_up_area",
        hover_name="sector",
        zoom=10,
        mapbox_style="open-street-map"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("☁️ Popular Amenities")

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate(feature_text_flat)

    fig,ax = plt.subplots(figsize=(12,6))

    ax.imshow(wc)
    ax.axis("off")

    st.pyplot(fig)
else:

    data = df_land.copy()
    st.subheader("📈 Market Insights")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "Avg Price",
            f"₹ {data['price'].mean():.2f} Cr"
        )

    with col2:
        st.metric(
            "Median Price",
            f"₹ {data['price'].median():.2f} Cr"
        )

    with col3:
        st.metric(
            "Avg Plot Area",
            f"{data['area'].mean():.0f} sq m"
        )

    with col4:

        sector = (
            data.groupby('sector')['price']
            .mean()
            .idxmax()
        )

        st.metric(
            "Top Sector",
            sector
        )
    st.subheader("🏆 Top Expensive & Cheapest Sectors")

    sector_price = (
        data.groupby("sector")["price"]
        .mean()
        .sort_values()
    )

    col1, col2 = st.columns(2)

    with col1:

        top10 = sector_price.tail(10)

        fig = px.bar(
            x=top10.values,
            y=top10.index,
            orientation="h",
            title="Most Expensive Sectors"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        cheap10 = sector_price.head(10)

        fig = px.bar(
            x=cheap10.values,
            y=cheap10.index,
            orientation="h",
            title="Most Affordable Sectors"
        )

        st.plotly_chart(fig, use_container_width=True)
    st.subheader("📉 Area vs Price")

    fig = px.scatter(
        data,
        x="area",
        y="price",
        hover_data=["sector"]
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("🗺️ Land Market Map")

    map_df = (
        data.groupby("sector")
        .agg({
            "latitude":"mean",
            "longitude":"mean",
            "price_per_sqm":"mean",
            "area":"mean"
        })
        .reset_index()
    )

    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqm",
        size="area",
        hover_name="sector",
        zoom=10,
        mapbox_style="open-street-map"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("☁️ Popular Land Features")

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate(feature_text_land)

    fig,ax = plt.subplots(figsize=(12,6))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)
