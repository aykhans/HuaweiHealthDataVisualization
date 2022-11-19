# sourcery skip: list-comprehension
import pandas as pd
import plotly.express as px
import json
import streamlit as st
from datetime import (datetime,
                    timedelta)
from pathlib import Path


data_dir = Path(__file__).resolve().parent.parent / 'data'

st.set_page_config(page_title = 'Health Data Visualization',
                    page_icon = ':bar_chart:',
                    layout = 'wide')

with open(data_dir / 'huawei_health_data.json') as f:
    data = json.load(f)

heart_rate = []
for d in data:
    if d['type'] == 7:
        heart_rate.append(
            {
                'rate': float(d['samplePoints'][0]['value']),
                'time': (datetime.fromtimestamp(
                            int(str(d['samplePoints'][0]['endTime'])[:10])
                    ) + timedelta(
                            hours = int(data[0]['timeZone'][1:].replace('0', ''))
                        )
                )
            }
        )

if st.sidebar.checkbox(f'All Data ({len(heart_rate)})', False):
    if st.sidebar.checkbox('Average of Days', False):
        heart_rate = pd.DataFrame(
            list(
                map(
                    lambda t: {'rate': t['rate'], 'date': t['time'].strftime("%d-%m-%Y")}, heart_rate
                )
            )
        )
        heart_rate_grouped = heart_rate.groupby('date', sort=False).mean()['rate']
        x = heart_rate_grouped.keys()
        y = heart_rate_grouped.values

    else:
        heart_rate = pd.DataFrame(heart_rate)
        x = list(map(
            lambda t: t.strftime("%d-%m-%Y %X"),
            heart_rate['time']
        ))
        y = heart_rate['rate']

else:
    day = st.sidebar.date_input(
        'Select Day',
        heart_rate[0]['time'],
        min_value = heart_rate[0]['time'],
        max_value = heart_rate[-1]['time']
    ).strftime("%d-%m-%Y")

    heart_rate = pd.DataFrame(
        list(
            filter(
                lambda t: t['time'].strftime("%d-%m-%Y") == day, heart_rate
            )
        )
    )

    x = list(map(
        lambda t: t.strftime("%d-%m-%Y %X"),
        heart_rate['time']
    ))
    y = heart_rate['rate']

st.sidebar.header('Split Data:')
average_number = st.sidebar.number_input(
    f'Amount of data split (0 - {len(heart_rate)-1}): ',
    step = 1,
    min_value = 0,
    max_value = len(heart_rate)-1
)

if average_number > 1:
    heart_rate2 = []
    rates = list(y)

    for i in range(0, len(rates), average_number):
        t = rates[i:i + average_number]
        heart_rate2.append(sum(t) / len(t))
    x = range(len(heart_rate2))
    y = heart_rate2


st.plotly_chart(
    px.line(
        x = x, y = y
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