import streamlit as st
import streamlit_authenticator as stauth
# import pyyaml module
import yaml
from yaml.loader import SafeLoader

def register():
    with open('users/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)


    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    ## preauthorization True so only people with the email in config.yaml 'preauthorized' can register 
    ## after they signed up their email will be removed from the yaml file
    try:
        if authenticator.register_user('Register user', preauthorization=True):
            st.success('You registered successfully! Please go to the login page')
    except Exception as e:
        st.error(e)

    with open('users/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

register()