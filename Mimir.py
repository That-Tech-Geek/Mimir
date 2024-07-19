# user inputs title and theme of paper
# model searches scholar.google.com for similar papers, and asks the user if his title and themes are similar to any of them
# if user says no, continue the process:
	# 1. Abstract
	# 2. Introduction
	# 3. Methodology
	# 4. Results
	# 5. Conclusions
	# 6. Sources
# Order of Search: 231-user intervenes to provide research data if the model cannot find it anywhere else-45-paper achieves user validation-6

import requests
from bs4 import BeautifulSoup
import llama
import streamlit as st

class ResearchPaper:
    def __init__(self):
        self.title = ""
        self.theme = ""
        self.sections = ["Abstract", "Introduction", "Methodology", "Results", "Conclusions", "Sources"]
        self.llama_api_key = "YOUR_LLAMA_API_KEY"
        self.llama_model = llama.LLaMA(self.llama_api_key)

    def _get_user_input(self, prompt: str) -> str:
        user_input = st.text_input(prompt)
        return user_input

    def display_paper_details(self) -> None:
        st.write(f"Research Paper: {self.title} - {self.theme}")

    def search_google_scholar(self) -> list:
        url = f"https://scholar.google.com/scholar?q={self.title}+{self.theme}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(response.content, 'html.parser')
            similar_papers = [result.find('h3', class_='gs_rt').text for result in soup.find_all('div', class_='gs_r')]
            return similar_papers
        except requests.exceptions.RequestException as e:
            st.error(f"Error searching Google Scholar: {e}")
            return []

    def generate_section(self, section_name: str) -> str:
        prompt = f"Generate a {section_name} for a research paper on {self.title} and {self.theme}."
        response = self.llama_model.ask(prompt)
        return response.answer

    def generate_paper(self) -> None:
        st.write("Generating research paper...")
        for section in self.sections:
            section_content = self.generate_section(section)
            st.write(f"{section}:")
            st.write(section_content)
            st.write()

    def run(self) -> None:
        self.title = self._get_user_input("Enter title of Research Paper: ")
        self.theme = self._get_user_input("Enter theme of Research Paper: ")
        self.display_paper_details()
        similar_papers = self.search_google_scholar()
        if similar_papers:
            st.write("Similar papers found:")
            for paper in similar_papers:
                st.write(paper)
            user_response = st.selectbox("Is your paper similar to any of these?", ["Yes", "No"])
            if user_response == "Yes":
                st.write("Please refine your title and theme.")
                return
        self.generate_paper()

if __name__ == "__main__":
    st.title("Research Paper Generator")
    research_paper = ResearchPaper()
    research_paper.run()
