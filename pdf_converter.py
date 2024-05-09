# # Import libraries
# import platform
# from tempfile import TemporaryDirectory
# from pathlib import Path
 
# import pytesseract
# from pdf2image import convert_from_path
# from PIL import Image
 

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
 
 
# Store Pdf with convert_from_path function
images = convert_from_path('railroad_ink_rules.pdf')
 
for i in range(len(images)):
   
      # Save pages as images in the pdf
    images[i].save('page'+ str(i) +'.jpg', 'JPEG')