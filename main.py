import streamlit as st
from pages.image_details import imageDetailPage
from dotenv import load_dotenv
import pages.test_image as test_image
import pages.img_to_website as img_to_website

load_dotenv()
st.set_page_config(layout="wide")

# def main():
#     # Render the navigation menu
#     navigation()

#     # Check the page selection and render the corresponding page
#     if st.session_state.page == 'Image Detail':
#         imageDetailPage()
#     elif st.session_state.page == 'Test Image':
#         test_image.main_page()
#     elif st.session_state.page == 'Img to website':
#         img_to_website.main_page()

# def navigation():
#     # Create a list of page options
#     pages = ['Image Detail', 'Test Image', 'Img to website']

#     # Add radio buttons for page selection
#     st.sidebar.title('Navigation')
#     selected_page = st.sidebar.radio('Go to', pages, key='navigation', index=1)
#     set_page(selected_page)

# def set_page(page):
#     # Set the selected page in the session state
#     st.session_state.page = page


# def about_page():
#     st.title('About')
#     st.write('This is the About page. It provides information about the application.')

# # Initialize the session state
# if 'page' not in st.session_state:
#     st.session_state.page = 'Hello World'

# Run the application
# if __name__ == '__main__':
#     main()
