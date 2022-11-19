import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np


### ------------------- student page -------------------------
## first chart - donut plot of lab's progress
def donut_chart(ref):
    user_df = pd.DataFrame.from_dict(ref, orient='index').reset_index().rename(columns={'index':'labs', 0:'status'})
    count_delivered = len(user_df[user_df['status'] == 'Delivered'])
    count_not_delivered = len(user_df[user_df['status'] == 'Not delivered'])

    labels = ['Delivered','Not Delivered']
    values = [count_delivered, count_not_delivered]
    colours = ['teal', 'lightgray']
    legend = str(count_delivered) + '/' + '43'

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, pull=[0.2,0], marker=dict(colors=colours))])
    fig.update_layout(annotations= [{'text': legend, 'font_size' : 20, 'showarrow' : False}])

    st.plotly_chart(fig, use_container_width=True)


## time of day - horizontal bar chart
def time_classification(hour):
    # 06.00 - 12.00
    # 12.00 - 18.00
    # 18.00 - 24.00
    # 24.00 - 06.00
    
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    elif 18 <= hour < 24:
        return 'Night'
    else:
        return 'Dawn'

def count_time(li):
    timedict = {'Morning' : 0, 'Afternoon' : 0, 'Night': 0, 'Dawn' : 0}
    for i in li:
        timedict[i] += 1
    return timedict


def time_of_day_chart(ref):
    timestamps = list(ref.values())
    lamfunctime = lambda x: int(x.split('T')[1][:2])

    timeli = list(map(lamfunctime, timestamps))

    result = list(map(time_classification, timeli))
    final = count_time(result)

    
    ## plot
    fig = go.Figure()
    colors = ['rgb(237,221,206)', 'rgb(205,155,154)', '#5c7998', 'rgb(72,68,65)']
    label = ['🔆', '🌞',  '🌙' ,'⛅']

    for index, key in enumerate(final):
        fig.add_trace(go.Bar(
            y=[''],
            x=[final[key]],
            name=key,
            orientation='h',

            texttemplate= label[index], 
            textposition='inside',
            insidetextanchor="middle",

            marker_color= colors[index],
            hovertemplate= "%{x}",   
            )
        )

    fig.update_layout(title = 'Time of day',
                    barmode='stack',
                    font=dict(size=20),
                    showlegend=False,
                    xaxis=dict(showgrid=False, visible= False, showticklabels= False),
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=250
                    )

    
    st.plotly_chart(fig, use_container_width=True)


## day of week = horizontal bar chart
def countday(li):
   wdays = [datetime.strptime(i,'%Y-%m-%d').weekday() for i in li]

   daydict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
   countdict = {'Monday' : 0, 'Tuesday' : 0, 'Wednesday': 0, 'Thursday' : 0, 'Friday' : 0, 'Saturday' : 0, 'Sunday' : 0}

   for d in wdays:
      dow = daydict[d]
      countdict[dow] += 1
   
   return countdict


def day_of_week_chart(ref):
    timestamps = list(ref.values())
    lamfuncdate = lambda x: x.split('T')[0]

    dateli = list(map(lamfuncdate, timestamps))
    finaldays = countday(dateli)


    ## plot
    fig = go.Figure()
    colors = ['#FEF3D2', '#EDCFC0', '#EDC0C0', '#C3D3D6', '#D5DBE4', '#E4D5E3', '#EAEEE0']
    label = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for index, key in enumerate(finaldays):
        fig.add_trace(go.Bar(
            y=[''],
            x=[finaldays[key]],
            name=key,
            orientation='h',

            texttemplate= label[index], 
            textposition='inside',
            insidetextanchor="middle",

            marker_color= colors[index],
            hovertemplate= "%{x}",   
            )
        )

    fig.update_layout(title = 'Day of the week',
                    barmode='stack',
                    font=dict(size=20),
                    showlegend=False,
                    xaxis=dict(showgrid=False, visible= False, showticklabels= False),
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=250
                    )

    st.plotly_chart(fig, use_container_width=True)

def daily_line_chart(ref):
    timestamps = list(ref.values())
    lamfuncdate = lambda x: x.split('T')[0]

    dateli = list(map(lamfuncdate, timestamps))
    val, count = np.unique(dateli, return_counts=True)
    
    fig = go.Figure(data=go.Scatter(x=val, y=count, line_shape='spline', marker_color='#62809A'))

    fig.update_layout(title = 'Daily line chart', 
                showlegend=False,
                font=dict(size=20),
                xaxis=dict(showgrid=False),
                yaxis =dict(showgrid=False, visible= False, showticklabels= False),
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
                )

    st.plotly_chart(fig, use_container_width=True)


### ----------------- admin page ----------------------------
## bar chart - student progress
def progress_bar_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x =df['Student'], y= df['Delivered'], hovertext= df['Percentage'],
                        texttemplate = "%{y} / 43 =<br><b>%{hovertext}</b>",
                        textfont_color="white"))
    fig.update_layout(yaxis_range=[0,43])
    fig.update_traces(marker_color='rgb(250, 175, 196)', marker_line_color='rgb(250, 100, 142)',
                    marker_line_width=1.5, hovertemplate = "<extra></extra>")


    fig.add_trace(go.Scatter(x= df['Student'], y=[31 for i in df['Student']], mode = 'lines', line=dict(color="rgb(137, 94, 189)")))

    fig.update_layout(title = 'Student Progress', 
            showlegend=False,
            font=dict(size=13),
            xaxis=dict(showgrid=False),
            yaxis =dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            height=500
            )

    st.plotly_chart(fig, use_container_width=True)

