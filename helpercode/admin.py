## ------------------------------ LIBRARY ----------------------------------------
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd
import time

from helpercode.streamplot import progress_bar_chart
from helpercode.labs import Labs

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

    if st.button("refresh"):
        # all the users who registered
        users = db.collection('registered')
         # list of registered username
        usernames = [user.to_dict()['username'] for user in users.stream() if (user.to_dict()['cohort'] == 'DAFTOCT22') & (user.to_dict()['username'] != 'gladysmawarni')]

        progressbar = st.progress(0)

        count = 0
        for user in usernames: 
            print(user)
            time.sleep(5)
            user = Labs(user)
            user.refresh()
            user.getComments()
            count += int(100/len(usernames))
            progressbar.progress(count)

        progressbar.progress(100)
        st.success('all data updated!')
    



