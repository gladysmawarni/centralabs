## ------------------------------ LIBRARY ----------------------------------------
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
from datetime import datetime, date
import streamlit.components.v1 as components

from helpercode.streamplot import donut_chart, time_of_day_chart, day_of_week_chart, daily_line_chart
from helpercode.labs import weekly_progress, weekly_table

## ----------------------------- DATABASE --------------------------------------
## dev
# db = firestore.Client.from_service_account_json("db/firestore-key.json")

## prod
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")

st.set_page_config(page_title='Centralabs', page_icon=':coffee:', layout="wide")

## ----------------------- FUNCTION -------------------------
## session state - Medea for demo
st.session_state.name = 'Medea Langer'
st.session_state.username = 'medea22'
st.session_state.cohort = 'DAFTOCT21'


st.session_state.labs = db.collection('labs').document('medea22').get().to_dict()
st.session_state.labstime = db.collection("time").document('medea22').get().to_dict()
st.session_state.comments = db.collection("comments").document('medea22').get().to_dict()

def hello():
    currentTime = datetime.now()
    if currentTime.hour < 12:
        greeting ='Good morning,'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good afternoon,'
    else:
        greeting = 'Good evening,'

    st.title(f'{greeting} *Student*!')

    today = date.today()
    d1 = today.strftime("%B %d, %Y")
    st.subheader(d1)
    st.write('\n')

    ## status
    st.header('Your status')
    mood = st.multiselect(
    "How are you today?",
    ('😄', '🙂', '😥', '😟', '🥳', '🤒'))

    song = st.text_input('Insert your theme song for today','')

    submit_stat = st.button('Share your status')

## second page - overview
def overview():
    st.title(f"Student's labs overview")

    col1, col2 = st.columns([2,1])

    with col1:
        donut_chart(st.session_state.labs)
    with col2:
        '\n' 
        '\n'
        '\n'
        '\n'
        '\n'
        st.write(weekly_progress(st.session_state.labstime))
    
    coll1, coll2, coll3 = st.columns([1,2,1])
    
    with coll2: 
        weeknumopt = st.selectbox(
        'select a week',
        ('week1', 'week2', 'week3', 'week4', 'week5', 'week7', 'week8'))

        st.write(weekly_table(st.session_state.labstime, weeknumopt))
        
    try:
        daily_line_chart(st.session_state.labstime)
        day_of_week_chart(st.session_state.labstime)
        time_of_day_chart(st.session_state.labstime)
    except:
        st.write('not enough data')

## third page - comments
def load_css():
    with open('style.css') as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def comments():
    st.title(f"Student's labs comments")

    load_css()
    for i in st.session_state.comments:
        if '👌🏻' in st.session_state.comments[i]:
            st.subheader(i)
            text = f"<div class= 'highlight ok'>{st.session_state.comments[i]}</div>"
            st.markdown(text, unsafe_allow_html=True)
        else:
            st.subheader(i)
            text = f"<div class= 'highlight notok'>{st.session_state.comments[i]}</div>"
            st.markdown(text, unsafe_allow_html=True)

## fourth page - status
def status():
    today = date.today()
    d1 = today.strftime("%B %d, %Y")

    st.title(f"Students status")

    cohort_ref = db.collection('status').document('November 14, 2022').collection('DAFTOCT22')
    cohort_stat_li = [i.to_dict() for i in cohort_ref.get()]

    for userstat in cohort_stat_li:
        st.header(f"{(userstat['name']).title()}'s mood: {' '.join(userstat['mood'])}")

        minipvar = userstat['song'][:25]+'embed/'+userstat['song'][25:]
        miniplayer = f"""
            <iframe style="border-radius:12px" src="{minipvar[:-20]}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
            """
        components.html(miniplayer, height=400)


## ------------------------- DEMO ----------------------------
st.session_state.navigation = ["hello 👋", "overview 👀", "comments 💡", "status 💭"]
selection = st.sidebar.radio("navigation", st.session_state.navigation)

if selection == "hello 👋":
    hello()

if selection == "overview 👀":
    overview()

if selection == "comments 💡":
    comments()

if selection == "status 💭":
    status()