import pytesseract
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
from langdetect import detect


pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Path of the pdf 
PATH = "src/notebooks/"
pdf_name = '100.pdf'


def extract_text(path,name) :

    ''' 
    Extracts text from pdf and 
    returns a list of all the strings which are in french

    '''
    PDF_file = path+name
    # Store all the pages of the PDF in a variable 
    pages = convert_from_path(PDF_file, 500) 
  
    # Counter to store images of each page of PDF to image 
    image_counter = 1
    
    # Iterate through all the pages stored above 
    for page in pages: 
        
        page2img(page,image_counter,name)
        # Increment the counter to update filename 
        image_counter += 1

    fr_list = image_to_text(image_counter,name)

    return fr_list


def page2img(page,img_cnt,name):
    
    # Declaring filename for each page of PDF as JPG 
    filename = name+"_"+str(img_cnt)+".jpg"
      
    # Save the image of the page in system 
    page.save(filename, 'JPEG') 
  


def text_to_list(text):
    to_list = []
    to_list = text.split('\n\n')
    to_list = list(filter(lambda x: x != " ", to_list))
    return to_list


def is_french(stringx) :
    try :
        if detect(stringx.lower()) == 'fr' :
            return True
    except :
        return False


def image_to_text(image_counter,name) :   
    ''' 
    Part #2 - Recognizing text from the images using OCR 
    '''
    
    # Variable to get count of total number of pages 
    filelimit = image_counter-1
  
    fr_list = []
  
    # Iterate from 1 to total number of pages 
    for i in range(1, filelimit + 1): 
  
        # Set filename to recognize text from 
    
        filename = name+"_"+str(i)+".jpg"
          
        # Recognize the text as string in image using pytesserct 
        text = str(((pytesseract.image_to_string(Image.open(filename))))) 
  
        text = text.replace('-\n', '')

        text_list = text_to_list(text)
        for line in text_list :
            if is_french(line) :
                fr_list.append(line.replace('\n',' '))
    
    return fr_list


french_text = extract_text(PATH,pdf_name)
print(french_text)
