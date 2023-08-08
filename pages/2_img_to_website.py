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

from dotenv import load_dotenv
load_dotenv()

maikadomain = os.getenv("MAIKA_DOMAIN")

if "html" not in st.session_state:
    st.session_state.html = ""
if "image" not in st.session_state:
    st.session_state.image = ''


credentials = service_account.Credentials.from_service_account_info(
    dict(st.secrets["connection"]["gcs"]), scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image

subscription_key = os.getenv("IMUN_SUBSCRIPTION_KEY2", "")
endpoint = os.getenv("AZURE_ENDPOINT", "")
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def text_recognition(img_url):

    print("===== Read File - remote =====")
    print(endpoint, subscription_key)
    read_response = computervision_client.read(img_url,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    

    layout = []
    if read_result.status == OperationStatusCodes.succeeded:
        print(read_result)
        print(read_result.analyze_result)
        # print(read_result.analyze_result.read_results)
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                layout.append({line.text:line.bounding_box})
    print(layout)
    print("End of Computer Vision.")
    return layout

def html_gen(layout):
    prompt = PromptTemplate(
        template="""This is a layout of a handwriting website design, including text and their coordinates of four outer vertices. 
        Make an HTML modern sans-serif website that reflects these elements and decide which 
        CSS can be used to match their relative positions, try to use proper layout tags to match
         their font size and relative placement based on their coordinates. 
         Use <ul> and <li> if the elements look like as menu list. 
         Smartly use function tags like <button> <input> if their names look like that.
         Your design should be prior to the coordinates, 
         then you should also use some imagination for the layout and CSS from common web design principle.
         Remember, don't use absolute coordinates in your HTML source code. 
         Generate only source code file, no description: {layout}.\n""",
        input_variables=["layout"]
    )
    # llm = ChatOpenAI(model="gpt-4-0613",temperature=0)
    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(prompt=prompt, llm=llm)
    output = chain.run(layout=layout)
    print(output)

    return output

def image_run():
    html_code = ""
    layout = text_recognition(st.session_state.img)
    if layout != []:
        html_code = html_gen(layout)

    st.session_state.html = html_code
    st.session_state.image = st.session_state.img


def main_page():
    st.title("Image to website")
    # reg_enabled = st.checkbox("Ocr")
    # if reg_enabled:
    #     layout = text_recognition('https://storage.googleapis.com/maika-ai-ext/test/drawing-website.png')
    #     html_gen(layout)
    col1, col2 = st.columns([0.5, 0.5], gap='medium')
    with col1:
        st.text_input("Image URL:", value="https://storage.googleapis.com/maika-ai-ext/test/drawing-website.png", key='img')
        st.button("Run", on_click=image_run)
        if st.session_state.img != '':
            st.image(st.session_state.img)
    with col2:
        with st.expander("See source code"):
            st.code(st.session_state.html)
        with st.container():
            components.html(st.session_state.html, height=600, scrolling=True)


# Run the application
if __name__ == '__main__':
    main_page()