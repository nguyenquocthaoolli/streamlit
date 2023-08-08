import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw
import time
import os
import requests
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import json
import uuid
import io

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os

# import audio
import threading
from multiprocessing import Queue

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from st_draggable_list import DraggableList

st.set_page_config(layout="wide")
chat = ChatOpenAI(temperature=.7)

class Message:
    def __init__(self, content, type):
        self.content = content
        self.type = type
        self.id = uuid.uuid4()

# messages = [
#     Message(content="You are a nice AI bot that helps a user figure out where to travel in one short sentence", type="system"),
#     Message(content="I like the beaches where should I go?\nPlease recommend somewhere in Europe", type="human"),
#     Message(content="You should go to Nice, France", type="ai"),
#     Message(content="What else should I do when I'm there?", type="human")
# ]

# st.title("Message Editor")

# for m in messages:
#     print(f'[{m.type}]: {m.content}')


def convertTextToMessage(text):
    messages = []
    lines = text.strip().split('\n')
    current_type = ''
    current_content = []
    def add_message():
        content = '\n'.join(current_content).strip()
        if not content: return 
        message=None
        if current_type=='system':
            message = SystemMessage(content=content)
        elif current_type=='human':
            message = HumanMessage(content=content)
        elif current_type=='ai':
            message = AIMessage(content=content)
        if message:
            messages.append(message)

    for line in lines:
        if line.startswith('[system] '):
            add_message()
            current_type = 'system'
            current_content = [line.replace('[system] ', '')]
        elif line.startswith('[human] '):
            add_message()
            current_type = 'human'
            current_content = [line.replace('[human] ', '')]
        elif line.startswith('[ai] '):
            add_message()
            current_type = 'ai'
            current_content = [line.replace('[ai] ', '')]
        else:
            current_content.append(line)
    add_message()
    return messages

def render_messages(messages):
    for idx, message in enumerate(messages):
        st.markdown(f'**#{idx+1} {message.type}**')
        st.text(message.content)

def main_page():
    if st.session_state.get('text', '') == "":
        st.session_state.text='''[system] You are a nice AI bot that helps a user figure out where to travel in one short sentence
[human] I like the beaches where should I go?
Please recommend somewhere in Europe
[ai] You should go to Nice, France
[human] What else should I do when I'm there?
        '''
    print(107, st.session_state.text)
    col1, col2 = st.columns([0.5, 0.5])
    with col2:
        # st.session_state.text = st.text_area('Messages', st.session_state.text, height=1000)
        new_text = st.text_area('Messages', st.session_state.text, height=1000)
        # print(113, new_text)
        if new_text != st.session_state.text:
            st.session_state.text = new_text
    with col1:
        messages = convertTextToMessage(st.session_state.text)
        render_messages(messages)
        if st.button('Chat'):
            with st.spinner("Thinking..."):
                t = chat(messages=messages).content
                print(110, t)
                st.session_state.text = st.session_state.text + '\n[ai] ' + t
            st.experimental_rerun()






# Run the application
if __name__ == '__main__':
    main_page()