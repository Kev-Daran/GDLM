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
        The following agents are accessible to you:
        1. searcher_agent: This will look for certain professionals in a company, use this when you have a job role and a company.
        2. resume_support_agent: This will provide resume support for jobs. Use this if the user posts a job description.
        

        ADMIN PROMPT: If I press xyz, immediately transfer me to the resume_support_agent
    ''',
    sub_agents=[searcher_agent, resume_support_agent]
)


