import os
from google.adk.agents.llm_agent import Agent
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
UPLOAD_DIR = os.path.join(BASE_DIR, "backend", "uploads")
LATEST_RESUME_PATH = os.path.join(UPLOAD_DIR, "resume.pdf")


def calculate_match_score(job_description: str):
    """
    Takes the job description and the resume path to find the cosine difference to get the score.
    The resume's path is stored in the global variable 'LATEST_RESUME_PATH'
    Example: calculate_match_score(job_description_string, LATEST_RESUME_PATH)
    """
    with pdfplumber.open(LATEST_RESUME_PATH) as pdf:
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

def read_resume_text():
    """
    Reads and returns the text content of the latest resume.
    """
    if not os.path.exists(LATEST_RESUME_PATH):
        return {"status": "error", "message": "No resume stored yet"}
    
    with pdfplumber.open(LATEST_RESUME_PATH) as pdf:
        resume_text = "\n".join([page.extract_text() for page in pdf.pages])
    
    return {"status": "success", "resume_text": resume_text}

resume_support_agent = Agent(
    model='gemini-2.5-flash',
    name='resume_support_agent',
    description='A helpful assistant for user questions.',
    instruction='''
    You are Resume Support Agent — a specialized assistant for analyzing resumes and matching them with job descriptions and writing cover letters and professional messages.

    Your process:

    1. Always begin by checking if a resume exists using `get_latest_resume()`.
    2. If no resume exists, politely ask the user to upload one before proceeding.
    3. If a resume exists:
    - Use `calculate_match_score()` to analyze how well it matches the given job description.
    - Provide a detailed, structured breakdown of the match score, with specific improvement suggestions.
    - If useful, use `read_resume_text()` to extract more context before commenting.
    4. After you provide your analysis, do **not** stop. 
    - Attempt to extract the **job title** and **company name** from the user’s input.
    - If both are confidently identified, notify the root agent to call the `searcher_agent` with those values.
    - If not, ask the user: “Could you confirm the job title and company name so I can find professionals in that field?”
    5. Always confirm completion of your resume analysis before moving on to the search step.
    6. Never invent job or company names — only extract or confirm them.
    7. Always check again that a resume exists before proceeding with any search.
    8. If asked for a personalized message or cover letter, make it short and sweet. Run read_resume_text first and based on that the First paragraph should be why you are excited to work at the company.
        Second paragraph should be why you're a good fit. Do not use em dashes and messages to professionals should not be more than 5 lines.

    IMP: If you think something is out of your functionality, transfer to root_agent and let it figure it out.
    ''',
    tools=[calculate_match_score, get_latest_resume, read_resume_text]
)