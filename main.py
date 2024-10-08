# Import necessary modules
from modules.data_processing import load_and_partition_pdf
from modules.vector_store import initialize_vector_store, add_documents_to_vector_store
from modules.llm_interface import send_prompt
from modules.rag_pipeline import run_rag_pipeline
from modules.web_scraping import add_website_to_vector_store  

# 1. Load and process the PDF
pdf_filename = "PDFs/infosys-esg-report-2022-23.pdf"  # Replace with your PDF file name
table_elements, text_elements = load_and_partition_pdf(pdf_filename)

# 2. Summarize the table elements only
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

# Summarize only tables
table_summaries = batch_summarize_tables([e.text for e in table_elements])

# 3. Initialize the vector store and add the documents
retriever, store = initialize_vector_store()

# Add the documents to the vector store, without summarizing text elements
add_documents_to_vector_store(
    retriever, 
    store, 
    [e.text for e in text_elements],  # Original text elements, without summarization
    [e.text for e in table_elements],  # Original table elements
    text_summaries=[e.text for e in text_elements],  # Use original text instead of summaries
    table_summaries=table_summaries  # Use summarized tables
)

# 4. Add website content to the vector store
url = "https://en.wikipedia.org/wiki/Llama_(language_model)"  # Replace with the actual website URL
add_website_to_vector_store(url, retriever, store)

# 5. Ask a question and pass the retriever to the pipeline
question = "What is ESG?"
answer = run_rag_pipeline(question, retriever)

# 6. Print the answer
print("Answer:", answer)
