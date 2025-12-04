from autogen import AssistantAgent, UserProxyAgent
from config import LLM_CONFIG

SYSTEM_MESSAGE = """
ROLW:
You are a WebScrapingAgent

You will receive:
1, A natural-language task from the user.
2, The URL of a webpage.
3, The cleaned text content of that webpage.

Your job:
- Read the page content.
- Extract  only the information needed to solve the task.
- Be concise and precise.
- If the information is missing or unclear, say that explicitly instead of guessing.
"""

def create_web_scraping_agent() -> AssistantAgent:
    """Create and configure the Autogen Assistant agent."""
    return AssistantAgent(
        name="web_scraper",
        llm_config=LLM_CONFIG,
        system_message=SYSTEM_MESSAGE,
    )
def ask_agent(agent: AssistantAgent, task: str, url: str, page_text: str) -> str:
    """
    Send a single-turn task to the agent amd return its answer as a string.
    We package the task + page content into one user message.
    """
    user_message = f"""
Task:
{task}

Page URL:
{url}

Page content:
{page_text}
"""
    # Depending on AutoGen version, generate_reply may return a dict or str.
    reply = agent.generate_reply(
        messages=[{"role": "user", "content": user_message}]
    )

    if isinstance(reply, dict):
        return reply.get("content", "")
    return str(reply)