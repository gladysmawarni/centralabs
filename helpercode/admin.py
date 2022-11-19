## ------------------------------ LIBRARY ----------------------------------------
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd

from helpercode.streamplot import progress_bar_chart

## ----------------------------- DATABASE --------------------------------------
## dev
# db = firestore.Client.from_service_account_json("db/firestore-key.json")

## prod
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")


## ----------------------------- FUNCTIONS ---------------------------------------
def df_progress(cohort):
    ref = db.collection("registered")
    registered_users = [i.to_dict() for i in ref.stream()]
    current_cohort_users = [usr['username'] for usr in registered_users if (usr['cohort'] == cohort) & (usr['username'] != 'gladysmawarni')]

    deliv = []
    not_deliv = []
    percentage = []
    for user in current_cohort_users:
        cohort_ref = db.collection("labs").document(user)
        x = cohort_ref.get().to_dict()
        deliv.append(len([i for i in  x.values() if i =='Delivered']))
        not_deliv.append(len([i for i in  x.values() if i =='Not delivered']))
        percentage.append(str(round((len([i for i in  x.values() if i =='Delivered']) / 43) * 100, 2)) + '%')
    
    df = pd.DataFrame([current_cohort_users, deliv, not_deliv, percentage]).T
    return df.rename(columns={0:'Student', 1:'Delivered', 2:'Not delivered', 3:'Percentage'})


# page
def student_progress():
    option = st.selectbox(
        "Select a cohort",
        ("DAFTOCT21", "DAFTJAN22", "DAFTAPR22", "DAFTJUL22", "DAFTOCT22"))

    studentprogdf = df_progress(option)
    progress_bar_chart(studentprogdf)

