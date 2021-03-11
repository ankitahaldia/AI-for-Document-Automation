from function import retrieve_cla
import streamlit as st
from datetime import datetime
import numpy as np
import cv2
import pytesseract as pt
import re
from textblob import TextBlob
import pandas as pd
from bokeh.models.widgets import Div
import webbrowser

st.title("""
CLA Checker
	""")
today = datetime.today().date()

def retrieve_cla(dataset,title):

    today = datetime.today().date()
    dataset=pd.read_csv(dataset,index_col=0)
    dataset['dates']=pd.to_datetime(dataset['dates'],utc=False)
    dataset['dates'] = dataset['dates'].dt.date

    dataset_match= dataset[dataset['title'] == title]
    update = dataset_match[dataset_match['dates'] == today]


    if len(update) >0:
        st.write('Updates were made at')
        st.write(today.day,today.strftime("%B"))
        st.write('stating')
        st.write(str(update.text.values))
        link= update['link'].values



        if st.button('GET PDF'):
            st.markdown(link, unsafe_allow_html=True)
            browser = webbrowser.get('safari')
            browser.open_new_tab(link)





        # if st.button('Open PDF'):
        #     webbrowser.open_new_tab(link)

       # return 'Updates were made at', today.day, today.strftime("%B"), 'stating', str(update.text.values), 'click here to download PDF',update.link
    elif len(dataset_match) ==0:

       return 'No Such Label'
    else:
       return 'No Updates'




selected_cla = st.selectbox('Select', ['Select One','UK Immigration','Politics', 'Healthcare', 'Bears'])
if selected_cla is not None:

    st.write("")
    st.write("-------------------------------------")
    st.write("Finding if there are any updates...")
    st.write("-------------------------------------")
    label=retrieve_cla('data2.csv',selected_cla)
    st.write(label)





def extract(img):
    slide=st.sidebar.slider("Select Page Segmentation Mode",1,14)
    conf=f"-l eng --oem 3 --psm {slide}"
    text=pt.image_to_string(img, config = conf)
    if(text!=""):
        st.markdown("<h1 style='color:yellow;'>Extracted Text</h1>", unsafe_allow_html=True)
        slot1=st.empty()
        slot2=st.empty()
        if(st.sidebar.checkbox("Apply Spelling Correction")):
            corrected=TextBlob(text).correct()
            slot1.markdown(f"{corrected}", unsafe_allow_html=True)
            polar=round(corrected.sentiment.polarity,2)
            slot2.markdown(f"""<h1 style='color:yellow;'>Polarity: <span style='color:white;'>{polar}</span> Sentiment: <span style='color:white;'>{sentiments(polar)}</span></h1>""", unsafe_allow_html=True)
        if(st.sidebar.checkbox("Remove Numbers & Special Characters")):
            filtered=re.sub(r'[^A-Za-z ]+', '', text)
            slot1.markdown(f"{filtered}", unsafe_allow_html=True)
            polar=round(TextBlob(filtered).sentiment.polarity,2)
            slot2.markdown(f"""<h1 style='color:yellow;'>Polarity: <span style='color:white;'>{polar}</span> Sentiment: <span style='color:white;'>{sentiments(polar)}</span></h1>""", unsafe_allow_html=True)
        else:
            slot1.markdown(f"{text}", unsafe_allow_html=True)
            polar=round(TextBlob(text).sentiment.polarity,2)
            slot2.markdown(f"""<h1 style='color:yellow;'>Polarity: <span style='color:white;'>{polar}</span> Sentiment: <span style='color:white;'>{sentiments(polar)}</span></h1>""", unsafe_allow_html=True)


st.sidebar.markdown("<h1 style='text-align: center;color: #2C3454;margin-top:30px;margin-bottom:-20px;'>Select Image</h1>", unsafe_allow_html=True)

image_file = st.sidebar.file_uploader("", type=["jpg","png","jpeg"])
if image_file is not None:
    st.markdown("<h1 style='color:yellow;'>Uploaded Image</h1>", unsafe_allow_html=True)
    st.image(image_file,width=400)
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    radio=st.sidebar.radio("Select Action",('Text Extraction','Thresholding'))
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if(radio=="Text Extraction"):
        extract(img)
