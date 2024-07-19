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
    api_url = "https://api.scholarcy.com/v1/analyze"
    payload = {
        "title": title,
        "theme": theme,
        "format": "stats",
        "section_type": section_type,
        "analysis_type": "observations_and_inferences",
        "stats": {
            "confidence_interval": 0.95,
            "significance_level": 0.05
        }
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        analysis = response.json()
        section_response = analysis["sections"][0]["text"]
        stats_response = analysis["sections"][0]["stats"]
        return section_response, stats_response
    else:
        return None, None

# Generate research paper sections
if title and theme:
    abstract_response, abstract_stats = generate_section(title, theme, "abstract")
    introduction_response, introduction_stats = generate_section(title, theme, "introduction")
    literature_review_response, literature_review_stats = generate_section(title, theme, "literature review")
    methodology_response, methodology_stats = generate_section(title, theme, "methodology")

    # Display generated responses
    st.header("Generated Research Paper Sections")
    st.subheader("Abstract")
    st.write(abstract_response)
    st.write("Stats:")
    st.write(f"Confidence Interval: {abstract_stats['confidence_interval']}")
    st.write(f"Significance Level: {abstract_stats['significance_level']}")
    st.subheader("Introduction")
    st.write(introduction_response)
    st.write("Stats:")
    st.write(f"Confidence Interval: {introduction_stats['confidence_interval']}")
    st.write(f"Significance Level: {introduction_stats['significance_level']}")
    st.subheader("Literature Review")
    st.write(literature_review_response)
    st.write("Stats:")
    st.write(f"Confidence Interval: {literature_review_stats['confidence_interval']}")
    st.write(f"Significance Level: {literature_review_stats['significance_level']}")
    st.subheader("Methodology")
    st.write(methodology_response)
    st.write("Stats:")
    st.write(f"Confidence Interval: {methodology_stats['confidence_interval']}")
    st.write(f"Significance Level: {methodology_stats['significance_level']}")
