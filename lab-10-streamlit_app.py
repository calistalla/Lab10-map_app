import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="California Housing Data (1990) by Harry Wang", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
    return df

df = load_data()


with st.sidebar:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #F7F8FB;
            border-right: 1px solid #E0E0E0;
        }
        div[data-testid="stSidebar"] h2 {
            font-size: 1.3rem;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Choose the location type")
    location_options = df["ocean_proximity"].unique().tolist()
    selected_locations = st.multiselect(
        "",
        location_options,
        default=location_options
    )

    st.header("Choose income level")
    income_level = st.radio("", ["Low", "Medium", "High"])

st.title("California Housing Data (1990) by Harry Wang")
min_price = int(df["median_house_value"].min())
max_price = 600000

price_slider = st.slider(
    "Minimal Median House Value",
    min_price,
    max_price,
    value=(200000, 600000),
    step=5000
)

st.write("See more filters in the sidebar:")

df_filtered = df[
    (df["median_house_value"] >= price_slider[0]) &
    (df["median_house_value"] <= price_slider[1]) &
    (df["ocean_proximity"].isin(selected_locations))
]

if income_level == "Low":
    df_filtered = df_filtered[df_filtered["median_income"] <= 2.5]
elif income_level == "Medium":
    df_filtered = df_filtered[(df_filtered["median_income"] > 2.5) & (df_filtered["median_income"] < 4.5)]
else:
    df_filtered = df_filtered[df_filtered["median_income"] >= 4.5]

st.map(df_filtered)

plt.style.use("seaborn-v0_8-darkgrid")

vals = df_filtered["median_house_value"].dropna()

x_min, x_max = 200_000, 600_000
bins = np.linspace(x_min, x_max, 31)
xticks = [200_000, 250_000, 300_000, 350_000, 400_000, 450_000, 500_000, 600_000]

vals = vals[(vals >= x_min) & (vals <= x_max)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(
    vals,
    bins=bins,
    edgecolor="white",
    linewidth=0.5,
    color="#3B5BA9",
    alpha=0.95
)

ax.set_xlim(x_min, x_max)
ax.set_xticks(xticks)
ax.set_xlabel("Median House Value ($)", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.set_title("Distribution of Median House Values (30 bins)", fontsize=14, fontweight="bold")
ax.grid(True, which="major", linestyle="-", alpha=0.3)

st.pyplot(fig)

st.caption("Data Source: California Housing Dataset (1990)")
