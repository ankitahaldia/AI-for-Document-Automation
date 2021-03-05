import pytesseract
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
from langdetect import detect
import src.services as sv
from io import BytesIO
import cv2


pages=convert_from_path("test.pdf")
images = []


for page in pages:
    with BytesIO() as f:
        page.save(f,format="jpg")
        f.seek(0)
        img_page= cv2.imread(f)
for i in images:
    cv2.imshow(i)