import src.sub_services as ssv
from pdf2image import convert_from_path 
from langdetect import detect
import pandas as pd
import requests
import time
import random
import sqlite3 


def extract_text(path,name) :

    ''' 
    Extracts text from pdf and 
    returns a list of all the strings which are in french
    '''
    PDF_file = path+name
    # Store all the pages of the PDF in a variable 
    pages = convert_from_path(r'C:/Users/opaps/source/BeCode/KPMG-JC/New folder/AI-for-Document-Automation/100.pdf', 500) 
  
    # Counter to store images of each page of PDF to image 
    image_counter = 1
    
    # Iterate through all the pages stored above 
    for page in pages: 
        
        ssv.page2img(page,image_counter,name)
        # Increment the counter to update filename 
        image_counter += 1

    fr_list = ssv.opencv_to_text(image_counter,name)

    return fr_list

def is_french(stringx) :
    try :
        if detect(stringx.lower()) == 'fr' :
            return True
    except :
        return False

def update_database(start_date, end_date):
    column_list=["jcId","jcFr","titleFr","titleNl","themesFr","themesNl",
    "signatureDate","validityDate","depositDate","recordDate","depositRegistrationDate",
    "depositNumber","enforced","royalDecreeDate","noticeDepositMBDate","publicationRoyalDecreeDate",
    "correctedDate","documentLink","documentSize","scopeFr","scopeNl","noScopeFr","noScopeNl"]
    conn = sqlite3.connect("KPMG_CLA_Project.db")
    cursor = conn.cursor()
    try: # is there any table in the database?
        cursor.execute("""select * from CLAs""")
        df = pd.DataFrame(cursor.fetchall(),columns=column_list)    
    except:#if not then create a new one
        df=pd.DataFrame()
        conn.close()
        conn = sqlite3.connect("KPMG_CLA_Project.db")
        cursor = conn.cursor()
        print("--- No table detected, creation of CLAs table ---")
        for x in column_list:
            df[x] = [""]        
        df = df.append(column_list.remove("jcId"))
        df.to_sql(name='CLAs', con=conn,if_exists='replace', index=False)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("""select * from CLAs""")
        df = pd.DataFrame(cursor.fetchall(),columns = column_list)

    api_base_url = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"
    #TODO : change
    #start_date = "2021-01-18T00:00:00.000Z" # we can use an UI to get start_date
    #end_date = "2021-12-31T00:00:00.000Z"   # we can use an UI to get end_date
    null = None
    true = True
    false =False
    dates={"lang":"fr","signatureDate":{"start":start_date, "end":end_date}}
    r = requests.post(api_base_url, json = dates)
    text ="".join(map(chr, r.content)) 
    list=eval(text)
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
            file = open("./assets/pdfs/"+url.replace('/', '-') , 'wb')
            file.write(r.content)    # puts the thread randomly to sleep from 0.1 to 1.9 seconds
            random_number = random.randint(0,10) /10 + random.randint(0,1)
            time.sleep(random_number)    
            file.close()
    print(df)
    conn.commit()
    df.to_sql(name = 'CLAs', con = conn, if_exists = 'replace', index = False)

def segmantize(text, identifiers):
  
  i = 0
  list_of_index = []
  for line in text:
    i += 1
    first_word = line.split(' ')[0]
    if first_word[0] == '§':
        first_word == '§'
    
    last_word = ' '
    if len(line.split(' ')) > 1:
      last_word = line.split(' ')[-2]
    print(f"{first_word} and {last_word}")
    if (first_word.lower() in [x.lower() for x in identifiers]) or (last_word.lower() in [x.lower() for x in identifiers]):

      list_of_index.append(i-1)

  print(list_of_index)
  articles = []
  for x in range(len(list_of_index)-1):
    new_list = []
    for y in range(list_of_index[x],list_of_index[x+1]):
    
      new_list.append(text[y])
    
    articles.append(new_list)  
  end_list = []
  if len(list_of_index) > 0:
    for z in range(list_of_index[-1], len(text)):
      end_list.append(text[z])
  
    articles.append(end_list)


  
  return articles