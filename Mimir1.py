import requests
from bs4 import BeautifulSoup
import csv
import os
import json
import pandas as pd
import streamlit as st

class ResearchPaper:
    def __init__(self):
        self.title = self.get_input("Enter title of Research Paper: ")
        self.theme = self.get_input("Enter theme of Research Paper: ")
        self.abstract = self.generate_text("abstract")
        self.introduction = self.generate_text("introduction")
        self.methodology = self.generate_text("methodology")
        self.results = self.generate_text("results")
        self.conclusion = self.generate_text("conclusion")
        self.sources = []

    #... (rest of the code remains the same)

    def convert_papers_to_txt(self, pdf_dir):
        txt_files = []
        for file in os.listdir(pdf_dir):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(pdf_dir, file)
                txt_path = os.path.join(pdf_dir, file.replace(".pdf", ".txt"))
                self.pdf_to_text(pdf_path, txt_path)
                txt_files.append(txt_path)
        return txt_files

    def pdf_to_text(self, pdf_path, txt_path):
        # Replaced PyPDF2 with Streamlit's built-in PDF rendering
        with open(pdf_path, 'rb') as pdf_file:
            st.image(pdf_file, width=800)  # display the PDF as an image
            # Note: this will not extract text from the PDF, but display it as an image
            # If you need to extract text, you may need to use a different library or approach

    def summarize_txt_files(self, txt_files):
        summaries = []
        for txt_file in txt_files:
            with open(txt_file, 'r') as f:
                text = f.read()
                summary = self.summarize_text(text)
                summaries.append(summary)
        return summaries

    def summarize_text(self, text):
        # Replaced nltk with Streamlit's built-in text processing capabilities
        st.write(text)  # display the text

    def merge_summaries_into_research_paper(self, summaries):
        research_paper_text = ''
        research_paper_text += "Abstract:\n" + self.abstract + "\n\n"
        research_paper_text += "Introduction:\n" + self.introduction + "\n\n"
        research_paper_text += "Methodology:\n" + self.methodology + "\n\n"
        research_paper_text += "Results:\n" + '\n'.join(summaries) + "\n\n"
        research_paper_text += "Conclusion:\n" + self.conclusion + "\n\n"
        research_paper_text += "Sources:\n" + '\n'.join(self.sources) + "\n\n"
        return research_paper_text

    def submit_results(self, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            summary = df.describe().to_string()
            print(f"Results:\n{summary}")
            with open('results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Theme", "Abstract", "Introduction", "Methodology", "Results", "Conclusion", "Sources"])
                writer.writerow([self.title, self.theme, self.abstract, self.introduction, self.methodology, summary, self.conclusion, "\n".join(self.sources)])
            print("Results submitted successfully!")
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")
        except csv.Error as e:
            print(f"Error submitting results: {e}")

def main():
    paper = ResearchPaper()
    try:
        if paper.search_google_scholar():
            print("Search completed successfully")
            paper.download_papers()
            csv_file_path = input("Enter the path of the CSV file: ")
            pdf_dir = input("Enter the path of the PDF directory: ")
            txt_files = paper.convert_papers_to_txt(pdf_dir)
            summaries = paper.summarize_txt_files(txt_files)
            research_paper_text = paper.merge_summaries_into_research_paper(summaries)
            print(research_paper_text)
            paper.submit_results(csv_file_path)
        else:
            print("Search failed")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
