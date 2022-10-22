# import streamlit 
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json


## ----- functions -----
def login():
    ## dev
    # db = firestore.Client.from_service_account_json("users/firestore-key.json")

    ## prod
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="centralabs99")

    users = db.collection('registered')

    emails = [user.to_dict()['email'] for user in users.stream()]


    with st.form('login_form'):
        st.subheader('Login')
        email = st.text_input('Email')
        password = st.text_input('Password', type= 'password')
        submit = st.form_submit_button('Login')

    if (not email) | (not password):
        st.warning('Please fill in your information')
    else:
        if email not in emails:
            st.error('User not registered')
        else:
            logged_user = users.document(email).get().to_dict()
            if password != logged_user['password']:
                st.error('Password incorrect')
            else:
                st.success('Logged in!')

                ## session state
                st.session_state.name = logged_user['name']
                st.session_state.authenticated = True
                
                return True
                
    
def pageOne():
    st.write(f'Welcome *{st.session_state.name}*')
    st.write("Seems like you've logged in!")

def pageTwo():
    st.write("second page")


## ----- app -----
selection = None

# if user not logged in 
if "navigation" not in st.session_state:
    st.session_state.navigation = ["login"]
    selection = st.session_state.navigation

if "authenticated" not in st.session_state:
    selection = st.sidebar.radio(label="pages", options=st.session_state.navigation)
    if login():
        st.session_state.navigation = ["pageone", "pagetwo"]

# if user logged in
if "authenticated" in st.session_state and st.session_state['authenticated'] == True:
    selection = st.sidebar.radio(label="pages", options=st.session_state.navigation)

if selection == "pageone":
    pageOne()

if selection == "pagetwo":
    pageTwo()