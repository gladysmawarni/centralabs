import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json
import streamlit as st



## prod
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")


class Labs:
    week1 = ['lab-list-comprehensions', 'lab-tuple-set-dict', 'lab-string-operations', 'lab-numpy', 'lab-intro-pandas']
    week2 = ['lab-mysql-first-queries', 'lab-mysql-select', 'lab-mysql', 'lab-dataframe-calculations', 'lab-advanced-pandas', 'lab-import-export', 'lab-data-cleaning', 'lab-lambda-functions']
    week3 = ['lab-api-scavenger', 'lab-web-scraping', 'lab-pandas-deep-dive', 'lab-advanced-regex', 'lab-matplotlib-seaborn']
    week4 = ['lab-intro-bi-tableau', 'lab-bi-analysis-tableau', 'lab-pivot-table-and-correlation', 'Descriptive-Stats', 'lab-regression-analysis', 'lab-subsetting-and-descriptive-stats']
    week5 = ['lab-intro-prob', 'lab-probability-distributions', 'M2-mini-project2', 'lab-confidence-intervals', 'lab-hypothesis-testing-1', 'lab-hypothesis-testing-2', 'lab-intro-to-scipy', 'lab-two-sample-hyp-test', 'lab-goodfit-indeptests']
    week7 = ['lab-intro-to-ml', 'lab-supervised-learning-feature-extraction', 'lab-supervised-learning', 'lab-supervised-learning-sklearn', 'lab-imbalance', 'lab-problems-in-ml']
    week8 = ['lab-unsupervised-learning', 'lab-unsupervised-learning-and-sklearn', 'lab-deep-learning', 'lab-nlp']

    def __init__(self, username) -> None:
        self.username = username
    
    def __updateLabsDB(self, lablist):
        user_ref = db.collection("labs").document(self.username)
        for lab in lablist:
            labspr = [lab['url'].split('ta-data-lis/')[1].split('/')[0].replace('-', '')]
            for labname in labspr:
                user_ref.update({labname : 'Delivered'})


    def checklabs(self):
        url = 'https://api.github.com/search/issues?q=state%3Aopen+author%3A'+ self.username + '+type%3Apr'
        response = requests.get(url=url, auth= HTTPBasicAuth('gladysmawarni', st.secrets["github_token"]))
        user_pr = response.json()

        try:
            lablist = [i['pull_request'] for i in user_pr['items']]
            self.__updateLabsDB(lablist)
        except:
            print('no pr yet')