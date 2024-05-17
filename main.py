import streamlit as st
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client_openai = OpenAI(api_key=OPENAI_API_KEY)


boardgame_list = ('Railroad Ink', 'Cascadia')

col1, col2 = st.columns(2)
with col1:
    st.title('Boardgame Buddy') # Set Title of the webapp
with col2:
    st.image('boardgame_buddy.png')

option = st.selectbox('Which pesky boardgame do you need help with?',
        boardgame_list)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What can I help you with?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content":prompt})


    openai_response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    response = openai_response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})