import streamlit as st
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Initialize the model and tokenizer
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize the text generation pipeline
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

class ResearchPaper:
    def __init__(self):
        self.title = ""
        self.theme = ""
        self.sections = ["Abstract", "Introduction", "Methodology", "Results", "Conclusions", "Sources"]

    def _get_user_input(self, prompt: str) -> str:
        user_input = st.text_input(prompt)
        return user_input

    def display_paper_details(self) -> None:
        st.write(f"Research Paper: {self.title} - {self.theme}")

    def generate_section(self, section_name: str) -> str:
        prompt = f"Generate a {section_name} for a research paper on {self.title} and {self.theme}."
        response = generator(prompt, max_length=512, num_return_sequences=1)
        return response[0]['generated_text']

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
        self.generate_paper()

if __name__ == "__main__":
    st.title("Research Paper Generator")
    research_paper = ResearchPaper()
    research_paper.run()
