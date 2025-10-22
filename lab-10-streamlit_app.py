import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="California Housing Data (1990) by Yifei Li", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
    return df

df = load_data()

# -------------------------------
min_price = int(df["median_house_value"].min())
max_price = int(df["median_house_value"].max())

price_filter = st.slider(
    "Select Minimal Median House Value",
    min_price,
    max_price,
    200000
)

filtered_df = df[df["median_house_value"] >= price_filter]

# -------------------------------
# 侧边栏：其他过滤器
# -------------------------------
st.markdown("### See more filters in the sidebar:")
st.sidebar.header("Filters")

location_types = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types
)

filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

# 收入水平筛选
income_level = st.sidebar.radio(
    "Choose income level",
    ("Low", "Medium", "High")
)

if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)
    ]
else:
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]

# -------------------------------
# 地图显示
# -------------------------------
st.subheader("House Locations on Map")
st.map(filtered_df[["latitude", "longitude"]])

# -------------------------------
# 直方图（与示例一致）
# -------------------------------
st.subheader("Histogram of Median House Value")

sns.set(style="darkgrid")  # ✅ 设置 seaborn 风格
plt.figure(figsize=(10, 6))

plt.hist(
    filtered_df["median_house_value"],
    bins=30,
    color="#1f77b4",   # seaborn 默认蓝色
    edgecolor="none"
)

plt.xlabel("Median House Value ($)")
plt.ylabel("Count")
plt.grid(True)

# 不设置标题、不改变字体权重
st.pyplot(plt.gcf())