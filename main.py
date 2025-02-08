import fitz  # PyMuPDF
import openai
import os
import re
from dotenv import load_dotenv

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to extract text from PDF per page
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages_text = [page.get_text("text") for page in doc]
    return pages_text

# Function to send text to OpenAI for analysis
def analyze_text(text):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    model = "gpt-4"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Identify all critical legal clauses in the following text. Highlight clauses related to salaries, penalties, fees, contractual obligations, liability, dispute resolution, and any terms that could impact financial or legal responsibilities. Return only the exact sentences that should be highlighted."},
                {"role": "user", "content": text}
            ]
        )
        sentences = response.choices[0].message.content.split(". ")
        return [s.strip() for s in sentences if len(s.split()) > 3]  # Ignore very short highlights
    except openai.RateLimitError:
        print("Rate limit exceeded. Switching to gpt-3.5-turbo...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Identify all critical legal clauses in the following text. Highlight clauses related to salaries, penalties, fees, contractual obligations, liability, dispute resolution, any terms that could impact financial or legal responsibilities, or anything related to this. If a sentence contains any of the previous, it MUST be highlighted. Return only the exact sentences that should be highlighted."},
                {"role": "user", "content": text}
            ]
        )
        sentences = response.choices[0].message.content.split(". ")
        return [s.strip() for s in sentences if len(s.split()) > 5]

# Function to highlight sentences in PDF
def highlight_text_in_pdf(pdf_path, output_path, risky_sentences_per_page):
    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        text_lower = text.lower()
        for sentence in risky_sentences_per_page[page_num]:
            sentence = sentence.strip()
            sentence_lower = sentence.lower()
            
            # Try exact match first
            areas = page.search_for(sentence)
            
            # If exact match fails, find partial match with regex
            if not areas:
                sentence_pattern = re.escape(sentence[:15])  # Match first 15 characters
                match = re.search(sentence_pattern, text_lower)
                if match:
                    areas = [fitz.Rect(match.start(), match.end(), match.start() + 100, match.end() + 10)]
            
            for area in areas:
                highlight = page.add_highlight_annot(area)
                highlight.set_colors(stroke=(1, 0.5, 0))  # Set orange color
                highlight.update()
    doc.save(output_path)
    print(f"Processed PDF saved as: {output_path}")

# Main execution
if __name__ == "__main__":
    input_pdf = "input.pdf"  # File name
    output_pdf = "legallens.pdf"
    
    print("Extracting text from PDF...")
    pages_text = extract_text_from_pdf(input_pdf)
    
    print("Analyzing text with OpenAI per page...")
    risky_sentences_per_page = [analyze_text(text) for text in pages_text]
    
    print("Highlighting risky sentences in PDF...")
    highlight_text_in_pdf(input_pdf, output_pdf, risky_sentences_per_page)
