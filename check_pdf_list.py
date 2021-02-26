import pandas as pd
import requests
import time
import random
import sqlite3   
column_list=["jcId","jcFr","titleFr","titleNl","themesFr","themesNl","signatureDate","validityDate","depositDate","recordDate","depositRegistrationDate","depositNumber","enforced","royalDecreeDate","noticeDepositMBDate","publicationRoyalDecreeDate","correctedDate","documentLink","documentSize","scopeFr","scopeNl","noScopeFr","noScopeNl"]
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
try: # is there any table in the database?
    cursor.execute("""select * from our""")
    df = pd.DataFrame(cursor.fetchall(),columns=column_list)
except:#if not then create a new one
    df=pd.DataFrame()
    conn.close()
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    print("--- there was no record yet but we created new one ---")
    for x in column_list:
        df[x] = [""]        
    df = df.append(column_list.remove("jcId"))
    df.to_sql(name='our', con=conn,if_exists='replace', index=False)
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("""select * from our""")
    df = pd.DataFrame(cursor.fetchall(),columns = column_list)

api = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"
start_date = "2020-12-18T00:00:00.000Z" # we can use an UI to get start_date
end_date = "2021-12-31T00:00:00.000Z"   # we can use an UI to get end_date
null = None
true = True
false = False
dates={"lang":"fr","signatureDate":{"start":start_date, "end":end_date}}
r = requests.post(api, json = dates)
text ="".join(map(chr, r.content)) 
list = eval(text)
for x in list:    
    new_line={}
    for c in column_list:
        new_line[c] = str(x[c])
    its_in = False
    for a in df['depositNumber']:        
        if a == new_line['depositNumber']:
            print("it is an old record a=",a)
            its_in = True
    if not its_in:
        print("+++++ this file is new +++++")
        df.loc[len(df["jcId"])] = new_line            
        base_url = r'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/'
        url = x['documentLink']
        print("downloading the pdf file = ",url)
        r = requests.get(base_url + url, allow_redirects=True)
        file = open("./src/app/pdfs/"+url.replace('/', '-') , 'wb')
        file.write(r.content)    # puts the thread randomly to sleep from 0.1 to 1.9 seconds
        random_number = random.randint(0,10) /10 + random.randint(0,1)
        time.sleep(random_number)    
        file.close()
print(df)
conn.commit()
df.to_sql(name = 'our', con = conn, if_exists = 'replace', index = False)
conn.close()