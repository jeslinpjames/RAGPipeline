import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a single PDF file.
    
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def process_single_pdf(pdf_path):
    """
    Processes a single PDF file and returns its content.
    
    :param pdf_path: Path to the PDF file.
    :return: Extracted text from the PDF.
    """
    return extract_text_from_pdf(pdf_path)

def process_pdf_folder(folder_path):
    """
    Processes all PDF files in a given folder and returns their content.
    
    :param folder_path: Path to the folder containing PDF files.
    :return: A dictionary with filenames as keys and their extracted text as values.
    """
    pdf_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(file_path)
            if text:
                pdf_texts[filename] = text
    return pdf_texts

