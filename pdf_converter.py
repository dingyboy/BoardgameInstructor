# # Import libraries
# import platform
# from tempfile import TemporaryDirectory
# from pathlib import Path
 
import pytesseract
# from pdf2image import convert_from_path
from PIL import Image
import os

# print(platform.system())

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )
# # Path of the Input pdf
# PDF_file = Path(r"railroad_ink_rules.pdf")
 
# # Store all the pages of the PDF in a variable
# image_file_list = []
 
# text_file = Path("out_text.txt")


# import module
from pdf2image import convert_from_path
parent_dir = os.environ.get('BOARDGAME_ASSET_PATH')

 
def create_folder(bg_name='railroad_ink'):

  directory = bg_name
  path = os.path.join(parent_dir, directory)

  try: 
      os.makedirs(path, exist_ok = True) 
      print("Directory '%s' created successfully" % directory) 
  except OSError as error: 
      print("Directory '%s' can not be created" % directory)

# Store Pdf with convert_from_path function
def convert_PDF_to_JPEG(bg_name='railroad_ink'):
  images = convert_from_path(parent_dir + '/' + bg_name +  '_rules.pdf')
  
  for i in range(len(images)):
        # Save pages as images in the pdf
      images[i].save(parent_dir + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.jpg', 'JPEG')

def convert_JPEG_to_TxT(bg_name='railroad_ink'):
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

  images = convert_from_path(parent_dir + '/' + bg_name +  '_rules.pdf')

  for i in range(len(images)):
    rules_text = pytesseract.image_to_string(Image.open(parent_dir + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.jpg')).encode()
    with open(parent_dir + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.txt', 'wb') as f:
       f.write(rules_text)


# create_folder()
# convert_PDF_to_JPEG()
convert_JPEG_to_TxT()