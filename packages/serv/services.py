from datetime import datetime
from sqlalchemy import sql

import pandas as pd
import requests
import re

from packages import repository as repo


def get_cla_json():
    '''
    DOCSTRING:
    ---------
    Returns a dataframe containing metadata from all CLA's between 2018-01-18 and 2050-01-18
    '''

    base_url = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"
    body = {"lang":"fr","signatureDate":{"start":"2018-01-18T00:00:00.000Z", "end":"2050-01-18T00:00:00.000Z"}}
    response = requests.post(base_url, json= body)
    return pd.read_json(response.content, encoding = 'utf8')

def to_date(date_string):
    '''
    DOCSTRING:
    ---------
    Transforms a string (eg: 2018-01-18T00:00:00.000Z) into a datetime object, if not will return an sql NULL value
    '''

    if (date_string != "None") and not (pd.isnull(date_string)) and (type(date_string) is not datetime.timestamp) :
        return datetime.fromisoformat(date_string[:-5]).date()
    else:
        return sql.null()

def get_cla_id_from_text(text_list):
  """ get a list as a parameter and the function will iterate in the list to find the CLA_id and the sentence with the CLA_id. You can access the CLA_id at pair index and the sentence at impair indexes"""  
  pattern = r"\d{6}/\D\d/\d+"
  new = []

  for text in text_list:

    x = re.search(pattern, text)
    if x != None:
      new.append(x.group())
      new.append(x.string)
  
  return new

def update_database():
    df = get_cla_json()

    repo.insert_joint_commission(df)
    repo.insert_themes(df)
    repo.insert_CLA(df)
    repo.insert_no_scope(df)
    repo.insert_scope(df)