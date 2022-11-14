import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from google.cloud import firestore
import streamlit as st
import json
from google.oauth2 import service_account



## prod
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="centralabs99")

#db = firestore.Client.from_service_account_json("db/firestore-key.json")
cleanlabnamefunc = lambda x: x.split('ta-data-lis/')[1].split('/')[0].replace('-', '')


class Labs:
    githubusername = 'gladysmawarni'
    #githubtoken = st.secrets["github_token"]
    githubtoken = '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'


    ### ------------- private functions ---------------
    def __init__(self, username) -> None:
        self.username = username
    
    def __getDB(self, collection):
        """fetch data from a specific collection in database"""
        return db.collection(collection).document(self.username)
    
    def __getPR(self, state):
        """fetch pull request data of the user, either open or closed"""
        url = 'https://api.github.com/search/issues'
        params= {'q': f'state:{state} author:{self.username} type:pr', 'per_page': 100}

        response = requests.get(url=url, params= params, auth= HTTPBasicAuth(self.githubusername, self.githubtoken))
        return response.json()['items']

    def __updateLabsStatus(self, lablist):
        """update labs status"""
        user_lab_ref = self.__getDB('labs')
        user_time_ref =self.__getDB('time')

        for labname, time in lablist:
            user_lab_ref.update({labname : 'Delivered'})
            user_time_ref.set({labname : time}, merge=True)
            print(self.username + ' : ' + labname)
    
    def __updateLabsComments(self,closedprlist):
        """get TA comments from github"""
        user_ref = self.__getDB('comments')
        try:
            done = list(user_ref.get().to_dict().keys())
            notdone = [pr for pr in closedprlist if pr not in done]

        except:
            # when there is no data in db comments yet
            notdone = [pr for pr in closedprlist]

        for url in notdone:
            response = requests.get(url=url, auth= HTTPBasicAuth(self.githubusername, self.githubtoken))
            urlresponse = response.json()
            try:
                labname = cleanlabnamefunc(urlresponse[0]['url'])
            except:
                pass
            
            for data in urlresponse:
                try:
                    if data['user']['login'] == 'ta-data-lis':
                        user_ref.set({labname: data['body']}, merge=True)
                        print(self.username + ': comments - ' + labname)
                except:
                    pass

    
    ## ------------ functions to use ------------------

    def refresh(self):
        """fetch data from github and update DB if there's a new PR"""
        user_pr = self.__getPR('open')

        try:
            labnames = [i['pull_request']['url'] for i in user_pr if 'ta-data-lis' in i['pull_request']['url']]

            # map to apply to all at once
            cleanlabsname = list(map(cleanlabnamefunc, labnames))

            timestamp = [i['created_at'][:-1] for i in user_pr]
            lablist = list(zip(cleanlabsname, timestamp))

            self.__updateLabsStatus(lablist)
        except:
            print('no pr yet')
            pass

    
    def getComments(self):
        """fetch comments from github to save in DB"""
        closedpr = self.__getPR('closed')
        closedprlist = [pr['timeline_url'] for pr in closedpr]
        self.__updateLabsComments(closedprlist)
    

    def doubleCheck(self):
        """check if there's any labs that is skipped and not updated in the DB"""
        user_lab_ref = self.__getDB('labs')
        user_time_ref = self.__getDB('time')

        closedpr = self.__getPR('closed')
        labnames = [i['pull_request']['url'] for i in closedpr if 'ta-data-lis' in i['pull_request']['url']]

        timelabs = list(user_time_ref.get().to_dict().keys())

        # map to apply to all at once
        cleanlabsname = list(map(cleanlabnamefunc, labnames))

        timestamp = [i['created_at'][:-1] for i in closedpr]
        lablist = list(zip(cleanlabsname, timestamp))

        closedprdf= pd.DataFrame(lablist, columns=['name', 'time'])
        finaldf = closedprdf[~closedprdf['name'].isin(timelabs)]

        if len(finaldf) > 0 :
            for labname, labtime in finaldf[['name', 'time']].values:
                user_lab_ref.update({labname : 'Delivered'})
                user_time_ref.set({labname : labtime}, merge=True)
                print('closed: ', self.username + ' : ' + labname)
        else:
            print('everything is fine')



weeklylabsdict = {'week1' : ['lablistcomprehensions', 'labtuplesetdict', 'labstringoperations', 'labnumpy', 'labintropandas'],
'week2' : ['labmysqlfirstqueries', 'labmysqlselect', 'labmysql', 'labdataframecalculations', 'labadvancedpandas', 'labimportexport', 'labdatacleaning', 'lablambdafunctions'],
'week3' : ['labapiscavenger', 'labwebscraping', 'labpandasdeepdive', 'labadvancedregex', 'labmatplotlibseaborn'],
'week4' : ['labintrobitableau', 'labbianalysistableau', 'labpivottableandcorrelation', 'DescriptiveStats', 'labregressionanalysis', 'labsubsettinganddescriptivestats'],
'week5' : ['labintroprob', 'labprobabilitydistributions', 'M2miniproject2', 'labconfidenceintervals', 'labhypothesistesting1', 'labhypothesistesting2', 'labintrotoscipy', 'labtwosamplehyptest', 'labgoodfitindeptests'],
'week7' : ['labintrotoml', 'labsupervisedlearningfeatureextraction', 'labsupervisedlearning', 'labsupervisedlearningsklearn', 'labimbalance', 'labproblemsinml'],
'week8' : ['labunsupervisedlearning', 'labunsupervisedlearningandsklearn', 'labdeeplearning', 'labnlp']}

def weekly_progress(ref):
    final = {}

    for i in ['week1', 'week2', 'week3', 'week4', 'week5', 'week7', 'week8']:
        cnt = len([labname for labname in weeklylabsdict[i] if labname in ref.keys()])
        cntweek = f"{cnt} / {len(weeklylabsdict[i])}"
        final[i] = cntweek


    return pd.DataFrame.from_dict(final, orient='index', columns=['progress'])

def weekly_table(ref, num):
    names = [labname for labname in weeklylabsdict[num]]
    status = [ref[labname].split('T')[0] if labname in ref.keys() else 'Not Delivered' for labname in weeklylabsdict[num]]

    return pd.DataFrame(list(zip(names, status)), columns=[f'Labs {num.title()}', 'Date Submitted'])