# Boardgame Instructor
Chatbot that helps the user with board game instructions.

Python 3.11.5

Creating virtual env:
pip install virtualenv
python -m venv bgenv

Activating virtual env:
source bgenv/Scripts/activate

Checking virtual env (This will show that you are in the virtual environment path):
pip -V 

Helpful commands:
pip list - shows all the installed packages
pip freeze > requirements.txt - moves all the packages into requirements.txt file
pip install -r requirements.txt - reads the requirements file and installs the packages

https://github.com/dingyboy/BoardgameInstructor

Chunking Strategy (Semantic Chunking):
https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/semantic-chunker/ 

TODO: 
Need to convert pdf to text 

Need to do Semantic Chunking

Need to convert chunk into text-embedding-3-small (https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)

Need to insert into mongoDB vector search

Need to query vector DB

Need to build UI search bar

Need to build UI chat window

Need to ensure mobile compatibility 


