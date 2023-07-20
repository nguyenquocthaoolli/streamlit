import streamlit as st
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

# import audio
import threading
from multiprocessing import Queue

from dotenv import load_dotenv
load_dotenv()

credentials = service_account.Credentials.from_service_account_info(
    dict(st.secrets["connection"]["gcs"]), scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# def detect_document_text_with_confidence(full_text_annotation, min_confidence=0.9):

#     filtered_text_blocks = []
#     for page in full_text_annotation.pages:
#         for block in page.blocks:
#             for paragraph in block.paragraphs:
#                 for word in paragraph.words:
#                     text = ''.join([symbol.text for symbol in word.symbols])
#                     confidence = word.confidence
#                     if confidence > min_confidence:
#                         filtered_text_blocks.append((text, confidence))

#     return filtered_text_blocks

def detect_document_text_with_confidence(full_text_annotation, min_block_conf = 0.0, min_paragraph_conf=0.9, min_word_conf=0.0):
    result=''

    for page in full_text_annotation.pages:
        # print(42, page.confidence)
        block_texts = []
        for block in page.blocks:
            if float(block.confidence) < min_block_conf:
                continue
            paragraph_texts = []
            for paragraph in block.paragraphs:
                if float(paragraph.confidence) < min_paragraph_conf: continue

                words = []
                # print(48, paragraph.confidence)
                for word in paragraph.words:
                    if float(word.confidence)<min_word_conf: continue
                    # print(55, word)

                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    # if word_text=='quan': print(59, word_text, block.confidence, paragraph.confidence, word.confidence)
                    # paragraph_texts.append(word_text)
                    words.append(word_text)
                paragraph_texts.append(' '.join(words))
            block_text = ' '.join(t for t in paragraph_texts)
            block_texts.append(block_text)

        page_text = '\n\n'.join(b for b in block_texts)
        result += page_text
    return result



def ocr2(filecontent):
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = types.Image(content=filecontent)
    response = client.document_text_detection(image=image)
    # pages = response.full_text_annotation
    # with open("x.json", "w") as f:
        # json.dump(f, response.full_text_annotation)
    # print(42, dir(response), dir(pages))
    # print(pages[0].blocks[0])

    # if pages:
    # return response.full_text_annotation.text
        # return pages[0].blocks[0].parga
    # return None
    # return ' '.join(v[0] for v in detect_document_text_with_confidence(response.full_text_annotation))
    # return detect_document_text_with_confidence(response.full_text_annotation)
    return response.full_text_annotation




maikadomain = "https://stg-content-gateway.development.iviet.com"
# maikadomain = "http://localhost:3331"

def perform_ocr(filecontent):
    response = requests.post(
        maikadomain + "/api/command/ocr",
        headers={"Authorization": "Bearer " + os.getenv("MAIKA_TOKEN")},
        files={"file": filecontent},
        data={"request_id": str(uuid.uuid4())},
    )
    if response.status_code == 200:
        response_data = response.json()
        print(22, response_data)
        return response_data["results"], response_data["locale"]
    else:
        response_data = response.json()
        print(29, response_data)
        raise Exception(response_data["message"])
# 

def translate(text):
    response = requests.post(
        maikadomain + "/api/command/translate",
        headers={
            "Authorization": "Bearer " + os.getenv("MAIKA_TOKEN"),
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "text": text,
                "target_language": "vi",
            }
        ),
    )
    if response.status_code == 200:
        return response.content.decode()
    else:
        response_data = response.json()
        # print(29, response_data)
        return Exception(response_data["message"])
    
def getUrls():
    for i in range(0,8):
        yield f'https://storage.googleapis.com/maika-ai-ext/test/{i}.jpg'

min_block_conf = min_paragraph_conf = min_word_conf = 0.0


def main_page():
    st.title("Test images")
    min_block_conf = st.sidebar.slider( label="min_block_conf", min_value=0.0, max_value=1.0, value=0.0, step=0.01, )
    min_paragraph_conf = st.sidebar.slider( label="min_paragraph_conf", min_value=0.0, max_value=0.8, value=0.0, step=0.01, )
    min_word_conf = st.sidebar.slider( label="min_word_conf", min_value=0.0, max_value=1.0, value=0.8, step=0.01, )


    # Create a generator for the image URLs
    image_urls = getUrls()

    # Iterate over the image URLs and display the columns
    for image_url in image_urls:
        response = requests.get(image_url)
        # print(image_url, len(response.content))
        file_content = response.content
        col1, col2,col3 = st.columns(3)
        with col1:
            # st.subheader("Image")
            image = Image.open(io.BytesIO(file_content))
            st.image(image, use_column_width=True)

        with col2:
            # st.subheader("OCR Result")
            ocr_results, locale = perform_ocr(file_content)
            st.write(ocr_results)
        ftannotation = ocr2(file_content)
        with col3:
            # ocr_results_2 = ocr2(file_content)

            ocr_results_2 = detect_document_text_with_confidence(ftannotation, min_block_conf, min_paragraph_conf, min_word_conf)
            st.write(ocr_results_2)

        # Display the translation in the third column
        # with col3:
        #     st.subheader("Translation")
        #     translation = translate(ocr_results)
        #     st.write(translation)

        # st.markdown("---")
# Run the application
if __name__ == '__main__':
    main_page()