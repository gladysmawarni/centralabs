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


## ----------------------------- FUNCTIONS --------------------------------------
def login():

    # all the users who registered
    users = db.collection('registered')
    # list of registered emails
    usernames = [user.to_dict()['username'] for user in users.stream()]

    # login form
    with st.form('login_form'):
        st.subheader('Login')
        username = st.text_input('username').lower().strip()
        password = st.text_input('Password', type= 'password').strip()
        submit = st.form_submit_button('Login')

    # if the user did not fill all fields
    if (not username) | (not password):
        st.warning('Please fill in your information')
    else:
        # if email is not in database
        if username not in usernames:
            st.error('User not registered')
        else:
            # get the data of the user
            logged_user = users.document(username).get().to_dict()
            if password != logged_user['password']:
                st.error('Password incorrect')
            else:
                st.success('Logged in!')

                ## session state
                st.session_state.name = logged_user['name']
                st.session_state.username = username
                st.session_state.cohort = logged_user['cohort']
                st.session_state.authenticated = True


                st.session_state.labs = db.collection('labs').document(logged_user['username']).get().to_dict()
                st.session_state.labstime = db.collection("time").document(logged_user['username']).get().to_dict()
                st.session_state.comments = db.collection("comments").document(logged_user['username']).get().to_dict()
                return True


## first page - greetings
def hello():
    currentTime = datetime.now()
    if currentTime.hour < 12:
        greeting ='Good morning,'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good afternoon,'
    else:
        greeting = 'Good evening,'

    st.title(f'{greeting} *{(st.session_state.name.title())}*!')

    today = date.today()
    d1 = today.strftime("%B %d, %Y")
    st.subheader(d1)
    st.write('\n')

    ## status
    st.header('Your status')

    try:
        user_stat_ref = db.collection('status').document(d1).collection(st.session_state.cohort).document(st.session_state.username)
        user_status = user_stat_ref.get().to_dict()
        st.subheader(f"Today's mood : {' '.join(user_status['mood'])}", )
        st.subheader("Today's song : ")

        minipvar = user_status['song'][:25]+'embed/'+user_status['song'][25:]
        miniplayer = f"""
            <iframe style="border-radius:12px" src="{minipvar[:-20]}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
            """

        components.html(miniplayer, height=400)


    except:
        mood = st.multiselect(
        "How are you today?",
        ('😄', '🙂', '😥', '😟', '🥳', '🤒'))

        song = st.text_input('Insert your theme song for today','')

        submit_stat = st.button('Share your status')

        if submit_stat:
            if (len(song) < 1) or ('spotify' not in song):
                st.error('please put a spotify song link')
            else:
                user_stat_ref = db.collection('status').document(d1).collection(st.session_state.cohort).document(st.session_state.username)
                user_stat_ref.set(
                    {
                        "name" : st.session_state.name,
                        "mood" : mood,
                        "song" : song
                    }
                )

                st.success('Your status is updated!')

    logout = st.sidebar.button('goodbye')

    if logout:
        for key in st.session_state.keys():
            del st.session_state[key]


## second page - overview
def overview():
    st.title(f"{(st.session_state.name).title()}'s labs overview")

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
    st.title(f"{(st.session_state.name).title()}'s labs comments")

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

    st.title(f"{st.session_state.cohort} status: {d1}")

    cohort_ref = db.collection('status').document(d1).collection(st.session_state.cohort)
    cohort_stat_li = [i.to_dict() for i in cohort_ref.get()]

    for userstat in cohort_stat_li:
        st.header(f"{(userstat['name']).title()}'s mood: {' '.join(userstat['mood'])}")

        minipvar = userstat['song'][:25]+'embed/'+userstat['song'][25:]
        miniplayer = f"""
            <iframe style="border-radius:12px" src="{minipvar[:-20]}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
            """
        components.html(miniplayer, height=400)

    
