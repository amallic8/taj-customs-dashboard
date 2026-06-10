
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Bike Business Record - Sheet1 (1).csv")
total_bikes = len(df)

sold_bikes = len(df[df["Status"] == "Sold"])

inventory = len(df[df["Status"] != "Sold"])

total_profit = df["total_profit"].fillna(0).sum()

money_in_stock = df[df["Status"] != "Sold"]["total_cost"].sum()

col1, col2, col3, col4, col5 = st.columns([1,1,1,2,2])

col1.metric("Total Bikes", total_bikes)
col2.metric("Sold", sold_bikes)
col3.metric("Inventory", inventory)
col4.metric("Profit", f"₹{total_profit:,.0f}")
col5.metric("Stock Value", f"₹{money_in_stock:,.0f}")


df["total_profit"] = pd.to_numeric(df["total_profit"], errors="coerce")

st.title("Bike Business Dashboard")

#st.metric("Total Profit", f"₹{df['total_profit'].sum():,.0f}")

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
brand_summary = (
    df.groupby("bike_brand")
    .agg(
        Bikes=("bike_brand", "count"),
        Profit=("total_profit", "sum")
    )
    .reset_index()
)

st.subheader("Brand Performance")

st.dataframe(brand_summary)

st.dataframe(df)
