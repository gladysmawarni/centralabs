import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json


labs_dict = {'lablistcomprehensions' : 'Not delivered',
'labtuplesetdict' : 'Not delivered',
'labstringoperations' : 'Not delivered',
'labnumpy' : 'Not delivered',
'labintropandas' : 'Not delivered',
'labmysqlfirstqueries' : 'Not delivered',
'labmysqlselect' : 'Not delivered',
'labmysql' : 'Not delivered',
'labdataframecalculations' : 'Not delivered',
'labadvancedpandas' : 'Not delivered',
'labimportexport' : 'Not delivered', 
'labdatacleaning' : 'Not delivered',
'lablambdafunctions' : 'Not delivered',
'labapiscavenger' : 'Not delivered',
'labwebscraping' : 'Not delivered',
'labpandasdeepdive' : 'Not delivered',
'labadvancedregex' : 'Not delivered',
'labmatplotlibseaborn' : 'Not delivered',
'labintrobitableau' : 'Not delivered',
'labbianalysistableau' : 'Not delivered',
'labpivottableandcorrelation' : 'Not delivered',
'DescriptiveStats' : 'Not delivered',
'labregressionanalysis' : 'Not delivered',
'labsubsettinganddescriptivestats' : 'Not delivered',
'labintroprob' : 'Not delivered',
'labprobabilitydistributions' : 'Not delivered',
'M2miniproject2' : 'Not delivered',
'labconfidenceintervals' : 'Not delivered',
'labhypothesistesting1' : 'Not delivered',
'labhypothesistesting2' : 'Not delivered',
'labintrotoscipy' : 'Not delivered',
'labtwosamplehyptest' : 'Not delivered',
'labgoodfitindeptests' : 'Not delivered',
'labintrotoml' : 'Not delivered',
'labsupervisedlearningfeatureextraction' : 'Not delivered',
'labsupervisedlearning' : 'Not delivered',
'labsupervisedlearningsklearn' : 'Not delivered',
'labimbalance' : 'Not delivered',
'labproblemsinml' : 'Not delivered',
'labunsupervisedlearning' : 'Not delivered',
'labunsupervisedlearningandsklearn' : 'Not delivered',
'labdeeplearning' : 'Not delivered',
'labnlp' : 'Not delivered'}

## DEV
# db = firestore.Client.from_service_account_json("db/firestore-key.json")

## PROD
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")


def register():
    preauth = db.collection('preauthorized')

    # emails of pre-authorized students
    preauthstudents = [(doc.to_dict()['email'], doc.to_dict()['cohort']) for doc in preauth.stream()]
 
    # registration form
    with st.form('register_form'):
        st.subheader('Registration')
        email = st.text_input('Email')
        name = st.text_input('Full Name').lower()
        username = st.text_input('Github username').lower()
        password = st.text_input('Password', type= 'password')
        password2 = st.text_input('Re-enter Password', type= 'password')
        submit = st.form_submit_button('Register')

    # if the user did not fill all the forms
    if (not email) | (not name) | (not password):
        st.warning('Please fill in your information')

    else:
        # if the passwords do not match
        if password != password2:
            st.error('Password does not match')

        else:
            flag = False
            for preauthemail, preauthcohort in preauthstudents:
                # if the email is pre-authorized
                if email == preauthemail:
                    user_ref = db.collection('registered').document(username)
                    user_ref.set(
                        {
                            "email" : email,
                            "name" : name,
                            "username" : username,
                            "password" : password,
                            "cohort" : preauthcohort
                        }
                    )

                    # populate labs db
                    populatedb(username)

                    st.success('Successfully registered :)')
                    flag = True

                     ## delete registered preauthorized email
                    delete_query = preauth.where('email', '==', preauthemail)
                    deleted = [doc.reference.delete() for doc in delete_query.get()]

            # if the email is not pre-authorized
            if flag == False:
                st.error('Email not pre-authorized.')


# make a new document in the 'labs' collection for the new registered user
def populatedb(username):
    # connect to user's labs collection
    labs_ref = db.collection("labs").document(username)
    # send the labs structure to db
    labs_ref.set(labs_dict)



register()