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
  print("Start: create_folder " + bg_name)
  directory = bg_name
  path = os.path.join(parent_dir, directory)

  try: 
      os.makedirs(path, exist_ok = True) 
      print("Directory '%s' created successfully" % directory) 
      print("Finish: create_folder " + bg_name)

  except OSError as error: 
      print("Directory '%s' can not be created" % directory)
      print("Finish: create_folder " + bg_name)

  
# Store Pdf with convert_from_path function
def convert_PDF_to_JPEG(bg_name='railroad_ink'):

  print("Start: convert_PDF_to_JPEG " + bg_name)

  images = convert_from_path(parent_dir + '/' + bg_name +  '_rules.pdf')
  
  for i in range(len(images)):
        # Save pages as images in the pdf
      images[i].save(parent_dir + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.jpg', 'JPEG')
  print("Finish: convert_PDF_to_JPEG " + bg_name)

def convert_JPEG_to_TxT(bg_name='railroad_ink'):
  
  print("Start: convert_JPEG_to_TxT " + bg_name)

  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

  images = convert_from_path(parent_dir + '/' + bg_name +  '_rules.pdf')

  for i in range(len(images)):
    rules_text = pytesseract.image_to_string(Image.open(parent_dir + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.jpg')).encode()
    with open(parent_dir + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.txt', 'wb') as f:
       f.write(rules_text)
  
  print("Finish: convert_JPEG_to_TxT " + bg_name)

def generate_asset(bg_name='railroad_ink'):

  print("Start: generate_asset " + bg_name)

  create_folder(bg_name)
  convert_PDF_to_JPEG(bg_name)
  convert_JPEG_to_TxT(bg_name)
  
  print("Finish: generate_asset " + bg_name)

generate_asset()