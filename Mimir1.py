import requests
from bs4 import BeautifulSoup
import csv
import os
import json
import pandas as pd
import PyPDF2

class ResearchPaper:
    def __init__(self):
        self.title = input("Enter title of Research Paper: ")
        self.theme = input("Enter theme of Research Paper: ")
        self.abstract = self.generate_text("abstract")
        self.introduction = self.generate_text("introduction")
        self.methodology = self.generate_text("methodology")
        self.results = self.generate_text("results")
        self.conclusion = self.generate_text("conclusion")
        self.sources = self.generate_text("sources")



    def generate_text(self, section):
        api_key = input("enter api key of user: ")
        url = f"https://api.llama.ai/generate"
        payload = {
            "prompt": f"Generate a {section} for a research paper on {self.title} and {self.theme}",
            "max_tokens": 1000000,
            "temperature": 5
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["text"]
        except requests.exceptions.RequestException as e:
            print(f"Error generating text: {e}")
            return ""

    def __init__(self):
        while True:
            self.title = input("Enter title of Research Paper: ")
            if self.title.strip()!= "":
                break
            else:
                print("Title cannot be empty. Please try again.")

        while True:
            self.theme = input("Enter theme of Research Paper: ")
            if self.theme.strip()!= "":
                break
            else:
                print("Theme cannot be empty. Please try again.")
    def search_google_scholar(self):
        url = f"https://scholar.google.com/scholar?q={self.title}+{self.theme}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='gs_r')
            if results:
                print("Similar papers found on Google Scholar:")
                for result in results:
                    print(result.text)
                return True
            else:
                print("No similar papers found on Google Scholar. Retry with a new Topic and theme.")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error searching Google Scholar: {e}")
            return False

    def download_papers(self):
        url = f"https://scholar.google.com/scholar?q={self.title}+{self.theme}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='gs_r')
            if results:
                for result in results:
                    pdf_links = result.find_all('a', href=True)
                    for link in pdf_links:
                        if 'pdf' in link['href']:
                            pdf_url = link['href']
                            print(f"Downloading PDF from {pdf_url}...")
                            try:
                                response = requests.get(pdf_url, stream=True)
                                response.raise_for_status()
                                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                                pdf_path = os.path.join(desktop_path, f"{self.title}_{self.theme}.pdf")
                                with open(pdf_path, 'wb') as f:
                                    for chunk in response.iter_content(1024):
                                        f.write(chunk)
                                print("PDF downloaded successfully!")
                                self.sources.append(pdf_url)
                                break
                            except requests.exceptions.RequestException as e:
                                print(f"Error downloading PDF: {e}")
                                continue
            else:
                print("No PDF found. Please try again.")
        except requests.exceptions.RequestException as e:
            print(f"Error searching Google Scholar: {e}")

    def convert_papers_to_txt(self):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        pdf_path = os.path.join(desktop_path, f"{self.title}_{self.theme}.pdf")
        try:
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            txt_content = ""
            for page in pdf_content:
                txt_content += page.extractText()
            with open(f"{self.title}_{self.theme}.txt", 'w') as f:
                f.write(txt_content)
            print("PDF converted to TXT successfully!")
        except Exception as e:
            print(f"Error converting PDF to TXT: {e}")

    def pdf_to_text(self, pdf_path, txt_path):
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

    def summarize_txt_files(self, txt_files):
        summaries = []
        for txt_file in txt_files:
            with open(txt_file, 'r') as f:
                text = f.read()
                summary = self.summarize_text(text)
                summaries.append(summary)
        return summaries

    def summarize_text(self, text):
        # implement your own text summarization algorithm here
        # for example, you can use the NLTK library
        import nltk
        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(text)
        summary = '.join(sentences[:5])  # summarize the first 5 sentences'
        return summary

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
        
import os
import PyPDF2
def convert_pdfs_to_txt(self, pdf_dir):
    txt_files = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file)
            txt_path = os.path.join(pdf_dir, file.replace(".pdf", ".txt"))
            self.pdf_to_text(pdf_path, txt_path)
            txt_files.append(txt_path)
    return txt_files

def pdf_to_text(self, pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def summarize_txt_files(self, txt_files):
    summaries = []
    for txt_file in txt_files:
        with open(txt_file, 'r') as f:
            text = f.read()
            summary = self.summarize_text(text)
            summaries.append(summary)
            return summaries

def summarize_text(self, text):
        # implement your own text summarization algorithm here
        # for example, you can use the NLTK library
    import nltk
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text)
    summary = '.join(sentences[:5])  # summarize the first 5 sentences'
    return summary

def merge_summaries_into_research_paper(self, summaries):
    research_paper_text = ''
    research_paper_text += "Abstract:\n" + self.abstract + "\n\n"
    research_paper_text += "Introduction:\n" + self.introduction + "\n\n"
    research_paper_text += "Methodology:\n" + self.methodology + "\n\n"
    research_paper_text += "Results:\n" + '\n'.join(summaries) + "\n\n"
    research_paper_text += "Conclusion:\n" + self.conclusion + "\n\n"
    research_paper_text += "Sources:\n" + '\n'.join(self.sources) + "\n\n"
    return research_paper_text

def main():
    paper = ResearchPaper()
    try:
        if paper.search_google_scholar():
            print("Search completed successfully")
            paper.download_papers()
            csv_file_path = input("Enter the path of the CSV file: ")
            pdf_dir = input("Enter the path of the PDF directory: ")
            paper.submit_results(csv_file_path, pdf_dir)
        else:
            print("Search failed")
    except Exception as e:
        print(f"An error occurred: {e}")