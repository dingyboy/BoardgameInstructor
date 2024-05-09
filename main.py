import streamlit as st
import os
st.title('Greatest of Three Numbers') # Set Title of the webapp

choice1 = st.number_input('Enter First number') #Accepts a number input
choice2 = st.number_input('Enter Second number')
choice3 = st.number_input('Enter Third number')

string = f'Maximum value is {max(choice1,choice2,choice3)}'

#test
st.write(string)

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