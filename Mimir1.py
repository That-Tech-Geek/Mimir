import streamlit as st
from gemini import generate_section

# App title
st.set_page_config(page_title="Research Paper Generator")

# User input for title and theme
with st.sidebar:
    st.title('Research Paper Generator')
    title = st.text_input('Enter the title of your research paper:')
    theme = st.text_input('Enter the theme of your research paper:')

# Function for generating research paper sections using Gemini
def generate_section_gemini(title, theme, section_type):
    try:
        section, stats = generate_section(title, theme, section_type)
        return section, stats
    except Exception as e:
        st.error(f"Error generating {section_type} section: {e}")
        return None, None

# Generate research paper sections
if title and theme:
    abstract_response, abstract_stats = generate_section_gemini(title, theme, "abstract")
    introduction_response, introduction_stats = generate_section_gemini(title, theme, "introduction")
    literature_review_response, literature_review_stats = generate_section_gemini(title, theme, "literature review")
    methodology_response, methodology_stats = generate_section_gemini(title, theme, "methodology")

    # Display generated responses
    st.header("Generated Research Paper Sections")
    st.subheader("Abstract")
    if abstract_response and abstract_stats:
        st.write(abstract_response)
        st.write("Stats:")
        st.write(f"Confidence Interval: {abstract_stats.get('confidence_interval', 'N/A')}")
        st.write(f"Significance Level: {abstract_stats.get('significance_level', 'N/A')}")
    else:
        st.write("Error generating abstract section.")
    st.subheader("Introduction")
    if introduction_response and introduction_stats:
        st.write(introduction_response)
        st.write("Stats:")
        st.write(f"Confidence Interval: {introduction_stats.get('confidence_interval', 'N/A')}")
        st.write(f"Significance Level: {introduction_stats.get('significance_level', 'N/A')}")
    else:
        st.write("Error generating introduction section.")
    st.subheader("Literature Review")
    if literature_review_response and literature_review_stats:
        st.write(literature_review_response)
        st.write("Stats:")
        st.write(f"Confidence Interval: {literature_review_stats.get('confidence_interval', 'N/A')}")
        st.write(f"Significance Level: {literature_review_stats.get('significance_level', 'N/A')}")
    else:
        st.write("Error generating literature review section.")
    st.subheader("Methodology")
    if methodology_response and methodology_stats:
        st.write(methodology_response)
        st.write("Stats:")
        st.write(f"Confidence Interval: {methodology_stats.get('confidence_interval', 'N/A')}")
        st.write(f"Significance Level: {methodology_stats.get('significance_level', 'N/A')}")
    else:
        st.write("Error generating methodology section.")
