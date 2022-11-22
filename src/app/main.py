# sourcery skip: list-comprehension
from pathlib import Path
main_path: Path = Path(__file__).resolve().parent.parent

from sys import path
if str(main_path) not in path:
    path.append(str(main_path))

import plotly.express as px
import streamlit as st
from data_access import LocalDataAccess


st.set_page_config(page_title = 'Health Data Visualization',
                    page_icon = ':bar_chart:',
                    layout = 'wide')

local_data = LocalDataAccess('data')
_ = local_data.get_data('huawei_health_data.json')
heart_rate = local_data.get_heart_rate()

if st.sidebar.checkbox(f'All Data ({len(heart_rate)})', False):
    if st.sidebar.checkbox('Average of Days', False):
        x, y = local_data.get_average_heart_rate_for_days_as_axis()
        labels = {'x': 'Date of The Day', 'y': 'Average Heart Rate'}

    else:
        x, y = local_data.get_heart_rate_for_all_days_as_axis()
        labels = {'x': 'Date and Time', 'y': 'Heart Rate'}

else:
    day = st.sidebar.date_input(
        'Select Day',
        heart_rate[0]['time'],
        min_value = heart_rate[0]['time'],
        max_value = heart_rate[-1]['time']
    ).strftime("%d-%m-%Y")

    x, y = local_data.get_heart_rate_for_one_day(day)
    labels = {'x': 'Date and Time', 'y': 'Heart Rate'}

st.sidebar.header('Split Data:')
average_number = st.sidebar.number_input(
    f'Amount of data split (0 - {len(heart_rate)-1}): ',
    step = 1,
    min_value = 0,
    max_value = len(heart_rate)-1
)

if average_number > 1:
    x, y = local_data.get_averages_of_heart_rates(y, average_number)
    labels = {'x': 'Number of Heart Rate', 'y': 'Heart Rate'}

chart_type = st.sidebar.selectbox(
    'Chart Type',
    ('Line', 'Scatter', 'Bar')
)

st.plotly_chart(
    {'Line': px.line, 'Scatter': px.scatter, 'Bar': px.bar}[chart_type](
        x = x, y = y,
        labels = labels
    )
    .update_layout(
        xaxis = dict(
            rangeslider = dict(
                visible = True
            ),
            type = "-" # ['-', 'linear', 'log', 'date', 'category', 'multicategory']
        )
    )
)

st.plotly_chart(
    px.box(y = y, labels = {'y': 'Heart Rate'})
)