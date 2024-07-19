import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="Research Paper Generator")

# Hugging Face Credentials
with st.sidebar:
    st.title('Research Paper Generator')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your research paper details!', icon='👉')

# User input for title and theme
title = st.text_input('Enter the title of your research paper:')
theme = st.text_input('Enter the theme of your research paper:')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# Generate research paper sections
if title and theme:
    abstract_prompt = f"Generate an abstract for a research paper on {theme} titled {title}"
    introduction_prompt = f"Generate an introduction for a research paper on {theme} titled {title}"
    literature_review_prompt = f"Generate a literature review for a research paper on {theme} titled {title}"
    methodology_prompt = f"Generate a methodology for a research paper on {theme} titled {title}"

    abstract_response = generate_response(abstract_prompt, hf_email, hf_pass)
    introduction_response = generate_response(introduction_prompt, hf_email, hf_pass)
    literature_review_response = generate_response(literature_review_prompt, hf_email, hf_pass)
    methodology_response = generate_response(methodology_prompt, hf_email, hf_pass)

    # Display generated responses
    st.header("Generated Research Paper Sections")
    st.subheader("Abstract")
    st.write(abstract_response)
    st.subheader("Introduction")
    st.write(introduction_response)
    st.subheader("Literature Review")
    st.write(literature_review_response)
    st.subheader("Methodology")
    st.write(methodology_response)
