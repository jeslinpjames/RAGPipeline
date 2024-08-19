import os
from flask import Flask, request, render_template, jsonify
from modules.rag_pipeline import run_rag_pipeline
from modules.data_processing import load_and_partition_pdf
from modules.vector_store import initialize_vector_store, add_documents_to_vector_store
from modules.web_scraping import add_website_to_vector_store
from modules.llm_interface import send_prompt
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
def summarize_element(element):
    prompt_template = """
    You are a data analyst specialized in interpreting and summarizing tables. The following content is a table extracted from a document. 
    Please provide a concise summary that highlights the key insights, trends, or important points from this table. Your summary should be 
    understandable to someone without access to the table and should include any notable comparisons, patterns, or outliers.
    
    Table:
    {element}
    
    Summary:
    """
    prompt = prompt_template.format(element=element)
    response = send_prompt(prompt)
    return response

def batch_summarize_tables(elements):
    summaries = []
    for element in elements:
        summary = summarize_element(element)
        summaries.append(summary)
    return summaries

# Initialize the vector store and retriever
retriever, store = initialize_vector_store()

uploaded_pdfs = []
uploaded_websites = []

@app.route('/')
def home():
    return render_template('index.html', pdfs=uploaded_pdfs, websites=uploaded_websites)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify(success=False, message="No file part"), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify(success=False, message="No selected file"), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Simulate processing
        time.sleep(1)

        table_elements, text_elements = load_and_partition_pdf(file_path)
        table_summaries = batch_summarize_tables([e.text for e in table_elements])
        add_documents_to_vector_store(retriever, store, [e.text for e in text_elements], [e.text for e in table_elements], [e.text for e in text_elements], table_summaries)

        uploaded_pdfs.append(filename)
        return jsonify(success=True, pdf=filename)

@app.route('/add_website', methods=['POST'])
def add_website():
    url = request.form['url']
    
    # Simulate processing
    time.sleep(1)

    add_website_to_vector_store(url, retriever, store)
    uploaded_websites.append(url)
    return jsonify(success=True, website=url)

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form['question']
    answer = run_rag_pipeline(question, retriever)
    return jsonify(answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
