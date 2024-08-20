from typing import List, Dict

class Survey:
    def __init__(self, title: str):
        self.title = title
        self.questions = []
        self.answers = {}

    def add_question(self, question: str):
        self.questions.append(question)

    def add_answer(self, question: str, answer: str):
        self.answers[question] = answer

    def get_questions(self) -> List[str]:
        return self.questions

    def get_answers(self) -> Dict[str, str]:
        return self.answers

    def __repr__(self):
        return f"Survey(title={self.title}, questions={len(self.questions)}, answers={len(self.answers)})"


class SurveyManager:
    def __init__(self):
        self.surveys: Dict[str, Survey] = {}

    def create_survey(self, title: str) -> Survey:
        if title in self.surveys:
            raise ValueError(f"Survey with title '{title}' already exists.")
        survey = Survey(title)
        self.surveys[title] = survey
        return survey

    def get_survey(self, title: str) -> Survey:
        return self.surveys.get(title, None)

    def get_all_surveys(self):
        return list(self.surveys.values())

    def list_surveys(self) -> List[str]:
        return list(self.surveys.keys())

    def __repr__(self):
        return f"SurveyManager(surveys={len(self.surveys)})"


