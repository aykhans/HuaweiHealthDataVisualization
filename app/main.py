import plotly.express as px
import json
import streamlit as st
from pathlib import Path


data_dir = Path(__file__).resolve().parent.parent / 'data'

st.set_page_config(page_title='Health Data Visualization',
                    page_icon=':bar_chart:',
                    layout='wide')

with open(data_dir / 'huawei_health_data.json') as f:
    data = json.load(f)

heart_rate = []
for i in range(len(data)):
    if data[i]['type'] == 7:
        heart_rate.append(float(data[i]['samplePoints'][0]['value']))

st.sidebar.header('Split Data:')
average_number = st.sidebar.number_input(
    f'Amount of data split (0 - {len(heart_rate)-1}): ',
    step=1,
    min_value=0,
    max_value=len(heart_rate)-1
)

if average_number > 1:
    heart_rate2 = []

    for i in range(0, len(heart_rate), average_number):
        t = heart_rate[i:i + average_number]
        heart_rate2.append(sum(t) / len(t))
    heart_rate = heart_rate2

st.plotly_chart(
    px.line(x=range(len(heart_rate)), y=heart_rate)
)