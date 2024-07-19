import requests
import llama
import streamlit as st
import json

class ResearchPaper:
    def __init__(self):
        self.title = ""
        self.theme = ""
        self.sections = ["Abstract", "Introduction", "Methodology", "Results", "Conclusions", "Sources"]
        self.llama_model = llama.LLaMA(apikey)

    def _get_user_input(self, prompt: str) -> str:
        user_input = st.text_input(prompt)
        return user_input

    def display_paper_details(self) -> None:
        st.write(f"Research Paper: {self.title} - {self.theme}")

    def search_google_scholar(self) -> list:
        api_url = f"https://serpstack.com/search?access_key=YOUR_SERPSTACK_API_KEY&q={self.title}+{self.theme}&tbm=sch"
        response = requests.get(api_url)
        response.raise_for_status()
        search_results = response.json()
        similar_papers = [result["title"] for result in search_results["organic_results"]]
        return similar_papers

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
