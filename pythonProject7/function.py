from datetime import date
import datetime as dt
from datetime import datetime

import pandas as pd
df=pd.read_csv('data2.csv',index_col=0)
df['dates']= pd.to_datetime(df['dates'])
df.to_csv('data2.csv')


def retrieve_cla(dataset,title):

    today = datetime.today().date()
    dataset=pd.read_csv(dataset,index_col=0)
    dataset['dates']=pd.to_datetime(dataset['dates'],utc=False)
    dataset['dates'] = dataset['dates'].dt.date

    dataset_match= dataset[dataset['title'] == title]
    update = dataset_match[dataset_match['dates'] == today]


    if len(update) >0:
       return 'Updates were made at', today.day, today.strftime("%B"), 'stating', str(update.text.values), 'click here to download PDF',update.link
    elif len(dataset_match) ==0:

       return 'No Such Label'
    else:
       return 'No Updates'





# def download_pdf():

    #
    # update.set_index('title')

    # if update:
    #     print('0')





#retrieve_cla('data2.csv','Conjuction')
# print(df.dtypes)
# title='A New World'
# print(df[df['title'] == title])






