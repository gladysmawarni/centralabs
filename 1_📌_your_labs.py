# import streamlit 
from cProfile import label
import streamlit as st
import streamlit_authenticator as stauth
# import pyyaml module
import yaml
from yaml.loader import SafeLoader


## pages functions
def loginPage():
    with open('users/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')


    if st.session_state["authentication_status"]:
        st.success("Succesfully logged in! :tada:")
        st.session_state.logged_in = True
        st.session_state.navopts = ["pageone", "pagetwo"]
        st.session_state.username = username
        return True
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')



def pageOne():
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.write("Seems like you've logged in!")

def pageTwo():
    st.write("Jose is a bitch")




## streamlit run
# no selection at first
selection = None

# if user not logged in 
if "navopts" not in st.session_state:
    st.session_state.navopts = ["login"]
    selection = st.session_state.navopts

if "logged_in" not in st.session_state:
    selection = st.sidebar.radio(label="pages", options=st.session_state.navopts, label_visibility="hidden")
    if loginPage():
        st.session_state.navopts = ["pageone", "pagetwo"]

# if user logged in
if "logged_in" in st.session_state and st.session_state.logged_in == True:
    selection = st.sidebar.radio(label="pages", options=st.session_state.navopts, label_visibility="hidden")

if selection == "pageone":
    pageOne()

if selection == "pagetwo":
    pageTwo()