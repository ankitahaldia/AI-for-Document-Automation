import pandas as pd
import requests
import time
import random
import sqlite3   
column_list=["jcId","jcFr","jcNl","titleFr","titleNl","themesFr","themesNl","signatureDate","validityDate","depositDate","recordDate","depositRegistrationDate","depositNumber","enforced","royalDecreeDate","noticeDepositMBDate","publicationRoyalDecreeDate","correctedDate","documentLink","documentSize","scopeFr","scopeNl","noScopeFr","noScopeNl"]
column_CLA=["jcId","titleFr","titleNl","signatureDate","validityDate","depositDate","recordDate","depositRegistrationDate","id","enforced","royalDecreeDate","noticeDepositMBDate","publicationRoyalDecreeDate","correctedDate","documentLink","documentSize"]
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
try: # is there any table in the database?
    cursor.execute("""select * from CLA""")
    df_CLA = pd.DataFrame(cursor.fetchall(),columns=column_CLA)    
    if len(df_CLA["jcId"])<1:
        raise ValueError('A very specific bad thing happened.')
except:#if not then create a new one
    df_CLA=pd.DataFrame(columns=column_CLA)
    conn.close()
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    print("--- there was no record yet but we created new one ---")
    # for x in column_CLA:
    #     df_CLA[x] = [""]     
    # df_CLA.drop(df_CLA.index[[0]])     
    # df_CLA = df_CLA.append(column_CLA)#df_CLA.append(column_CLA.remove("jcId"))
    # del df_CLA[0]
    df_CLA.to_sql(name='CLA', con=conn,if_exists='replace', index=False)
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("""select * from CLA""")
    df_CLA = pd.DataFrame(cursor.fetchall(),columns = column_CLA)
# print("started-------------------------------")
api = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"
start_date = "2018-01-01T00:00:00.000Z" # we can use an UI to get start_date
end_date = "2021-12-31T00:00:00.000Z"   # we can use an UI to get end_date
null = None
true = True
false =False
dates={"lang":"fr","signatureDate":{"start":start_date, "end":end_date}}
# r = requests.post(api, json = dates)
# text ="".join(map(chr, r.content)) 
# print("finished-------------------------------")

# f = open("demofile3.txt", "r") ##########
f = open("full.txt", "r") ##########
text = f.read()############

list=eval(text)

# f = open("full.txt", "w")#############
# f.write(str(list))###############
# f.close()###############

