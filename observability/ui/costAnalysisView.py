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








# import streamlit as st
# import pandas as pd
# import requests
# import plotly.express as px

# # API Endpoint (Replace with actual API)
# API_URL = "https://fn-get-insight.azurewebsites.net/api/aoai_pricing_appinsight_api"

# # Token cost per unit (adjust as needed)
# INPUT_TOKEN_COST = 0.00000395789
# OUTPUT_TOKEN_COST = 0.0000158316

# # Function to Fetch API Data
# def fetch_api_data(username=""):
#     response = requests.get(API_URL)
#     if response.status_code == 200:
#         data = response.json()
#         df = pd.DataFrame([entry[0] for entry in data["data"]])
#         if username:
#             df = df[df["User"].str.lower() == username.lower()]
#         return df
#     else:
#         st.error("Failed to fetch data from API.")
#         return pd.DataFrame()

# # Streamlit Page Config
# st.set_page_config(page_title="API Cost Dashboard", layout="wide")

# # **Custom CSS for Vibrant UI**
# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #f0f2f5;
#     }
#     .main-title {
#         text-align: center;
#         font-size: 42px;
#         font-weight: bold;
#         color: #2c3e50;
#         margin-bottom: 20px;
#     }
#     .data-section {
#         background: linear-gradient(135deg, #6a11cb, #2575fc);
#         padding: 20px;
#         border-radius: 15px;
#         box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
#         margin-bottom: 20px;
#         color: white;
#     }
#     .tile {
#         padding: 20px;
#         border-radius: 12px;
#         text-align: center;
#         font-size: 18px;
#         font-weight: bold;
#         color: white;
#     }
#     .tile-blue { background: #3498db; }
#     .tile-green { background: #2ecc71; }
#     .tile-red { background: #e74c3c; }
#     .table-container {
#         background: white;
#         padding: 15px;
#         border-radius: 10px;
#         box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("<h1 class='main-title'>🚀 API Cost Dashboard</h1>", unsafe_allow_html=True)

# # **User Input for API Filtering**
# username = st.text_input("🔍 Enter User Name to Filter Data:")
# if st.button("🔄 Fetch Data"):
#     df = fetch_api_data(username)
# else:
#     df = fetch_api_data()

# if df.empty:
#     st.warning("⚠️ No data available for the selected user.")
# else:
#     # **Token Cost Calculation**
#     df["InputToken"] = df["InputToken"].astype(int)
#     df["OutputToken"] = df["OutputToken"].astype(int)
#     df["Input Cost"] = df["InputToken"] * INPUT_TOKEN_COST
#     df["Output Cost"] = df["OutputToken"] * OUTPUT_TOKEN_COST
#     df["Total Cost"] = df["Input Cost"] + df["Output Cost"]

#     # **Colorful Metric Tiles**
#     st.markdown("### 💰 Token Cost Breakdown")
#     col1, col2, col3 = st.columns(3)
#     col1.markdown(f"<div class='tile tile-blue'>🔵 Total Input Tokens <br> <h2>{df['InputToken'].sum()}</h2></div>", unsafe_allow_html=True)
#     col2.markdown(f"<div class='tile tile-green'>🟢 Total Output Tokens <br> <h2>{df['OutputToken'].sum()}</h2></div>", unsafe_allow_html=True)
#     col3.markdown(f"<div class='tile tile-red'>🔴 Total Cost ($) <br> <h2>{round(df['Total Cost'].sum(), 4)}</h2></div>", unsafe_allow_html=True)

#     # **Modern Data Grid with Styling**
#     st.markdown("### 📊 API Calls Data")
#     st.markdown("<div class='table-container'>", unsafe_allow_html=True)
#     st.data_editor(df, hide_index=True, height=300)
#     st.markdown("</div>", unsafe_allow_html=True)

#     # **Interactive Data Visualizations**
#     st.markdown("### 📈 API Performance & Cost Analysis")

