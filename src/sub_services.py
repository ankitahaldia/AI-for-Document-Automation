from PIL import Image 
import cv2
import pytesseract 
import src.services as sv


# TODO : use relative path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


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
            if sv.is_french(line) :
                fr_list.append(line.replace('\n',' '))
    
    return fr_list

def opencv_to_text(image_counter,name) :
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
        text = str(((pytesseract.image_to_string(cv2.imread(filename))))) 
  
        text = text.replace('-\n', '')

        text_list = text_to_list(text)        
    
    return text_list