one_record = False
# print("-----------------------------------------",list)
for x in list:    
    new_line={}
    for c in column_list:
        new_line[c] = str(x[c])
    its_in = False
    for a in df_CLA['id']:        
        if a == new_line['depositNumber']:
            # print("it is an old record a=",a)
            its_in = True            
    if not its_in:
        one_record =True
        # print("+++++ this file is new +++++")
        new_CLA = new_line.copy()
        del new_CLA["jcFr"]
        del new_CLA["jcNl"]
        # del new_CLA["titleFr"]
        # del new_CLA["titleNl"]
        del new_CLA["themesFr"]
        del new_CLA["themesNl"]
        new_CLA["id"] =new_CLA["depositNumber"]
        del new_CLA["depositNumber"]
        del new_CLA["scopeFr"]
        del new_CLA["scopeNl"]
        del new_CLA["noScopeFr"]
        del new_CLA["noScopeNl"]        
        # 1- check for 4 tables is there a new record then add them(commission , scope , noscope, theme)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from commission""")        
        df_commission = pd.DataFrame(cursor.fetchall(),columns=["id","fr","nl"]) 
        its_in2 = False
        for k in df_commission['id']:        
            if k == new_line['jcId']: # print("it is an old record a=",a)
                its_in2 = True
        if not its_in2:            # 
            # print("+++++ this commission is new +++++")
            new_commission = {"id":new_line["jcId"],"fr":new_line['jcFr'],"nl":new_line['jcNl']}
            # print(len(df_commission["id"]),"")
            df_commission.loc[len(df_commission["id"])+1] = new_commission            
            # print(len(df_commission["id"]),"")        
        conn.commit()
        df_commission.to_sql(name = 'commission', con = conn, if_exists = 'replace', index = False)
        conn.commit()

        # 2- check for 4 tables is there a new record then add them(commission , scope , noscope, theme)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from Scope""")        
        df_Scope = pd.DataFrame(cursor.fetchall(),columns=["id","fr","nl"]) 
        its_in2 = False
        if new_line["scopeFr"] != "None":
            index=0
            for scope in eval(new_line["scopeFr"]):
                scope = scope.replace('"',"`")
                scope = scope.replace("'","`")
                for k in df_Scope['fr']:        
                    if k == scope: # print("it is an old record a=",a)
                        its_in2 = True
                if not its_in2:             #
                    # print("+++++ this scope is new +++++")
                    if len(df_Scope["id"])==0:
                        new_Scope = {"id":len(df_Scope["id"]),"fr":scope,"nl":eval(new_line['scopeNl'])[index].replace('"',"`").replace("'","`")}                        
                    else:
                        new_Scope = {"id":max(df_Scope["id"])+1,"fr":scope,"nl":eval(new_line['scopeNl'])[index].replace('"',"`").replace("'","`")}                    
                    df_Scope.loc[len(df_Scope["id"])+1] = new_Scope
                index+=1
        conn.commit()
        df_Scope.to_sql(name = 'Scope', con = conn, if_exists = 'replace', index = False)
        conn.commit()   
        
        # 3- check for 4 tables is there a new record then add them(commission , scope , noscope, theme)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from No_scope""")        
        df_No_scope = pd.DataFrame(cursor.fetchall(),columns=["id","fr","nl"]) 
        its_in2 = False
        if new_line["noScopeFr"] != "None":
            index=0
            for scope in eval(new_line["noScopeFr"]):
                scope = scope.replace('"',"`")
                scope = scope.replace("'","`")
                # print("----------------",scope,"----------------")
                for k in df_No_scope['fr']:        
                    if k == scope: # print("it is an old record a=",a)
                        its_in2 = True
                if not its_in2:             #                    
                    # print("+++++ this noScope is new +++++",len(df_No_scope["id"]))
                    if len(df_No_scope["id"])==0:
                        new_No_scope = {"id":len(df_No_scope["id"]),"fr":scope,"nl":eval(new_line['noScopeNl'])[index].replace('"',"`").replace("'","`")}                    
                    else:
                        new_No_scope = {"id":max(df_No_scope["id"])+1,"fr":scope,"nl":eval(new_line['noScopeNl'])[index].replace('"',"`").replace("'","`")}                    
                    df_No_scope.loc[len(df_No_scope["id"])+1] = new_No_scope
                    # print("+++++ +++++",len(df_No_scope["id"]))
                index+=1
        conn.commit()
        df_No_scope.to_sql(name = 'No_scope', con = conn, if_exists = 'replace', index = False)
        conn.commit()    

        # 4- check for 4 tables is there a new record then add them(commission , scope , noscope, theme)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from Theme""")        
        df_Theme = pd.DataFrame(cursor.fetchall(),columns=["id","fr","nl"]) 
        its_in2 = False
        if new_line["themesFr"] != "None":
            index=0
            for theme in eval(new_line["themesFr"]):
                theme = theme.replace('"',"`")
                theme = theme.replace("'","`")                        
                for k in df_Theme['fr']:        
                    if k == theme: # print("it is an old record a=",a)
                        its_in2 = True
                if not its_in2:             #
                    # print("+++++ this theme is new +++++")
                    if len(df_Theme["id"])==0:
                        new_Theme = {"id":len(df_Theme["id"]),"fr":theme,"nl":eval(new_line['themesNl'])[index].replace('"',"`").replace("'","`")}                    
                    else:
                        new_Theme = {"id":max(df_Theme["id"])+1,"fr":theme,"nl":eval(new_line['themesNl'])[index].replace('"',"`").replace("'","`")}                    
                    df_Theme.loc[len(df_Theme["id"])+1] = new_Theme
                index+=1
        conn.commit()    
        df_Theme.to_sql(name = 'Theme', con = conn, if_exists = 'replace', index = False)        
        conn.commit()        
        
        # 5- add records to tables (Theme_CLA , Scope_CLA , No_scope_CLA)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from Theme_CLA""")        
        df_Theme_CLA = pd.DataFrame(cursor.fetchall(),columns=["id","CLA_id","theme_id"]) 
        cursor2 = conn.cursor()
        if new_line["themesFr"] != "None":
            for theme in eval(new_line["themesFr"]):
                theme = theme.replace('"',"`")        
                theme = theme.replace("'","`")                        
                cursor2.execute(f'select id from Theme where fr="{theme}"')                             
                df_id = pd.DataFrame(cursor2.fetchall(),columns=["id"]) 
                if len(df_id["id"])==0:
                    if len(df_Theme_CLA["id"])==0:
                        new_Theme_CLA = {"id":len(df_Theme_CLA["id"]),"CLA_id":new_CLA["id"],"theme_id":0}
                    else:
                        new_Theme_CLA = {"id":max(df_Theme_CLA["id"])+1,"CLA_id":new_CLA["id"],"theme_id":0}
                    if len(df_Theme_CLA[(df_Theme_CLA["CLA_id"]==new_CLA["id"])&(df_Theme_CLA["theme_id"]==0)])==0:
                        df_Theme_CLA.loc[len(df_Theme_CLA["id"])+1] = new_Theme_CLA
                else:                    
                    if len(df_Theme_CLA["id"])==0:                    
                        new_Theme_CLA = {"id":len(df_Theme_CLA["id"]),"CLA_id":new_CLA["id"],"theme_id":df_id["id"][0]}
                    else:
                        new_Theme_CLA = {"id":max(df_Theme_CLA["id"])+1,"CLA_id":new_CLA["id"],"theme_id":df_id["id"][0]}
                    if len(df_Theme_CLA[(df_Theme_CLA["CLA_id"]==new_CLA["id"])&(df_Theme_CLA["theme_id"]==df_id["id"][0])])==0:
                        df_Theme_CLA.loc[len(df_Theme_CLA["id"])+1] = new_Theme_CLA
        conn.commit()        
        df_Theme_CLA.to_sql(name = 'Theme_CLA', con = conn, if_exists = 'replace', index = False)
        conn.commit()
        
        # 6- add records to tables (Theme_CLA , Scope_CLA , No_scope_CLA)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from Scope_CLA""")        
        df_Scope_CLA = pd.DataFrame(cursor.fetchall(),columns=["id","CLA_id","scope_id"]) 

        cursor2 = conn.cursor()
        if new_line["scopeFr"] != "None":
            for theme in eval(new_line["scopeFr"]):                
                theme = theme.replace('"',"`") 
                theme = theme.replace("'","`")                               
                cursor2.execute(f'select id from Scope where fr="{theme}"')        
                df_id = pd.DataFrame(cursor2.fetchall(),columns=["id"]) 
                # if len(df_CLA["id"])>200 == 0:
                    # print(abc,end=" - ")
                if len(df_id["id"])==0:
                    if len(df_Scope_CLA["id"])==0:
                        new_Scope_CLA = {"id":len(df_Scope_CLA["id"]),"CLA_id":new_CLA["id"],"scope_id":0}
                    else:
                        new_Scope_CLA = {"id":max(df_Scope_CLA["id"])+1,"CLA_id":new_CLA["id"],"scope_id":0}
                    if len(df_Scope_CLA[(df_Scope_CLA["CLA_id"]==new_CLA["id"])&(df_Scope_CLA["scope_id"]==0)])==0:
                        df_Scope_CLA.loc[len(df_Scope_CLA["id"])+1] = new_Scope_CLA
                else:
                    if len(df_Scope_CLA["id"])==0:                    
                        new_Scope_CLA = {"id":len(df_Scope_CLA["id"]),"CLA_id":new_CLA["id"],"scope_id":df_id["id"][0]}
                    else:
                        new_Scope_CLA = {"id":max(df_Scope_CLA["id"])+1,"CLA_id":new_CLA["id"],"scope_id":df_id["id"][0]}
                    if len(df_Scope_CLA[(df_Scope_CLA["CLA_id"]==new_CLA["id"])&(df_Scope_CLA["scope_id"]==df_id["id"][0])])==0:
                        df_Scope_CLA.loc[len(df_Scope_CLA["id"])+1] = new_Scope_CLA
        conn.commit()
        df_Scope_CLA.to_sql(name = 'Scope_CLA', con = conn, if_exists = 'replace', index = False)
        conn.commit()    

        # 7- add records to tables (Theme_CLA , Scope_CLA , No_scope_CLA)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from No_scope_CLA""")        
        df_No_scope_CLA = pd.DataFrame(cursor.fetchall(),columns=["id","CLA_id","no_scope_id"])         
        cursor2 = conn.cursor()
        if new_line["noScopeFr"] != "None":
            for theme in eval(new_line["noScopeFr"]):
                theme = theme.replace('"',"`")
                theme = theme.replace("'","`")                                
                cursor2.execute(f'select id from No_scope where fr="{theme}"')                        
                df_id = pd.DataFrame(cursor2.fetchall(),columns=["id"]) 
                # are these CLA_id and no_scope_id set in the database?
                
                # print("buraya geliyor ama",len(df_No_scope_CLA["id"]),len(df_id["id"]),len(df_No_scope_CLA[(df_No_scope_CLA["CLA_id"]==new_CLA["id"])&(df_No_scope_CLA["no_scope_id"]==df_id["id"][0])]))
                if len(df_id["id"])==0:
                    if len(df_No_scope_CLA["id"])==0:
                        new_No_cope_CLA = {"id":len(df_No_scope_CLA["id"]),"CLA_id":new_CLA["id"],"no_scope_id":0}
                    else:
                        new_No_cope_CLA = {"id":max(df_No_scope_CLA["id"])+1,"CLA_id":new_CLA["id"],"no_scope_id":0}
                    if len(df_No_scope_CLA[(df_No_scope_CLA["CLA_id"]==new_CLA["id"])&(df_No_scope_CLA["no_scope_id"]==0)])==0:
                        df_No_scope_CLA.loc[len(df_No_scope_CLA["id"])+1] = new_No_cope_CLA
                else:                                        
                    if len(df_No_scope_CLA["id"])==0:
                        new_No_cope_CLA = {"id":len(df_No_scope_CLA["id"]),"CLA_id":new_CLA["id"],"no_scope_id":df_id["id"][0]}
                    else:
                        new_No_cope_CLA = {"id":max(df_No_scope_CLA["id"])+1,"CLA_id":new_CLA["id"],"no_scope_id":df_id["id"][0]}
                    if len(df_No_scope_CLA[(df_No_scope_CLA["CLA_id"]==new_CLA["id"])&(df_No_scope_CLA["no_scope_id"]==df_id["id"][0])])==0:
                        df_No_scope_CLA.loc[len(df_No_scope_CLA["id"])+1] = new_No_cope_CLA
        conn.commit()
        df_No_scope_CLA.to_sql(name = 'No_scope_CLA', con = conn, if_exists = 'replace', index = False)
        conn.commit()
        abc = len(df_CLA["id"])                 
        df_CLA.loc[abc] = new_CLA
        if abc%100 ==0:
            print(abc,end=" - ")
        # ***** following codes are downloading PDF files in the end we will open them *****
        # base_url = r'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/'
        # url = x['documentLink']
        # print("downloading the pdf file = ",url)
        # r = requests.get(base_url + url, allow_redirects=True)
        # file = open("./assets/pdfs/"+url.replace('/', '-') , 'wb')
        # file.write(r.content)    # puts the thread randomly to sleep from 0.1 to 1.9 seconds
        # random_number = random.randint(0,10) /10 + random.randint(0,1)
        # time.sleep(random_number)    
        # file.close()
print(df_CLA.describe())
if one_record:    
    df_CLA.to_sql(name = 'CLA', con = conn, if_exists = 'replace', index = False)    
    conn.commit()
conn.close()