#     fig = px.bar(df, x="User", y=["Input Cost", "Output Cost"], barmode="group",
#                  title="💸 Cost Breakdown by User", color_discrete_map={"Input Cost": "#3498db", "Output Cost": "#e74c3c"})
#     st.plotly_chart(fig, use_container_width=True)

#     fig2 = px.pie(df, names="User", values="Total Cost", title="🏆 Total Cost Distribution",
#                   color_discrete_sequence=px.colors.qualitative.Set3)
#     st.plotly_chart(fig2, use_container_width=True)




# import streamlit as st
# import pandas as pd
# import requests
# import json
# import altair as alt
# from st_aggrid import AgGrid, GridOptionsBuilder

# # API URL (Replace with actual API)
# API_URL = "https://fn-get-insight.azurewebsites.net/api/aoai_pricing_appinsight_api"

# # Function to fetch data from API
# def fetch_api_data(user=None):
#     params = {"user": user} if user else {}
#     response = requests.get(API_URL, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"data": []}

# # Function to calculate costs
# def calculate_cost(df, ittoken_cost=0.00000395789, ottoken_cost=0.0000158316):
#     df["Input Token Cost"] = df["InputToken"] * ittoken_cost
#     df["Output Token Cost"] = df["OutputToken"] * ottoken_cost
#     df["Total Cost"] = df["Input Token Cost"] + df["Output Token Cost"]
#     return df

# # Streamlit App Configuration
# st.set_page_config(page_title="API Cost Dashboard", layout="wide")

# # CSS Styling
# st.markdown(
#     """
#     <style>
#     .main-title {
#         text-align: center;
#         font-size: 36px;
#         font-weight: bold;
#         color: #007bff;
#         margin-bottom: 20px;
#     }
#     .sidebar-title {
#         font-size: 24px;
#         font-weight: bold;
#         color: #343a40;
#         margin-bottom: 10px;
#     }
#     .data-container {
#         padding: 20px;
#         background: white;
#         border-radius: 10px;
#         box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Title
# st.markdown("<h1 class='main-title'>API Cost Dashboard</h1>", unsafe_allow_html=True)

# # Sidebar Input for API Call
# st.sidebar.markdown("<h2 class='sidebar-title'>Fetch Data</h2>", unsafe_allow_html=True)
# user_input = st.sidebar.text_input("Enter User Name", "")
# if st.sidebar.button("Fetch Data"):
#     data = fetch_api_data(user_input)
#     print(f"Data fetched for user: {data}")
# else:
#     data = {"data": [
#         {"id": "fe4874cc808a2ee2", "operation_ParentId": "aa4ca32f29623882fcd10d8ed1940793", "target_usr": "Get4o Processing", "target_token": "chat", "name": "Get4o Processing", "user": "asif", "it": 20, "ot": 141}
       
#     ]}
#     {"data": [[{"ApiCall": "Get4o Processing", "User": "asif", "InputToken": "20", "OutputToken": "141", "Perforamnce": "1sec-3sec"}], [{"ApiCall": "Get4o Processing", "User": "John", "InputToken": "20", "OutputToken": "206", "Perforamnce": "3sec-7sec"}], [{"ApiCall": "Get4o Processing", "User": "asif", "InputToken": "20", "OutputToken": "223", "Perforamnce": "3sec-7sec"}]]}

# # Convert Data to DataFrame
# df = pd.DataFrame(data["data"])
# if not df.empty:
#     df = calculate_cost(df)

# # Display API Calls Count
# st.write("### Cost Breakdown of API Calls")
# st.write(f"**Total API Calls:** {len(df)}")

# # Ag-Grid for modern data display
# st.write("### API Call Details")
# gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_pagination()
# gb.configure_side_bar()
# gb.configure_default_column(editable=False, groupable=True)
# grid_options = gb.build()
# AgGrid(df, gridOptions=grid_options, height=300, theme="streamlit")

