import streamlit as st
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()


BOARDGAME_LIST = []
BOARDGAME_DISPLAY_LIST = []
MODEL_LIST = []
SYSTEM_PROMPT = ""

with open('./public_asset/system_prompt.json') as a:
    SYSTEM_PROMPT = json.load(a)['content']

with open('./public_asset/boardgame_list.json') as b:
    BOARDGAME_LIST = json.load(b)
    for item in BOARDGAME_LIST:
        print(item)
        BOARDGAME_DISPLAY_LIST.append(item['display_name'])

with open('./public_asset/model_list.json') as c:
    model_temp_list = json.load(c)
    for item in model_temp_list:
        MODEL_LIST.append(item['name'])

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client_openai = OpenAI(api_key=OPENAI_API_KEY)


boardgame_list = ('Railroad Ink', 'Cascadia')
model_list =('gpt-3.5-turbo', 'gpt-4o')


col1, col2 = st.columns(2)
with col1:
    st.title('Board Game Buddy') # Set Title of the webapp
with col2:
    st.image('./public_asset/boardgame_buddy.png')

boardgame_option = st.selectbox('Which pesky boardgame do you need help with?', BOARDGAME_DISPLAY_LIST)
model_option = st.selectbox('Which model would you like to use?', MODEL_LIST)


if model_option == 'gpt-4o':
    enable_image = st.checkbox("Activate Advanced AI Visual Identification")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What can I help you with?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content":prompt})

    # need to fetch from MongoDB Database here
    # based on the promtp here: prompt
    # maybe we have a checkbox to ask the user if we want to use images or not

    openai_response = client_openai.chat.completions.create(
        model=model_option,
        messages= [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    response = openai_response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})


