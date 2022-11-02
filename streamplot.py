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