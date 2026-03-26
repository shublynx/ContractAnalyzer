import pdfplumber

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

# Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_text_chunks(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Embeddings
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_gemini_embeddings(text_list):
    # CHANGED: 'text-embedding-004' -> 'gemini-embedding-001'
    result = genai.embed_content(
        model="models/gemini-embedding-001", 
        content=text_list,
        task_type="retrieval_document",
        output_dimensionality=768  # Explicitly tell it to stay at 768
    )
    return result['embedding'] 
