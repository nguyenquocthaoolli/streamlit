import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dotenv import load_dotenv
load_dotenv()

# TfidVectorizer, cosine_similarity: not so working


# Define a dictionary of questions and answers
faq = {
    "What is Streamlit?": "Streamlit is an open-source Python library that makes it easy to create custom web apps for machine learning and data science.",
    "How do I install Streamlit?": "You can install Streamlit using pip: `pip install streamlit`.",
    "Can I deploy Streamlit apps?": "Yes, you can deploy Streamlit apps to various platforms including Heroku, AWS, and others.",
    "What are the main features of Streamlit?": "Streamlit offers a simple and intuitive API, automatic app updates, real-time interactive widgets, and easy sharing of apps.",
}

class SearchQ:
    def __init__(self):
        embeddings = OpenAIEmbeddings()
        self.keys = list(faq.keys())
        self.docsearch = Chroma.from_texts(self.keys, embeddings, metadatas=[{"i":i} for i in range(len(self.keys))])
    def search(self, q):
        docs = self.docsearch.similarity_search(q)
        for v in docs:
            print(v.page_content, v.metadata)
        return ''
        
class Search2:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.keys = list(faq.keys())
        self.tfidf_matrix = self.vectorizer.fit_transform(self.keys)
    def search(self, q):
        user_question_vector = self.vectorizer.transform([q])
        similarities = cosine_similarity(user_question_vector, self.tfidf_matrix)
        print(similarities[0])
        ind = max(range(len(self.keys)), key=lambda i: similarities[0][i])
        if similarities[0][ind] >= 0.8: return self.keys[ind]

        return ''
    



# Streamlit app
def run_app():
    st.title("Question and Answer App")
    st.write("Welcome! Ask a question and get an answer.")
    # searchQ = SearchQ()
    searchQ = Search2()


    # Display the list of available questions
    # question = st.selectbox("Select a question:", list(faq.keys()))

    question = st.text_input("Ask your question:")

    question = searchQ.search(question)

    # Retrieve and display the answer for the selected question
    if question in faq:
        answer = faq.get(question)
        st.write(f"**Q:** {question}")
        st.write(f"**A:** {answer}")
    else:
        st.write("Question not found in the FAQ.")

# Run the app
if __name__ == '__main__':
    run_app()
