import json

# Try both import styles so it works with different AutoGen setups.
try:
    # AutoGen 0.3.x style
    from autogen import AssistantAgent  # type: ignore
except ImportError:  # pragma: no cover
    # Newer AgentChat layout
    from autogen_agentchat.agents import AssistantAgent  # type: ignore

from config import LLM_CONFIG

SYSTEM_MESSAGE = """You are a WebScrapingAgent.

You will receive:
1) A natural-language task from the user.
2) The URL of a webpage.
3) The cleaned text content of that webpage.

Your job:
- Read the page content.
- Extract only the information needed to solve the task.
- Be concise and precise.
- If the information is missing or unclear, say that explicitly instead of guessing.

For Google Finance pages:
- They often show global indices like DAX, FTSE 100, CAC 40, etc. at the top.
- You MUST ignore those index values when asked for a stock price.
- Use the price that is clearly associated with the specific company (e.g. Meta Platforms Inc in the META card).

Always respond in valid JSON with the following structure and nothing else:

{
  "answer": "<short natural-language answer>",
  "extracted_value": "<if there is a key numeric or string value, put it here, otherwise null>",
  "unit_or_currency": "<e.g. USD or null>",
  "confidence": "<low|medium|high>",
  "notes": "<optional extra info or null>"
}
"""


def create_web_scraping_agent() -> AssistantAgent:
    """Create and configure the AutoGen assistant agent."""
    return AssistantAgent(
        name="web_scraper",
        llm_config=LLM_CONFIG,
        system_message=SYSTEM_MESSAGE,
    )


def _normalize_agent_output(raw_text: str) -> dict:
    """Parse the agent's reply as JSON and normalize it to the expected schema.

    If JSON parsing fails, return a fallback dict where 'answer' contains the raw text.
    """
    try:
        data = json.loads(raw_text)
        if not isinstance(data, dict):
            data = {"answer": data}
    except json.JSONDecodeError:
        # Fallback: treat the entire reply as the 'answer' field.
        return {
            "answer": raw_text,
            "extracted_value": None,
            "unit_or_currency": None,
            "confidence": "low",
            "notes": "LLM did not return valid JSON; raw content stored in 'answer'.",
        }

    return {
        "answer": data.get("answer", raw_text),
        "extracted_value": data.get("extracted_value"),
        "unit_or_currency": data.get("unit_or_currency"),
        "confidence": data.get("confidence", "medium"),
        "notes": data.get("notes"),
    }


def ask_agent(agent: AssistantAgent, task: str, url: str, page_text: str) -> dict:
    """Send one request to the agent and return its answer as a dict (JSON structure).

    Args:
        agent: The AssistantAgent instance.
        task:  Natural-language description of what to extract.
        url:   Page URL (for context only).
        page_text: Cleaned text content of the page.

    Returns:
        A dictionary with keys:
        - answer
        - extracted_value
        - unit_or_currency
        - confidence
        - notes
    """
    user_message = f"""Task:
{task}

Page URL:
{url}

Page content:
{page_text}
"""

    reply = agent.generate_reply(
        messages=[{"role": "user", "content": user_message}]
    )

    # Depending on AutoGen version, reply may be a dict or a plain string.
    if isinstance(reply, dict):
        raw_text = str(reply.get("content", "")).strip()
    else:
        raw_text = str(reply).strip()

    return _normalize_agent_output(raw_text)
