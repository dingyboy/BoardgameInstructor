import streamlit as st
import os


col1, col2 = st.columns(2)

with col1:
    st.title('Boardgame Buddy') # Set Title of the webapp
with col2:
    st.image('boardgame_buddy.png')

# choice1 = st.number_input('Enter First number') #Accepts a number input
# choice2 = st.number_input('Enter Second number')
# choice3 = st.number_input('Enter Third number')
if 'entrance_greeting' not in st.session_state:
    st.session_state['entrance_greeting'] = 'Slider to enter.'

slider_value = st.slider("", 0, 100, 0)
st.write(st.session_state.entrance_greeting)
if (slider_value > 25):
    st.session_state.entrance_greeting = "Wheeee!"
if (slider_value > 50):
    st.session_state.entrance_greeting = 'Whooaa! :o'
if (slider_value > 75):
    st.session_state.entrance_greeting = 'Ahhhhh! :D'
if(slider_value > 95):
    st.session_state.entrance_greeting = 'Here we go! :3'

# print(os.environ.get('OPENAI_API_KEY'))
# from openai import OpenAI
# client = OpenAI(    
#         api_key=os.environ.get('OPENAI_API_KEY')
#     )

# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#     ]
# )

# print(completion.choices[0].message)