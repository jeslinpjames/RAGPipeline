from modules.rag_pipeline import run_rag_pipeline

class SurveyAnswerer:
    def __init__(self, retriever):
        self.retriever = retriever
        self.surveys = {}
        self.answers_cache = {}  # Cache for storing generated answers

    def add_survey(self, survey):
        self.surveys[survey.title] = survey

    def answer_survey(self, survey_title):
        # Check if answers are already cached
        if survey_title in self.answers_cache:
            return self.answers_cache[survey_title]
        
        # If not cached, generate answers
        survey = self.surveys.get(survey_title)
        if not survey:
            return None

        for question in survey.get_questions():
            answer = run_rag_pipeline(question, self.retriever)
            survey.add_answer(question, answer)
        
        # Cache the answers
        self.answers_cache[survey_title] = survey
        return survey