# # Token Cost Calculation Area
# st.write("### Token Cost Summary")
# st.write(f"**Token Cost per Unit:** $0.002")
# AgGrid(df[["User", "InputToken", "OutputToken", "Input Token Cost", "Output Token Cost", "Total Cost"]], gridOptions=grid_options, height=250, theme="streamlit")

# # Charts for Data Visualization
# st.write("### API Usage Overview")

# chart = (
#     alt.Chart(df)
#     .mark_bar()
#     .encode(
#         x="user:N",
#         y="Total Cost:Q",
#         color="user:N",
#         tooltip=["user", "Total Cost"]
#     )
# )
# st.altair_chart(chart, use_container_width=True)

# # chart2 = (
# #     alt.Chart(df)
# #     .mark_area(opacity=0.6)
# #     .encode(
# #         x="user:N",
# #         y="it:Q",
# #         color="user:N",
# #         tooltip=["user", "it"]
# #     )
# # )
# # st.altair_chart(chart2, use_container_width=True)


# import streamlit as st
# import pandas as pd
# import requests
# import plotly.express as px

# # API Endpoint (Replace with actual API)
# API_URL = "https://fn-get-insight.azurewebsites.net/api/aoai_pricing_appinsight_api"

# # Token cost per unit (adjust as needed)
# INPUT_TOKEN_COST = 0.00000395789
# OUTPUT_TOKEN_COST = 0.0000158316

# # Fetch Data Function
# def fetch_api_data(username=""):
#     response = requests.get(API_URL)
#     if response.status_code == 200:
#         data = response.json()
#         df = pd.DataFrame([entry[0] for entry in data["data"]])
#         if username:
#             df = df[df["User"].str.lower() == username.lower()]
#         return df
#     else:
#         st.error("Failed to fetch data from API.")
#         return pd.DataFrame()

# # Streamlit App Configuration
# st.set_page_config(page_title="API Cost Dashboard", layout="wide")

# # Custom CSS for Modern UI
# st.markdown(
#     """
#     <style>
#     .main-title {
#         text-align: center;
#         font-size: 36px;
#         font-weight: bold;
#         color: #2c3e50;
#         margin-bottom: 20px;
#     }
#     .data-section {
#         background: white;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#         margin-bottom: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("<h1 class='main-title'>API Cost Dashboard</h1>", unsafe_allow_html=True)

# # **User Input Section**
# username = st.text_input("Enter User Name to Filter Data:")
# if st.button("Fetch Data"):
#     df = fetch_api_data(username)
# else:
#     df = fetch_api_data()

# if df.empty:
#     st.warning("No data available for the selected user.")
# else:
#     # **Cost Calculation**
#     df["InputToken"] = df["InputToken"].astype(int)
#     df["OutputToken"] = df["OutputToken"].astype(int)
#     df["Input Cost"] = df["InputToken"] * INPUT_TOKEN_COST
#     df["Output Cost"] = df["OutputToken"] * OUTPUT_TOKEN_COST
#     df["Total Cost"] = df["Input Cost"] + df["Output Cost"]

#     # **Data Grid Display**
#     st.write("### API Calls Data")
#     st.data_editor(df, hide_index=True, height=300)

#     # **Cost Summary**
#     st.write("### Token Cost Breakdown")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Input Tokens", df["InputToken"].sum())
#     col2.metric("Total Output Tokens", df["OutputToken"].sum())
#     col3.metric("Total Cost ($)", round(df["Total Cost"].sum(), 4))

#     # **Visualization**
#     st.write("### API Performance & Cost Analysis")

#     fig = px.bar(df, x="User", y=["Input Cost", "Output Cost"], barmode="group",
#                  title="Cost Breakdown by User", color_discrete_map={"Input Cost": "blue", "Output Cost": "red"})
#     st.plotly_chart(fig, use_container_width=True)

#     fig2 = px.pie(df, names="User", values="Total Cost", title="Total Cost Distribution")
#     st.plotly_chart(fig2, use_container_width=True)
