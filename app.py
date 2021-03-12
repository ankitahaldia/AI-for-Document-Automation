from sqlalchemy.sql.selectable import Join
import streamlit as st
from datetime import datetime
import numpy as np
import cv2
import pytesseract as pt
import re
import datetime
from textblob import TextBlob
import pandas as pd
from bokeh.models.widgets import Div
import webbrowser
import base64
import os 
import requests

from packages.repository import get_all_themes, get_all_jc, get_cla_full_search, check_for_new_cla
from packages.serv.services import get_cla_json




st.set_page_config(layout="wide")

#serv.update_database()
download_link ='https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/'

cwd = os.getcwd()

container = st.beta_container()

def download_pdf(url):
    r = requests.get(download_link + url, allow_redirects=True)
    file = open(url.replace('/', '-') , 'wb')
    file.write(r.content)
    file.close()


def display_pdf(pdf_file):
    
    with open(f'{pdf_file}',"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1050" height="1500" type="application/pdf">'
    container.markdown(pdf_display, unsafe_allow_html=True)


def display_mock(highlight):

    container.title('régime de chômage avec complément d\'entreprise à 59 ans')
    container.header(f'Deposit number: 152853')
    container.subheader(f'200: COMMISSION PARITAIRE POUR LES EMPLOYES DE L\'INDUSTRIE ALIMENTAIRE ')

    if highlight:
        container.subheader('Chapter 1 : Champ d\'application')
    
    
    st.sidebar.markdown(f'[Download link]({download_link}10203/10203-2020-001652.pdf)')
    
    st.sidebar.subheader('Chapters')
    for i in range(1,7):
        st.sidebar.button(f'Chapter {i}')
    

    if highlight:
        display_pdf('200_chapitre_surligne.pdf')
    else:
        display_pdf('200-200-2019-010018.pdf')
        
    



def display_cla(cla):
    

    download_pdf(cla.document_link)

    container.title(cla.title_fr)
    container.header(f'Deposit number: {cla.id}')
    if cla.joint_commission:
        container.subheader(f'{cla.joint_commission_id}: {cla.joint_commission.name_fr}')
    container.subheader(' ')
    
    display_pdf(cla.document_link.replace('/', '-'))
       
    st.sidebar.markdown(f'[Download link]({download_link}{cla.document_link})')
    if cla.corrected_date:
        st.sidebar.header(f'Errated on {cla.corrected_date}')
    st.sidebar.write(f'Annexe on page {cla.anenexe_page}')
    st.sidebar.write(f'Signature date: {cla.signature_date}')
    st.sidebar.write(f'Validity date: {cla.validity_date}')
    st.sidebar.write(f'Deposit date: {cla.deposit_date}')
    st.sidebar.write(f'Record date: {cla.record_date}')
    st.sidebar.write(f'Deposit registration date: {cla.deposit_registration_date}')
    st.sidebar.write(f'Royal decree date: {cla.royal_decree_date}')
    st.sidebar. write(f'Publ. royal decree date: {cla.publication_royal_decree_date}')  

    if cla.themes:
        st.sidebar.subheader('Themes')
        for theme in cla.themes:
            st.sidebar.button(theme.name_fr)        
        
    st.sidebar.subheader('Scopes')
    for scope in cla.scopes:
        st.sidebar.button(scope.name_fr)

    st.sidebar.subheader('No Scopes')
    for no_scope in cla.no_scopes:
        st.sidebar.button(no_scope.name_fr)


st.image('banner.png')

selected_jc = st.selectbox('Select a joint commission', get_all_jc() ,format_func=lambda x : f'{x.id} {x.name_fr}')

# SEARCH COLUMNS
col1, col2 = st.beta_columns((5,2))

# COLUMN 1
with col1:
    # THEME SELECTOR  
    selected_theme = st.selectbox('Select a theme', get_all_themes(), format_func=lambda x :x.name_fr)

    has_erratum = col1.checkbox('Look for an erratum', value=False)


# COLUMN 2
with col2:
    # BEGIN SIGNATURE DATE SELECTOR
    start_signature_date = st.date_input(
        "Select a starting signature date",
        datetime.date(2012, 1, 1))
    
    # END SIGNATURE DATE SELECTOR
    end_signature_date = st.date_input(
        "Select an ending signature date",
        datetime.date(2032, 1, 1))


# SEARCH BUTTON
click_search = st.button('SEARCH')

# NEW CLAS BUTTON
click_new_cla = st.button('SEARCH FOR NEW CLAS')

click_mock = st.button('BETA')
click_mock2 = st.button('BETA HIGHLIGHT CHAPTER 1')

if click_search:
    clas = get_cla_full_search(selected_theme.name_fr, selected_jc.id, has_erratum, start_signature_date, end_signature_date )

        
    if clas:
        selected_cla = container.selectbox('Select a CLA',clas, format_func=lambda x : f'{x.validity_date} : {x.title_fr}')
        display_cla(selected_cla)

    
if click_new_cla:
    cla1, cla2 = check_for_new_cla(get_cla_json())

    if cla2:
        selected_cla = container.selectbox('Select a CLA',cla2, format_func=lambda x : f'{x.validity_date} : {x.title_fr}')
        display_cla(selected_cla)
    
if click_mock:
    display_mock(False)

if click_mock2:
    display_mock(True)
    


    


         
       
    
    
 


# if selected_theme is not None:
#     cla_candidates = get_cla_by_theme(selected_theme)
#     selected_cla = st.selectbox('Select a CLA',cla_candidates, format_func=lambda x : f'{x.joint_commission_id} {x.joint_commission.name_fr} {x.validity_date} : {x.title_fr}'  )
    
#     if selected_cla is not None:
#         st.markdown(str(selected_cla))
    
    # st.write("")
    # st.write("-------------------------------------")
    # st.write("Finding if there are any updates...")
    # st.write("-------------------------------------")
    # label=retrieve_cla('data2.csv',selected_theme)
    # st.write(label)



# def retrieve_cla(dataset,title):

#     today = datetime.today().date()
#     dataset=pd.read_csv(dataset,index_col=0)
#     dataset['dates']=pd.to_datetime(dataset['dates'],utc=False)
#     dataset['dates'] = dataset['dates'].dt.date

#     dataset_match= dataset[dataset['title'] == title]
#     update = dataset_match[dataset_match['dates'] == today]

#     if len(update) >0:
#         st.write('Updates were made at')
#         st.write(today.day,today.strftime("%B"))
#         st.write('stating')
#         st.write(str(update.text.values))
#         link= update['link'].values

#         if st.button('GET PDF'):
#             st.markdown(link, unsafe_allow_html=True)
#             browser = webbrowser.get('safari')
#             browser.open_new_tab(link)

#         # if st.button('Open PDF'):
#         #     webbrowser.open_new_tab(link)

#        # return 'Updates were made at', today.day, today.strftime("%B"), 'stating', str(update.text.values), 'click here to download PDF',update.link
#     elif len(dataset_match) ==0:

#        return 'No Such Label'
#     else:
#        return 'No Updates'

# def extract(img):
#     slide=st.sidebar.slider("Select Page Segmentation Mode",1,14)
#     conf=f"-l eng --oem 3 --psm {slide}"
#     text=pt.image_to_string(img, config = conf)
#     if(text!=""):
#         st.markdown("<h1 style='color:yellow;'>Extracted Text</h1>", unsafe_allow_html=True)
#         slot1=st.empty()
#         slot2=st.empty()
#         if(st.sidebar.checkbox("Apply Spelling Correction")):
#             corrected=TextBlob(text).correct()
#             slot1.markdown(f"{corrected}", unsafe_allow_html=True)
#             polar=round(corrected.sentiment.polarity,2)
#             slot2.markdown(f"""<h1 style='color:yellow;'>Polarity: <span style='color:white;'>{polar}</span> Sentiment: <span style='color:white;'>{sentiments(polar)}</span></h1>""", unsafe_allow_html=True)
#         if(st.sidebar.checkbox("Remove Numbers & Special Characters")):
#             filtered=re.sub(r'[^A-Za-z ]+', '', text)
#             slot1.markdown(f"{filtered}", unsafe_allow_html=True)
#             polar=round(TextBlob(filtered).sentiment.polarity,2)
#             slot2.markdown(f"""<h1 style='color:yellow;'>Polarity: <span style='color:white;'>{polar}</span> Sentiment: <span style='color:white;'>{sentiments(polar)}</span></h1>""", unsafe_allow_html=True)
#         else:
#             slot1.markdown(f"{text}", unsafe_allow_html=True)
#             polar=round(TextBlob(text).sentiment.polarity,2)
#             slot2.markdown(f"""<h1 style='color:yellow;'>Polarity: <span style='color:white;'>{polar}</span> Sentiment: <span style='color:white;'>{sentiments(polar)}</span></h1>""", unsafe_allow_html=True)

# st.sidebar.markdown("<h1 style='text-align: center;color: #2C3454;margin-top:30px;margin-bottom:-20px;'>Select Image</h1>", unsafe_allow_html=True)

# image_file = st.sidebar.file_uploader("", type=["jpg","png","jpeg"])
# if image_file is not None:
#     st.markdown("<h1 style='color:yellow;'>Uploaded Image</h1>", unsafe_allow_html=True)
#     st.image(image_file,width=400)
#     file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
#     radio=st.sidebar.radio("Select Action",('Text Extraction','Thresholding'))
#     img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#     if(radio=="Text Extraction"):
#         extract(img)
