import os
import pymongo
import pandas as pd
import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Alynisits Dashboard", page_icon="🎄", layout="wide")  # Change page title and icon

# MongoDB connection
MONGO_DETAILS = "mongodb://TGR_GROUP3:ZK984B@mongoDB:27017"
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

# Data retrieval
@st.cache_data(ttl=1)
def get_data():
    db = client.database_alynisit
    items = db.hardware.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

# Extract data into separate lists
Name = [item["Name"] for item in items]
Date = [item["Date"] for item in items]
Month = [item["Month"] for item in items]
Year = [item["Year"] for item in items]
WaterDataFront = [item["WaterDataFront"] for item in items]
WaterDataBack = [item["WaterDataBack"] for item in items]
WaterDrainRate = [item["WaterDrainRate"] for item in items]

# Change background color
st.markdown(
    """
    <style>
        body {
            background-color: #f0f8ff;  /* Light blue color */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add Christmas theme decorations
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #228B22;">🎄 Alynisits Dashboard 🎄</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Create a grid layout for graphs
col1, col2, col3 = st.columns(3)

# Graph1: WaterDrainRate Over Time
with col1:
    st.header("Graph1: WaterDrainRate Over Time")
    chart_data_1 = pd.DataFrame({"Date": Date, "WaterDrainRate": WaterDrainRate})
    chart_data_1.set_index("Date", inplace=True)
    st.line_chart(chart_data_1)

# Graph2: WaterDataFront and WaterDataBack Over Time
with col2:
    st.header("Graph2: WaterDataFront and WaterDataBack Over Time")
    chart_data_2 = pd.DataFrame({"Date": Date, "WaterDataFront": WaterDataFront, "WaterDataBack": WaterDataBack})
    chart_data_2.set_index("Date", inplace=True)
    st.line_chart(chart_data_2)

# Charts1: WaterDataFront, WaterDataBack, and WaterDrainRate Over Time
with col3:
    st.header("Charts1: WaterDataFront, WaterDataBack, and WaterDrainRate Over Time")
    chart_data_3 = pd.DataFrame({"Date": Date, "WaterDataFront": WaterDataFront, "WaterDataBack": WaterDataBack, "WaterDrainRate": WaterDrainRate})
    chart_data_3.set_index("Date", inplace=True)
    st.bar_chart(chart_data_3)

# Date Selector
st.header("Date Selector")
start_time = st.slider(
    "Select a date",
    min_value=datetime(min(Year), min(Month), min(Date)),
    max_value=datetime(max(Year), max(Month), max(Date)),
    value=datetime(min(Year), min(Month), min(Date))
)
st.write("Selected date:", start_time)

# Selected Data Metrics
st.header("Selected Data Metrics")
selected_data = [item for item in items if datetime(item["Year"], item["Month"], item["Date"]) == start_time]
if selected_data:
    selected_item = selected_data[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("วันที่", start_time.strftime("%d/%m/%Y"))
    col2.metric("เดือน", selected_item["Month"])
    col3.metric("ปี", selected_item["Year"])

    st.metric(label="ชื่อ", value=selected_item["Name"])
    st.metric("น้ำที่เคยปล่อย", f"{selected_item['WaterDataFront']:.2f} ลบ.ม.")
    st.metric("น้ำที่มีอยู่", f"{selected_item['WaterDataBack']:.2f} ลบ.ม.")
    st.metric("การปล่อยน้ำ", f"{selected_item['WaterDrainRate']:.2f} ลบ.ม.")
else:
    st.warning("No data available for the selected date.")

# Raw Data Table
st.header("Raw Data Table")
st.dataframe(pd.DataFrame(items))

# Snow effect
st.snow()