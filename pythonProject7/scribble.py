import pandas as pd
from datetime import date
import datetime

data = {'title': ['UK Immigration','Politics', 'Healthcare', 'Bears'], 'date': ['07/15/2019', '10/10/2010', '03/09/2021', '03/11/2021'],'text':['here is news there','why do we need news','is it good news','is it a bad bear that it walks on its back legs'],'link':['https://www.annualreviews.org/doi/pdf/10.1146/annurev-neuro-060909-153151','https://www.jneurosci.org/content/jneuro/30/46/15616.full.pdf','https://www.jneurosci.org/content/jneuro/23/13/5583.full.pdf','https://www.jneurosci.org/content/21/24/9801.short']}

df= pd.DataFrame(data,columns=['title','date','text','link'])

df['dates']=pd.to_datetime(df['date'])
df=df.drop('date',axis=1)
print(df.head())
print(df.dates.dtype)

df.to_csv('data2.csv')