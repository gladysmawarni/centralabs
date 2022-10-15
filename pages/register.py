import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json


def register():
    ## dev
    # db = firestore.Client.from_service_account_json("users/firestore-key.json")

    ## prod
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="centralabs99")

    preauth = db.collection('preauthorized')


    emails = [doc.to_dict()['email'] for doc in preauth.stream()]

    with st.form('register_form'):
        st.subheader('Registration')
        email = st.text_input('Email')
        username = st.text_input('Username').lower()
        name = st.text_input('Name')
        password = st.text_input('Password', type= 'password')
        password2 = st.text_input('Re-type Password', type= 'password')
        submit = st.form_submit_button('Register')

    if (not email) | (not username) | (not name) | (not password):
        st.warning('Please fill in your information')
    else:
        if email not in emails:
            st.error('User not authorized')
        elif password != password2:
            st.error('Password does not match')
        else:
            user_ref = db.collection('registered').document(email)
            user_ref.set(
                {
                    "email" : email,
                    "username" : username,
                    "name" : name,
                    "password" : password
                }
            )
            ## TODO : delete registered preauthorized email
            st.success('Successfully registered :)')

register()