import plotly.graph_objects as go
import streamlit as st
import pandas as pd


## first chart - donut plot of lab's progress
def donutplot(user_dictionary):
    user_df = pd.DataFrame.from_dict(user_dictionary, orient='index').reset_index().rename(columns={'index':'labs', 0:'status'})
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
    colors = ['rgb(70, 152, 207)', 'rgb(235, 205, 108)', 'rgb(119, 83, 181)', 'rgb(179, 84, 133)']
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

    fig.update_layout(barmode='stack',
                    font=dict(size=20),
                    showlegend=False,
                    xaxis=dict(showgrid=False, visible= False, showticklabels= False),
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=350
                    )

    
    st.plotly_chart(fig, use_container_width=True)