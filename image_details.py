import streamlit as st
from PIL import Image
import time
import os
import requests
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.oauth2 import service_account
import json
import uuid
import audio
import threading
from multiprocessing import Queue

from dotenv import load_dotenv
load_dotenv()

# print(14, json.dumps(dict(st.secrets["connection"]["gcs"])))

credentials = service_account.Credentials.from_service_account_info(
    dict(st.secrets["connection"]["gcs"]), scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def img_captioning2(filecontent):
    api_url = os.getenv("IMUN_URL2", "")
    # q = os.getenv("IMUN_PARAMS2", "")
    api_url += "?" + "api-version=2023-02-01-preview&model-version=latest&features=caption"

    # file_path = "/home/ubuntu/Downloads/1613459883.noatek_password_dean_sig.png"
    # with open(file_path, "rb") as file:
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": os.getenv("IMUN_SUBSCRIPTION_KEY2", ""),
    }
    response = requests.post(api_url, headers=headers, data=filecontent)

    if response.status_code == 200:
        response_data = response.json()
        # print(22, response_data)

        return response_data["captionResult"]["text"]
    else:
        response_data = response.json()
        print(29, response_data)
        error_message = response_data.get("error", {}).get("message", "")
        raise Exception("API request failed with status code {}: {}".format(response.status_code, error_message))

maikadomain = "https://stg-content-gateway.development.iviet.com"

def perform_ocr(filecontent):
    response = requests.post(maikadomain + "/api/command/ocr", headers={"Authorization":"Bearer " + os.getenv("MAIKA_TOKEN")}, files={
        "file": filecontent
    })
    if response.status_code==200:
        response_data = response.json()
        # print(22, response_data)
        return response_data["results"], response_data["locale"]
    else:
        response_data = response.json()
        print(29, response_data)
        return Exception(response_data["message"])
    # client = vision.ImageAnnotatorClient(credentials=credentials)
    # # content = image.read()
    # image = types.Image(content=filecontent)
    # response = client.text_detection(image=image)
    # texts = response.text_annotations
    # # print(42, texts)
    # if texts:
    #     return texts[0].description
    # return None

def translate(text):
    response = requests.post(maikadomain + "/api/command/translate", headers={"Authorization":"Bearer " + os.getenv("MAIKA_TOKEN"), 
                                                                              'Content-Type': 'application/json'}, 
                                                                              data=json.dumps({
        "text": text,
        "target_language":"vi",
    }))
    if response.status_code==200:
        return response.content.decode()
    else:
        response_data = response.json()
        # print(29, response_data)
        return Exception(response_data["message"])

def summarize(text):
    response = requests.post(maikadomain + "/api/command/summarize", headers={
        "Authorization":"Bearer " + os.getenv("MAIKA_TOKEN"), 
        'Content-Type': 'application/json'}, 
        data=json.dumps({
        "text": text,
        "request_id": str(uuid.uuid4())
    }), stream=True)
    if response.status_code==200:
        for chunk in response.iter_content(chunk_size=None):
            yield chunk.decode()
    else:
        response_data = response.json()
        print(99, response_data)
        return Exception(response_data["message"])

def makeSpeakRequest(generator, locale):
    u = f'{maikadomain}/api/command/speak/stream?locale={locale}&audio_type=audio/wav&request_id=d1000'
    print(104, 'start making speak stream request')
    response = requests.post(u, headers={
        "Authorization":"Bearer " + os.getenv("MAIKA_TOKEN")}, 
        data=generator, stream=True)
    print(108, 'get response from speak stram')
    
    if response.status_code==200:
        for chunk in response.iter_content(chunk_size=None):
            # print(109, len(chunk))
            yield chunk
    else:
        response_data = response.json()
        print(130, response_data)
        return Exception(response_data["message"])
def speak(generator, locale):
    gen = makeSpeakRequest(generator, locale)
    threading.Thread(target=audio.play_audio, args=(gen,)).start()

def main():
    st.title("Image Details")

    # print(st.secrets)

    # Upload image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    # caption_enabled = st.checkbox("Generate Caption")
    caption_enabled = False
    # ocr_enabled = st.checkbox("Perform OCR")
    ocr_enabled = True
    if ocr_enabled:
        translate_enabled = st.checkbox("Translate")
        summarize_enabled = st.checkbox("Summarize")
    
    if summarize_enabled:
        audio_enabled = st.checkbox("Audio")

    # if st.checkbox('playaudio'):
    #     print(153, 'start playing audio')
    #     threading.Thread(target=audio.testaudio).start()
    #     # audio.testaudio()
    #     print(155, 'after calling testaudio')
    




    if uploaded_file is not None:
        filecontent = uploaded_file.read()
        # print(49, filecontent)
        # Open the uploaded image using PIL
        image = Image.open(uploaded_file)
        image_width, image_height = image.size

        # Display the image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if caption_enabled:        
            start_time = time.time()
            st.write(img_captioning2(filecontent))
            st.write("Execution Time:", time.time() - start_time, "seconds")
        ocr = ''
        locale = 'vi'
        if ocr_enabled:
            start_time = time.time()
            ocr, locale = perform_ocr(filecontent)
            st.write(ocr)
            st.write("Execution Time:",  time.time() - start_time, "seconds")
        if translate_enabled:
            ocr = translate(ocr)
            st.write("Translate: ", ocr)
        if summarize_enabled:
            st.write("Summarize: ")
            placeholder = st.empty()
            if audio_enabled:
                q = Queue()
                threading.Thread(target=speak, args=(audio.queueToGenerator(q), locale)).start()

            x = ocr
            ocr = ''
            for data in summarize(x):
                ocr += data
                q.put(data)
                placeholder.write(ocr)
            q.put(None)
            # st.write("Summarize: ", ocr)
        # result_placeholder = st.empty()
        # x=''
        # for i in range(100):
        #     x += str(i) + ','
        #     time.sleep(0.1)
        #     # st.write(x)
        #     result_placeholder.write(x)



        # Display the image details
        # st.write("Image Width:", image_width)
        # st.write("Image Height:", image_height)

if __name__ == "__main__":
    main()
