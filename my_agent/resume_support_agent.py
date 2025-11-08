import os
from google.adk.agents.llm_agent import Agent
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
UPLOAD_DIR = os.path.join(BASE_DIR, "backend", "uploads")
LATEST_RESUME_PATH = os.path.join(UPLOAD_DIR, "resume.pdf")


def calculate_match_score(job_description: str, resume_path: str):
    """
    Takes the job description and the resume path to find the cosine difference to get the score.
    The resume's path is stored in the global variable 'LATEST_RESUME_PATH'
    Example: calculate_match_score(job_description_string, LATEST_RESUME_PATH)
    """
    with pdfplumber.open(resume_path) as pdf:
        resume_text = "\n".join([page.extract_text() for page in pdf.pages])
    
    vectorizer = CountVectorizer().fit([job_description, resume_text])
    vectors = vectorizer.transform([job_description, resume_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100
    return round(score)

def get_latest_resume():
    """
    Checks if a resume is stored and returns its path.
    """
    if os.path.exists(LATEST_RESUME_PATH):
        return {"status": "success", "file_path": LATEST_RESUME_PATH}
    return {"status": "error", "message": "No resume stored yet"}

resume_support_agent = Agent(
    model='gemini-2.5-flash',
    name='resume_support_agent',
    description='A helpful assistant for user questions.',
    instruction='''
    You are Resume Support Agent - a specialized assistant for analyzing resumes and matching them with job descriptions.
    
    When a user provides a job description:
    1. First check if a resume exists using get_latest_resume()
    2. If no resume exists, ask the user to upload one
    3. If resume exists, use calculate_match_score() to analyze the match
    4. Provide detailed feedback on the match score and suggestions
    ''',
    tools=[calculate_match_score, get_latest_resume]
)