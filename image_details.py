import streamlit as st
from PIL import Image
import time
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def img_captioning2(file):
    api_url = os.getenv("IMUN_URL2", "")
    # q = os.getenv("IMUN_PARAMS2", "")
    api_url += "?" + "api-version=2023-02-01-preview&model-version=latest&features=caption"

    # file_path = "/home/ubuntu/Downloads/1613459883.noatek_password_dean_sig.png"
    # with open(file_path, "rb") as file:
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": os.getenv("IMUN_SUBSCRIPTION_KEY2", ""),
    }
    response = requests.post(api_url, headers=headers, data=file)

    if response.status_code == 200:
        response_data = response.json()
        print(22, response_data)

        return response_data["captionResult"]["text"]
    else:
        response_data = response.json()
        print(29, response_data)
        error_message = response_data.get("error", {}).get("message", "")
        raise Exception("API request failed with status code {}: {}".format(response.status_code, error_message))



def main():
    st.title("Image Details")

    # Upload image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        filecontent = uploaded_file.read()
        # print(49, filecontent)
        # Open the uploaded image using PIL
        image = Image.open(uploaded_file)
        image_width, image_height = image.size

        # Display the image
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        start_time = time.time()
        st.write(img_captioning2(filecontent))
        end_time = time.time()
        execution_time = end_time - start_time
        st.write("Execution Time:", execution_time, "seconds")

        # Display the image details
        # st.write("Image Width:", image_width)
        # st.write("Image Height:", image_height)

if __name__ == "__main__":
    main()
