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

    def update_question(self, index: int, question: str):
        if 0 <= index < len(self.questions):
            self.questions[index] = question
        else:
            raise IndexError("Question index out of range.")

    def remove_question(self, index: int):
        if 0 <= index < len(self.questions):
            self.questions.pop(index)
        else:
            raise IndexError("Question index out of range.")

    def __repr__(self):
        return f"Survey(title={self.title}, questions={len(self.questions)}, answers={len(self.answers)})"

class SurveyManager:
    def __init__(self):
        self.surveys: Dict[str, Survey] = {}

    def create_survey(self, title: str) -> Survey:
        normalized_title = title.strip().lower()
        if normalized_title in self.surveys:
            raise ValueError(f"Survey with title '{title}' already exists.")
        survey = Survey(title)
        self.surveys[normalized_title] = survey
        return survey

    def get_survey(self, title: str) -> Survey:
        normalized_title = title.strip().lower()
        return self.surveys.get(normalized_title, None)

    def get_all_surveys(self):
        return list(self.surveys.values())

    def edit_survey(self, title: str, questions: List[str]):
        normalized_title = title.strip().lower()
        if normalized_title in self.surveys:
            survey = self.surveys[normalized_title]
            survey.set_questions(questions)
        else:
            raise ValueError(f"Survey with title '{title}' does not exist.")

    def delete_survey(self, title: str):
        normalized_title = title.strip().lower()
        if normalized_title in self.surveys:
            del self.surveys[normalized_title]
        else:
            raise ValueError(f"Survey with title '{title}' does not exist.")

    def list_surveys(self) -> List[str]:
        return list(self.surveys.keys())

    def __repr__(self):
        return f"SurveyManager(surveys={len(self.surveys)})"
