## ------------------------------ LIBRARY ----------------------------------------
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd
import time
from datetime import datetime, date
import streamlit.components.v1 as components

from helpercode.streamplot import progress_bar_chart
from helpercode.labs import Labs

## ----------------------------- DATABASE --------------------------------------
## dev
# db = firestore.Client.from_service_account_json("db/firestore-key.json")

## prod
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")

st.set_page_config(page_title='Centralabs', page_icon=':coffee:', layout="wide")
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


weeklylabsdict = {'week1' : ['lablistcomprehensions', 'labtuplesetdict', 'labstringoperations', 'labnumpy', 'labintropandas'],
'week2' : ['labmysqlfirstqueries', 'labmysqlselect', 'labmysql', 'labdataframecalculations', 'labadvancedpandas', 'labimportexport', 'labdatacleaning', 'lablambdafunctions'],
'week3' : ['labapiscavenger', 'labwebscraping', 'labpandasdeepdive', 'labadvancedregex', 'labmatplotlibseaborn'],
'week4' : ['labintrobitableau', 'labbianalysistableau', 'labpivottableandcorrelation', 'DescriptiveStats', 'labregressionanalysis', 'labsubsettinganddescriptivestats'],
'week5' : ['labintroprob', 'labprobabilitydistributions', 'M2miniproject2', 'labconfidenceintervals', 'labhypothesistesting1', 'labhypothesistesting2', 'labintrotoscipy', 'labtwosamplehyptest', 'labgoodfitindeptests'],
'week7' : ['labintrotoml', 'labsupervisedlearningfeatureextraction', 'labsupervisedlearning', 'labsupervisedlearningsklearn', 'labimbalance', 'labproblemsinml'],
'week8' : ['labunsupervisedlearning', 'labunsupervisedlearningandsklearn', 'labdeeplearning', 'labnlp']}


def weekly_review_progress(cohort, num):
    students = db.collection('registered')
    students_username = [i.to_dict()['username'] for i in students.where('cohort', '==', cohort).get() if i.to_dict()['username'] != 'gladysmawarni']

    final_dict = {}
    for student in students_username:
        user_labs = db.collection('labs').document(student).get().to_dict()
        user_comments = db.collection('comments').document(student).get().to_dict()

        delivered = set([stat for stat in user_labs.keys() if (user_labs[stat] == 'Delivered') & (stat in weeklylabsdict[num])])
        not_delivered = set([stat for stat in user_labs.keys() if (user_labs[stat] == 'Not delivered') & (stat in weeklylabsdict[num])])
        commented = set([stat for stat in user_comments.keys() if (stat in weeklylabsdict[num])])

        # delivered no comment
        deliv_nocomm = {name: '🌓' for name in (delivered - commented)}
        # delivered and commented
        deliv_yescomm = {name: '🌕' for name in (delivered - (delivered-commented))}
        # not delivered
        notdeliv = {name: '🌑' for name in not_delivered}

        notdeliv.update(deliv_nocomm)
        notdeliv.update(deliv_yescomm)

        final_dict.update({student : notdeliv})

    return final_dict


## ----------------------------- PAGE -------------------------------------------
def hello():
    currentTime = datetime.now()
    if currentTime.hour < 12:
        greeting ='Good morning,'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good afternoon,'
    else:
        greeting = 'Good evening,'

    st.title(f'{greeting} *Admin*!')

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


def student_progress():
    cohort= st.selectbox(
        "Select a cohort",
        ("DAFTOCT21", "DAFTJAN22", "DAFTAPR22", "DAFTJUL22", "DAFTOCT22"))


    studentprogdf = df_progress(cohort)
    progress_bar_chart(studentprogdf)

    week = st.selectbox(
        "Select a week",
        ("week1", "week2", "week3", "week4", "week5", "week7", "week8"))

    overviewweek = weekly_review_progress(cohort, week)
    st.dataframe(data = pd.DataFrame(overviewweek), use_container_width= True)
    st.caption('🌑 - Not delivered 🌓 - Delivered + Not reviewed  🌕 - Delivered + Reviewed')

    

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


## ------------------ DEMO -------------------
st.session_state.navigation = ["hello 👋", "students progress 📊", "status 💭"]
selection = st.sidebar.radio("navigation", st.session_state.navigation)

if selection == "hello 👋":
    hello()
if selection == "students progress 📊":
    student_progress()
if selection == "status 💭":
    status()



