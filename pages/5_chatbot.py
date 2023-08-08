import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from st_draggable_list import DraggableList

st.set_page_config(layout="wide")
chatllm = ChatOpenAI(temperature=.7)

# App title
# st.set_page_config(page_title="🤗💬 ChatGPT")

# Hugging Face Credentials
# with st.sidebar:
#     st.title('🤗💬 HugChat')
#     if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
#         st.success('HuggingFace Login credentials already provided!', icon='✅')
#         hf_email = st.secrets['EMAIL']
#         hf_pass = st.secrets['PASS']
#     else:
#         hf_email = st.text_input('Enter E-mail:', type='password')
#         hf_pass = st.text_input('Enter password:', type='password')
#         if not (hf_email and hf_pass):
#             st.warning('Please enter your credentials!', icon='⚠️')
#         else:
#             st.success('Proceed to entering your prompt message!', icon='👉')
#     st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')
    
# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages =  [
        SystemMessage(content="You are a nice AI bot that helps a user figure out where to travel in one short sentence"),
        HumanMessage(content="I like the beaches where should I go?"),
        AIMessage(content="You should go to Nice, France"),
        HumanMessage(content="What else should I do when I'm there?")
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.write(message.content)

# Function for generating LLM response
def generate_response():
    return chatllm(messages=st.session_state.messages).content
    # return             t = chat(messages=messages).content
    #         print(110, t)
    #         st.session_state.text += '\n[ai] ' + t
    # # Hugging Face Login
    # sign = Login(email, passwd)
    # cookies = sign.login()
    # # Create ChatBot                        
    # chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    # return chatbot.chat(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("human"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1].type=='human':
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response() 
            st.write(response) 
            st.session_state.messages.append(AIMessage(content=response))
    # message = {"role": "assistant", "content": response}
