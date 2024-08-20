import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
from modules.rag_pipeline import run_rag_pipeline
from modules.data_processing import load_and_partition_pdf
from modules.vector_store import initialize_vector_store, add_documents_to_vector_store
from modules.web_scraping import add_website_to_vector_store
from modules.survey_creation import SurveyManager
from modules.survey_answering import SurveyAnswerer
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize the vector store and retriever
retriever, store = initialize_vector_store()

# Initialize survey manager and answerer
survey_manager = SurveyManager()
survey_answerer = SurveyAnswerer(retriever)

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
        add_documents_to_vector_store(
            retriever, 
            store, 
            [e.text for e in text_elements], 
            [e.text for e in table_elements], 
            text_summaries=[e.text for e in text_elements], 
            table_summaries=[e.text for e in table_elements]
        )

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

@app.route('/create-survey', methods=['GET', 'POST'])
def create_survey():
    if request.method == 'POST':
        title = request.form['survey-title']
        questions = [request.form[key] for key in request.form if key.startswith('question')]
        survey = survey_manager.create_survey(title)
        for question in questions:
            survey.add_question(question)
        survey_answerer.add_survey(survey)
        return redirect(url_for('survey_results_list'))
    return render_template('survey.html')

@app.route('/survey-results')
def survey_results_list():
    surveys = survey_manager.get_all_surveys()
    return render_template('survey_results_list.html', surveys=surveys)

@app.route('/survey-results/<survey_title>')
def survey_results(survey_title):
    answered_survey = survey_answerer.answer_survey(survey_title)
    return render_template('survey_results.html', survey=answered_survey)

if __name__ == '__main__':
    app.run(debug=True)
