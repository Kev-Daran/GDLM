from google.adk.agents.llm_agent import Agent
import requests
import os

def get_current_time(city : str) -> dict:
    """ Returns the current time in a specified city """
    return {"status" : "success",
            "city" : city,
            "time" : "10:30 AM"}

def find_relevant_people(company : str, role : str):
    """
    Uses Google Search API to find people related to a company and role.
    Example: find_relevant_people("Google", "Data Scientist")
    """

    query = f'site:linkedin.com/in "{role.strip()}" "{company.strip()}" email OR contact'
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={os.getenv('GOOGLE_SEARCH_KEY')}&cx={os.getenv('SEARCH_ENGINE_ID')}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        people = []

        for item in data.get("items", []):
            people.append({
                "name": item.get("title"),
                "snippet": item.get("snippet"),
                "link" : item.get("link")
            })
        return {
            "status" : "success",
            "company" : company,
            "role" : role,
            "results" : people
        }

    except Exception as e:
        return {
            "status" : "error",
            "message" : str(e)
        }

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )

root_agent = Agent(
    model='gemini-2.5-flash',
    name='searcher_agent',
    description='Finds people and contact info for specific roles in a company.',
    instruction='Search the web for professionals working at the specified company and role, and return their names, profiles, and snippets',
    tools=[find_relevant_people]
)
