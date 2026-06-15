import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv("Bike Business Record - Sheet1 (1).csv")

# Clean Data
df["total_profit"] = pd.to_numeric(df["total_profit"], errors="coerce").fillna(0)
df["total_cost"] = pd.to_numeric(df["total_cost"], errors="coerce").fillna(0)
df["date_sold"] = pd.to_datetime(df["date_sold"], errors="coerce")
df["date_sold"] = pd.to_datetime(df["date_sold"],dayfirst=True,errors="coerce")

# =========================
# KPI CARDS
# =========================

total_bikes = len(df)
sold_bikes = len(df[df["Status"] == "Sold"])
inventory = len(df[df["Status"] != "Sold"])
total_profit = df["total_profit"].sum()
money_in_stock = df[df["Status"] != "Sold"]["total_cost"].sum()

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 2])

col1.metric("Total Bikes", total_bikes)
col2.metric("Sold", sold_bikes)
col3.metric("Inventory", inventory)
col4.metric("Profit", f"₹{total_profit:,.0f}")
col5.metric("Stock Value", f"₹{money_in_stock:,.0f}")

st.title("🏍️ Bike Business Dashboard")

# =========================
# PROFIT BY BRAND
# =========================

sold_df = df[df["Status"] == "Sold"]

brand_profit = (
    sold_df.groupby("bike_brand")["total_profit"]
    .sum()
    .reset_index()
    .sort_values("total_profit", ascending=False)
)
st.write(df["Status"].unique())
# =========================
# MONTHLY SALES TREND
# =========================

monthly_sales = (
    sold_df.dropna(subset=["date_sold"])
    .groupby(sold_df["date_sold"].dt.to_period("M"))
    .size()
    .reset_index(name="Bikes Sold")
)

monthly_sales["date_sold"] = monthly_sales["date_sold"].astype(str)

# =========================
# SIDE-BY-SIDE CHARTS
# =========================

col_left, col_right = st.columns(2)

with col_left:
    fig1 = px.bar(
        brand_profit,
        x="bike_brand",
        y="total_profit",
        title="Profit by Brand"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    fig2 = px.line(
        monthly_sales,
        x="date_sold",
        y="Bikes Sold",
        markers=True,
        title="Monthly Sales Trend"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# BRAND PERFORMANCE
# =========================

brand_summary = (
    sold_df.groupby("bike_brand")
    .agg(
        Bikes=("bike_brand", "count"),
        Profit=("total_profit", "sum"),
        Avg_Profit=("total_profit", "mean")
    )
    .reset_index()
    .sort_values("Profit", ascending=False)
)

st.subheader("🏆 Brand Performance")

st.dataframe(
    brand_summary,
    use_container_width=True
)

# =========================
# INVENTORY BY BRAND
# =========================

inventory_df = df[df["Status"] != "Sold"]

inventory_brand = (
    inventory_df.groupby("bike_brand")
    .size()
    .reset_index(name="In Stock")
    .sort_values("In Stock", ascending=False)
)

st.subheader("📦 Inventory by Brand")

st.dataframe(
    inventory_brand,
    use_container_width=True
)

# =========================
# RAW DATA
# =========================
# =========================
# OLDEST & NEWEST INVENTORY
# =========================

inventory_df = df[df["Status"] != "Sold"].copy()

inventory_df["date_purchased"] = pd.to_datetime(
    inventory_df["date_purchased"],
    dayfirst=True,
    errors="coerce"
)

inventory_df = inventory_df.dropna(subset=["date_purchased"])

if not inventory_df.empty:

    oldest_bike = inventory_df.loc[
        inventory_df["date_purchased"].idxmin()
    ]

    newest_bike = inventory_df.loc[
        inventory_df["date_purchased"].idxmax()
    ]

    today = pd.Timestamp.today()

    oldest_days = (
        today - oldest_bike["date_purchased"]
    ).days

    newest_days = (
        today - newest_bike["date_purchased"]
    ).days

    st.subheader("⏳ Inventory Ageing")

    col1, col2 = st.columns(2)

    with col1:
        st.warning(
            f"""
**🕰️ Oldest Bike in Stock**

**{oldest_bike['bike_brand']} {oldest_bike['model']}**

Purchased: {oldest_bike['date_purchased'].date()}

Days in Stock: {oldest_days}
"""
        )

    with col2:
        st.success(
            f"""
**🆕 Newest Bike in Stock**

**{newest_bike['bike_brand']} {newest_bike['model']}**

Purchased: {newest_bike['date_purchased'].date()}

Days in Stock: {newest_days}
"""
        )
st.subheader("📋 Complete Inventory")

st.dataframe(
    df,
    use_container_width=True
)
