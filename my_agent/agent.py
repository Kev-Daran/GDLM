from google.adk.agents.llm_agent import Agent
from .searcher_agent import searcher_agent
from .resume_support_agent import resume_support_agent

def get_current_time(city : str) -> dict:
    """ Returns the current time in a specified city """
    return {"status" : "success",
            "city" : city,
            "time" : "10:30 AM"}


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=''' 
        You are the orchestration layer of a multi-agent system.

        Agents available:
        1. resume_support_agent — Analyzes job descriptions and compares them to the user’s resume to determine match quality and draft messages for professionals.
        2. searcher_agent — Searches for professionals or insights about a specific role and company.

        Primary workflow:
        - When a user provides a job description or requests a match, FIRST call `resume_support_agent` to generate the resume match analysis.
        - After receiving that response, automatically call `searcher_agent` to gather company and role insights, but only if the job title and company name can be extracted.
        - If you cannot confidently extract the job title or company name, ask the user to clarify before calling `searcher_agent`.

        Always display the results clearly:
        1. First show the resume match analysis.
        2. Then show insights from the searcher agent under a separate section titled “Company & Role Insights”.
    ''',
    sub_agents=[searcher_agent, resume_support_agent]
)


