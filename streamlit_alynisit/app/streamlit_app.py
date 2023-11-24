import os
import pandas
import dotenv
import pymongo
import datetime
import streamlit

# take environment variables from .env.
dotenv.load_dotenv()

# Page configuration
streamlit.set_page_config(
    page_title="Dashboard - Alynisits",
    page_icon="random",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# MongoDB connection
@streamlit.cache_resource
def init_connection():
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    return pymongo.MongoClient(CONNECTION_STRING)

client = init_connection()

# Data retrieval
# @streamlit.cache_data(ttl=1)
def get_data():
    db = client.database_alynisit
    items = db.matlab.find()
    items = list(items)
    return items

items = get_data()

Day = [item["Day"] for item in items]
H = [item["H"] for item in items]
Q = [item["Q"] for item in items]

google_font_url = 'https://fonts.googleapis.com/css2?family=Prompt&display=swap'

if len(items) != 0:
    # Set the custom style with the Google Font
    custom_style = f"""
        <style>
            @import url('{google_font_url}');
            body {{
                font-family: 'Prompt', sans-serif;
            }}
        </style>
    """
    streamlit.markdown(custom_style, unsafe_allow_html=True)

    tab_graph, tab_chart = streamlit.tabs(["แสดงกราฟ", "แสดงรายละเอียด"])

    with tab_graph:
        streamlit.header('กราฟความต่างของระดับความสูงของน้ำกับอัตราการไหลของน้ำ', divider='rainbow')
        filter_options = streamlit.multiselect(
        'กรองข้อมูล',
        ['ระดับความสูงของน้ำ', 'อัตราการไหลของน้ำ'],
        ['ระดับความสูงของน้ำ', 'อัตราการไหลของน้ำ'])
        if "ระดับความสูงของน้ำ" in filter_options and "อัตราการไหลของน้ำ" in filter_options:
            graph_data = pandas.DataFrame({"Day": Day, "ระดับความสูงของน้ำ": H, "อัตราการไหลของน้ำ": Q})
            graph_data.set_index("Day", inplace=True)
            streamlit.line_chart(data=graph_data, use_container_width=True)
        elif "ระดับความสูงของน้ำ" in filter_options:
            graph_data = pandas.DataFrame({"Day": Day, "ระดับความสูงของน้ำ": H})
            graph_data.set_index("Day", inplace=True)
            streamlit.line_chart(data=graph_data, use_container_width=True)
        elif "อัตราการไหลของน้ำ" in filter_options:
            graph_data = pandas.DataFrame({"Day": Day, "อัตราการไหลของน้ำ": Q})
            graph_data.set_index("Day", inplace=True)
            streamlit.line_chart(data=graph_data, use_container_width=True)
        else:
            streamlit.error("กรุณาเลือกข้อมูลเพื่อแสดงกราฟ")
        streamlit.snow()

    with tab_chart:
        streamlit.header('รายละเอียดข้อมูลระดับความสูงของน้ำกับอัตราการไหลของน้ำในแต่ละวัน', divider='rainbow')
        data = pandas.DataFrame({"Day": Day, "ระดับความสูงของน้ำ": H, "อัตราการไหลของน้ำ": Q})
        streamlit.dataframe(data=data, hide_index=True)
        streamlit.balloons()

    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(pandas.DataFrame(items))

    streamlit.download_button(
        label="โหลดข้อมูลเป็นไฟล์ CSV",
        data=csv,
        file_name='water_data.csv',
        mime='text/csv',
    )
else:
    streamlit.error("ไม่มีข้อมูลเพื่อแสดงผล")
    streamlit.snow()