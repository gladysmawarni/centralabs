## ------------------------------ LIBRARY ----------------------------------------
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

from helpercode.user import login, hello, overview, comments, status
from helpercode.admin import student_progress

## ----------------------------- DATABASE --------------------------------------
## dev
# db = firestore.Client.from_service_account_json("db/firestore-key.json")

## prod
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")


## ------------------------------ APP -----------------------------------
st.set_page_config(page_title='Centralabs', page_icon=':coffee:', layout="wide")

selection = None

# if user not logged in 
if "navigation" not in st.session_state:
    st.session_state.navigation = ["login"]
    selection = st.session_state.navigation

if "authenticated" not in st.session_state:
    selection = st.sidebar.radio("navigation", st.session_state.navigation)
    if login():
        ## user / admin
        if st.session_state.username == 'gladysmawarni':
            st.session_state.navigation = ["hello 👋", "students progress 📊", "status 💭"]
        else:
            st.session_state.navigation = ["hello 👋", "overview 👀", "comments 💡", "status 💭"]

# if user logged in
if "authenticated" in st.session_state and st.session_state.authenticated == True:
    selection = st.sidebar.radio("navigation", st.session_state.navigation)

    # user / admin
    if st.session_state.username == 'gladysmawarni':
        if selection == "hello 👋":
            hello()
        if selection == "students progress 📊":
            student_progress()
        if selection == "status 💭":
            status()
    else:
        if selection == "hello 👋":
            hello()

        if selection == "overview 👀":
            overview()

        if selection == "comments 💡":
            comments()

        if selection == "status 💭":
            status()