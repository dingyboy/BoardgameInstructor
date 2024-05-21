import streamlit as st
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import json
from auxiliary import connect_openai, generate_embedding, request_response, setup_mongo_connection, fetch_from_mongo

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
    try:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role":"user", "content":prompt})

        # need to fetch from MongoDB Database here
        # based on the promtp here: prompt
        # maybe we have a checkbox to ask the user if we want to use images or not

        openai_client = connect_openai()


        embedding = generate_embedding(openai_client)


        boardgame_display_key = "display_name"
        boardgame_database_key = "database_name"
        boardgame_database_name = None
        for game in BOARDGAME_LIST:
            if game.get(boardgame_display_key) == boardgame_option:
                boardgame_database_name = game.get(boardgame_database_key)
                break
        
        print(boardgame_database_name)
        mongo_collection = setup_mongo_connection()

        # print(BOARDGAME_LIST)

        mongo_response = None
        if boardgame_database_name != None:
            mongo_response = fetch_from_mongo(mongo_collection, embedding, boardgame_database_name)
        else:
            # TODO: Need to have a response here where it just says please refresh and try again
            print("Was not able to find boardgame name or some other internal error :'(")

        enhanced_prompt = prompt 

        for response in mongo_response:
            enhanced_prompt += " *** " + response['rule_description'] + " !!! "

        # TODO: Need to check if gpt4o is enabled and if it is we need to fetch images and use them as part of the response 

        # openai_response = client_openai.chat.completions.create(
        #     model=model_option,
        #     messages= [
        #         {"role": "system", "content": SYSTEM_PROMPT},
        #         {"role": "user", "content": prompt}
        #     ]
        # )        
        openai_response = request_response(openai_client, model_option, enhanced_prompt)

        response = openai_response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        response = "We apologize but an issue occurred please try again later. :'("
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

