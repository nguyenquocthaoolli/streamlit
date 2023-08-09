import streamlit as st
import requests
import os
import time

# Streamlit app title
st.title("Image Uploader")

maikadomain = os.getenv("MAIKA_DOMAIN")

# Upload image using Streamlit's file uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
uploadDirectlyToGoogle = st.checkbox("Upload directly to google")

def main_page():

    if uploaded_file is not None:

        if uploadDirectlyToGoogle:
            start_time = time.time()

            response = requests.post(maikadomain + '/api/command/upload-file',
                                     headers={"Authorization": "Bearer " + os.getenv("MAIKA_TOKEN")},
                                      data = {'file_name': uploaded_file.name})

            end_time = time.time()

            result = response.json()
            if response.status_code != 200:
                st.error(result)
                return 
            st.write(f"Request time: {end_time - start_time:.4f} seconds")
            st.write(result)
            requests.put(result['results']['upload_url'], data = uploaded_file)
            end_time2 = time.time()
            st.write(f"Request time: {end_time2 - end_time:.4f} seconds")
            image_url = result['results']['url']
            st.image(image_url, caption="Uploaded Image", use_column_width=True)

            st.write(f"Request time: {end_time2 - start_time:.4f} seconds")
        else:
            start_time = time.time()

            # Create a form for uploading the file
            files = {"file": uploaded_file}            
            # Submit POST request to the API
            response = requests.post(maikadomain + "/api/command/upload-file", 
                                     headers={"Authorization": "Bearer " + os.getenv("MAIKA_TOKEN")},
                                     files=files)

            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()["results"]
                image_url = result["url"]
                
                # Display the uploaded image
                st.image(image_url, caption="Uploaded Image", use_column_width=True)
            else:
                st.error("Error uploading the image. Please try again.")
                st.error(response.json())

            st.write(f"Request time: {end_time - start_time:.4f} seconds")

if __name__ == '__main__':
    main_page()
