import pandas as pd
import requests
import time
import random

df = pd.read_json('jc.json')

base_url = r'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/'


# fetches the pdf file
for url in df['documentLink']:
    r = requests.get(base_url + url, allow_redirects=True)
    # replacing / with - in the filename of the pdf
    file = open(url.replace('/  ', '-') , 'wb')
    file.write(r.content)
    # puts the thread randomly to sleep from 0.1 to 1.9 seconds
    random_number = random.randint(0,10) /10 + random.randint(0,1)
    time.sleep(random_number)    
    file.close()

