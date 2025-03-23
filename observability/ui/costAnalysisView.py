import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

# API Endpoint (Replace with actual API)
API_URL = "https://fn-get-insight.azurewebsites.net/api/aoai_pricing_appinsight_api"

# Token cost per unit (adjust as needed)
INPUT_TOKEN_COST = 0.00000395789
OUTPUT_TOKEN_COST = 0.0000158316

# Function to Fetch API Data
@st.cache_data(ttl=10)  # Refresh every 10 seconds
def fetch_api_data(username=""):
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame([entry[0] for entry in data["data"]])
        if username:
            df = df[df["User"].str.lower() == username.lower()]
        return df
    else:
        st.error("Failed to fetch data from API.")
        return pd.DataFrame()

# Auto-refresh mechanism
def auto_refresh(interval=10):
    time.sleep(interval)
    st.rerun()  # Updated from `st.experimental_rerun()`

# Streamlit Page Config
st.set_page_config(page_title="API Cost Dashboard", layout="wide")

# **Custom CSS for Vibrant UI**
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f5;
    }
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .data-section {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        color: white;
    }
    .tile {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    .tile-blue { background: #3498db; }
    .tile-green { background: #2ecc71; }
    .tile-red { background: #e74c3c; }
    .table-container {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>🚀 API Cost Dashboard (Auto-Refreshing 🔄)</h1>", unsafe_allow_html=True)

# **User Input for API Filtering**
username = st.text_input("🔍 Enter User Name to Filter Data:")

st.empty()

df = fetch_api_data(username)

if df.empty:
    st.warning("⚠️ No data available for the selected user.")
else:
    # **Token Cost Calculation**
    df["InputToken"] = df["InputToken"].astype(int)
    df["OutputToken"] = df["OutputToken"].astype(int)
    df["Input Cost"] = df["InputToken"] * INPUT_TOKEN_COST
    df["Output Cost"] = df["OutputToken"] * OUTPUT_TOKEN_COST
    df["Total Cost"] = df["Input Cost"] + df["Output Cost"]

    # **Colorful Metric Tiles**
    st.markdown("### 💰 Token Cost Breakdown")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='tile tile-blue'>🔵 Total Input Tokens <br> <h2>{df['InputToken'].sum()}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='tile tile-green'>🟢 Total Output Tokens <br> <h2>{df['OutputToken'].sum()}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='tile tile-red'>🔴 Total Cost ($) <br> <h2>{round(df['Total Cost'].sum(), 4)}</h2></div>", unsafe_allow_html=True)

    # **Modern Data Grid with Styling**
    st.markdown("### 📊 API Calls Data")
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    st.data_editor(df, hide_index=True, height=300)
    st.markdown("</div>", unsafe_allow_html=True)

    # **Interactive Data Visualizations**
    st.markdown("### 📈 API Performance & Cost Analysis")

    fig = px.bar(df, x="User", y=["Input Cost", "Output Cost"], barmode="group",
                 title="💸 Cost Breakdown by User", color_discrete_map={"Input Cost": "#3498db", "Output Cost": "#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(df, names="User", values="Total Cost", title="🏆 Total Cost Distribution",
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig2, use_container_width=True)

# **Auto Refresh**
st.markdown("🔄 Auto-refreshing every 10 seconds...")
auto_refresh(10)