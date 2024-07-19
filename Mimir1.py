import streamlit as st
import requests

# App title
st.set_page_config(page_title="Research Paper Generator")

# User input for title and theme
with st.sidebar:
    st.title('Research Paper Generator')
    title = st.text_input('Enter the title of your research paper:')
    theme = st.text_input('Enter the theme of your research paper:')

# Function for generating research paper sections using Scholarcy's API
def generate_section(title, theme, section_type):
    api_url = "https://api.scholarcy.com/v1/summarize"
    payload = {
        "title": title,
        "theme": theme,
        "format": "flashcards",
        "section_type": section_type
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        flashcards = response.json()
        section_response = flashcards[0]["summary"]
        return section_response
    else:
        return None

# Generate research paper sections
if title and theme:
    abstract_response = generate_section(title, theme, "abstract")
    introduction_response = generate_section(title, theme, "introduction")
    literature_review_response = generate_section(title, theme, "literature review")
    methodology_response = generate_section(title, theme, "methodology")

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
