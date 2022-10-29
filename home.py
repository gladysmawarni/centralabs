## ------------------------------ LIBRARY ----------------------------------------
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
from helper import Labs


## ----------------------------- FUNCTIONS --------------------------------------
def login():
    ## dev
    # db = firestore.Client.from_service_account_json("db/firestore-key.json")

    ## prod
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="centralabs99")

    # all the users who registered
    users = db.collection('registered')
    # list of registered emails
    emails = [user.to_dict()['email'] for user in users.stream()]

    # login form
    with st.form('login_form'):
        st.subheader('Login')
        email = st.text_input('Email')
        password = st.text_input('Password', type= 'password')
        submit = st.form_submit_button('Login')

    # if the user did not fill all fields
    if (not email) | (not password):
        st.warning('Please fill in your information')
    else:
        # if email is not in database
        if email not in emails:
            st.error('User not registered')
        else:
            # get the data of the user
            logged_user = users.document(email).get().to_dict()
            if password != logged_user['password']:
                st.error('Password incorrect')
            else:
                st.success('Logged in!')

                ## session state
                st.session_state.name = logged_user['name']
                st.session_state.authenticated = True
                st.session_state.navigation = ["pageone", "pagetwo"]
                st.session_state.labs = db.collection('labs').document(logged_user['name']).get().to_dict()     
                return True


## first chart - donut plot of lab's progress
def donutplot(user_dictionary):
    user_df = pd.DataFrame.from_dict(user_dictionary, orient='index').reset_index().rename(columns={'index':'labs', 0:'status'})
    count_delivered = len(user_df[user_df['status'] == 'Delivered'])
    count_not_delivered = len(user_df[user_df['status'] == 'Not delivered'])

    labels = ['Delivered','Not Delivered']
    values = [count_delivered, count_not_delivered]
    colours = ['teal', 'lightgray']
    legend = str(count_delivered) + '/' + str(count_not_delivered)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, pull=[0.2,0], marker=dict(colors=colours))])
    fig.update_layout(annotations= [{'text': legend, 'font_size' : 20, 'showarrow' : False}])

    st.plotly_chart(fig, use_container_width=True)
    
## first page - greetings
def pageOne():
    currentTime = datetime.now()
    if currentTime.hour < 12:
        greeting ='Good morning,'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good afternoon,'
    else:
        greeting = 'Good evening,'

    st.header(f'{greeting} *{st.session_state.name}*!')

    today = date.today()
    d1 = today.strftime("%B %d, %Y")
    st.header(d1)


    logout = st.sidebar.button('logout')

    if logout:
        for key in st.session_state.keys():
            del st.session_state[key]

## second page
def pageTwo():
    st.header(f"{st.session_state.name}'s labs progress")

    donutplot(st.session_state.labs)

    col1, col2 = st.columns(2)




## ------------------------------ APP -----------------------------------
selection = None

# if user not logged in 
if "navigation" not in st.session_state:
    st.session_state.navigation = ["login"]
    selection = st.session_state.navigation

if "authenticated" not in st.session_state:
    selection = st.sidebar.radio("", st.session_state.navigation)
    if login():
        st.session_state.navigation = ["pageone", "pagetwo"]

# if user logged in
if "authenticated" in st.session_state and st.session_state.authenticated == True:
    selection = st.sidebar.radio("", st.session_state.navigation)

if selection == "pageone":
    pageOne()

if selection == "pagetwo":
    pageTwo()