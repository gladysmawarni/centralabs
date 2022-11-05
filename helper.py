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
    githubtoken = st.secrets["github_token"]

    def __init__(self, username) -> None:
        self.username = username
    
    def __getDB(self, collection):
        return db.collection(collection).document(self.username)
    
    def __getPR(self, state):
        url = 'https://api.github.com/search/issues'
        params= {'q': f'state:{state} author:{self.username} type:pr', 'per_page': 100}

        response = requests.get(url=url, params= params, auth= HTTPBasicAuth(self.githubusername, self.githubtoken))
        return response.json()['items']

    
    def __updateLabsStatus(self, lablist):
        user_lab_ref = self.__getDB('labs')
        user_time_ref =self.__getDB('time')

        for labname, time in lablist:
            user_lab_ref.update({labname : 'Delivered'})
            user_time_ref.set({labname : time}, merge=True)
            print(self.username + ' : ' + labname)


    def refresh(self):
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


    def __updateLabsComments(self,closedprlist):
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

    
    def getComments(self):
        closedpr = self.__getPR('closed')
        closedprlist = [pr['timeline_url'] for pr in closedpr]
        self.__updateLabsComments(closedprlist)
    

    def doubleCheck(self):
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



if __name__ == '__main__':
    # all the users who registered
    users = db.collection('registered')
    # list of registered username
    usernames = [user.to_dict()['username'] for user in users.stream()]

    for user in usernames:
        user = Labs(user)
        #user.refresh()
        user.doubleCheck()
        # user.getComments()