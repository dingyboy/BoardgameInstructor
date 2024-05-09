# importing required modules 
from pypdf import PdfReader 
  
# creating a pdf reader object 
reader = PdfReader('railroad_ink_rules.pdf') 
  
# printing number of pages in pdf file 
print(len(reader.pages)) 
  
# getting a specific page from the pdf file 
page = reader.pages[0] 
  
# extracting text from page 
text = page.extract_text() 
print(text) 

page_2 = reader.pages[1].extract_text()
print(page_2)

page_3 = reader.pages[2].extract_text()
print(page_3)

page_4 = reader.pages[3].extract_text()
print(page_4)

