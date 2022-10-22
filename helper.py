import requests
import pandas as pd


class Labs:
    week1 = ['lab-list-comprehensions', 'lab-tuple-set-dict', 'lab-string-operations', 'lab-numpy', 'lab-intro-pandas']
    week2 = ['lab-mysql-first-queries', 'lab-mysql-select', 'lab-mysql', 'lab-dataframe-calculations', 'lab-advanced-pandas', 'lab-import-export', 'lab-data-cleaning', 'lab-lambda-functions']
    week3 = ['lab-api-scavenger', 'lab-web-scraping', 'lab-pandas-deep-dive', 'lab-advanced-regex', 'lab-matplotlib-seaborn']
    week4 = ['lab-intro-bi-tableau', 'lab-bi-analysis-tableau', 'lab-pivot-table-and-correlation', 'Descriptive-Stats', 'lab-regression-analysis', 'lab-subsetting-and-descriptive-stats']
    week5 = ['lab-intro-prob', 'lab-probability-distributions', 'M2-mini-project2', 'lab-confidence-intervals', 'lab-hypothesis-testing-1', 'lab-hypothesis-testing-2', 'lab-intro-to-scipy', 'lab-two-sample-hyp-test', 'lab-goodfit-indeptests']
    week7 = ['lab-intro-to-ml', 'lab-supervised-learning-feature-extraction', 'lab-supervised-learning', 'lab-supervised-learning-sklearn', 'lab-imbalance', 'lab-problems-in-ml']
    week8 = ['lab-unsupervised-learning', 'lab-unsupervised-learning-and-sklearn', 'lab-deep-learning', 'lab-nlp']

    def __init__(self, name) -> None:
        self.name = name.lower()

    def refresh(self, num):
        user_ref = db.collection("labs").document(self.name)
        weeklylabs = {1: self.week1, 2: self.week2, 3: self.week3, 4: self.week4, 5: self.week5, 7: self.week7, 8: self.week8}
        
        for lab_name in weeklylabs[num]:
            print(lab_name)
            response = requests.get('https://api.github.com/repos/ta-data-lis/' + lab_name + '/pulls')
            data = pd.DataFrame(response.json())
            if 'title' in data:
                pr = data['title']

                pr_cohort_name = [a.split(']')[0].strip('[').strip() for a in pr if len(a.split(']')) > 1]
                pr_name = [a.split(']')[1].strip() for a in pr if len(a.split(']')) > 1]

                for pr in pr_name:
                    if pr.lower().find(self.name) != -1:
                        clean_labname = lab_name.replace('-', '')
                        user_ref.update({clean_labname : 'Delivered'})