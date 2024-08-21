from bs4 import BeautifulSoup
import requests

def extract_questions_from_survey(url):
    """
    Extracts survey questions from the given URL.

    Args:
        url (str): The URL of the survey page.

    Returns:
        list: A list of questions found on the survey page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    questions = []
    
    # Example: Find all labels associated with text input fields
    for label in soup.find_all('label'):
        associated_input = label.find_next('input')
        if associated_input and associated_input.get('type') == 'text':
            question_text = label.get_text(strip=True)
            questions.append(question_text)
    
    # Example: Find all fieldsets with legends (often used for groups of radio buttons)
    for fieldset in soup.find_all('fieldset'):
        legend = fieldset.find('legend')
        if legend:
            question_text = legend.get_text(strip=True)
            choices = [label.get_text(strip=True) for label in fieldset.find_all('label')]
            questions.append(f"{question_text} (Choices: {', '.join(choices)})")
    
    return questions
