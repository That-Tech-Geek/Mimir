import streamlit as st

# App title
st.set_page_config(page_title="Research Paper Generator")

# User input for title and theme
with st.sidebar:
    st.title('Research Paper Generator')
    title = st.text_input('Enter the title of your research paper:')
    theme = st.text_input('Enter the theme of your research paper:')

# Function for generating research paper sections
def generate_section(prompt):
    # Simple text generation approach
    response = f"This is a generated {prompt} for a research paper on {theme} titled {title}."
    return response

# Generate research paper sections
if title and theme:
    abstract_response = generate_section("abstract")
    introduction_response = generate_section("introduction")
    literature_review_response = generate_section("literature review")
    methodology_response = generate_section("methodology")

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
