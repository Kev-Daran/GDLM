import os
from google.adk.agents.llm_agent import Agent
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber

LATEST_RESUME_PATH = 'E:\GDLM\my_agent\Dev_Karan_Suresh_CV.pdf'


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
    if os.path.exists(LATEST_RESUME_PATH):
        return {"status": "success", "file_path": LATEST_RESUME_PATH}
    return {"status": "error", "message": "No resume stored yet"}

resume_support_agent = Agent(
    model='gemini-2.5-flash',
    name='resume_support_agent',
    description='A helpful assistant for user questions.',
    instruction='''
    You are Resume Support Agent - a specialized assistant for storing, analyzing, and improving resumes.
    ''',
    tools=[calculate_match_score, get_latest_resume]
)