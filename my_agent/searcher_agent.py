import requests
import os
from google.adk.agents.llm_agent import Agent


def find_relevant_people(company : str, role : str, country : str = "India"):
    """
    Uses Google Search API to find people related to a company and role.
    Example: find_relevant_people("Google", "Data Scientist", "India")
    """

    query = f'site:linkedin.com/in "{role.strip()}" "{company.strip()}" "{country.strip()}"email OR contact'
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



searcher_agent = Agent(
    model='gemini-2.5-flash',
    name='searcher_agent',
    description='Finds people and contact info for specific roles in a company.',
    instruction='''
    You are Searcher Agent — a specialized retrieval assistant.

    Your role is to find and return professional candidate data based on specific search criteria such as job role, skills, and country.

    Follow these rules carefully:

    1. Always return results in a standardized JSON format:
    {
        {
        "name": "<full_name>",
        "title": "<current_title_or_role>",
        "location": "<city_or_country>",
        "experience_years": <integer>,
        "skills": ["<skill1>", "<skill2>", ...],
        "linkedin_url": "<url>",
        "email": "<email_if_available>"
        },
        ...
    }

    2. Always filter candidates by the specified **country** if provided.

    3. If information such as email or experience is unavailable, omit the field instead of leaving it blank.

    4. Limit to a reasonable number of results (typically 5–10).

    5. Ensure names and roles are clearly human-readable (no placeholder or null values).

    6. Do not generate fake or random data. Let the user know if the API is unavailable.

    7. Your output must be clean JSON — no text outside the JSON block.
    ''',
    tools=[find_relevant_people]
)
