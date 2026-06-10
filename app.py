
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Bike Business Record - Sheet1 (1).csv")

df["total_profit"] = pd.to_numeric(df["total_profit"], errors="coerce")

st.title("Bike Business Dashboard")

st.metric("Total Profit", f"₹{df['total_profit'].sum():,.0f}")

brand_profit = (
    df.groupby("bike_brand")["total_profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    brand_profit,
    x="bike_brand",
    y="total_profit",
    title="Profit by Brand"
)

st.plotly_chart(fig)

st.dataframe(df)
