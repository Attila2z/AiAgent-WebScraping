import json
from pathlib import Path

from WebScraping.tools import (
    fetch_page_html,
    html_to_visible_text,
    extract_google_finance_price,
    FetchError,
)
from WebScraping.agent import create_web_scraping_agent, ask_agent

# Define several use-cases for the agent.
USE_CASES = [
    {
        "id": "meta_price",
        "url": "https://www.google.com/finance/quote/META:NASDAQ",
        "task": (
            "Extract the current stock price of META in USD from this Google Finance page. "
            "Ignore any global indices such as DAX, FTSE 100, CAC 40, etc. "
            "Use the price that is clearly associated with Meta Platforms Inc."
        ),
    },
    {
        "id": "meta_summary",
        "url": "https://www.google.com/finance/quote/META:NASDAQ",
        "task": "Summarize the key information about META from this page.",
    },
    # You can add more cases here if you want.
]


def run_use_cases(output_path: str = "use_cases_outputs.json") -> None:
    """Run all use-cases and save prompts + JSON outputs to a file."""
    agent = create_web_scraping_agent()
    results = []

    for case in USE_CASES:
        url = case["url"]
        task = case["task"]

        try:
            html = fetch_page_html(url)
            text = html_to_visible_text(html)
            parsed_price = extract_google_finance_price(html)
            agent_output = ask_agent(agent, task, url, text)
        except FetchError as exc:
            agent_output = {
                "answer": f"ERROR: {exc}",
                "extracted_value": None,
                "unit_or_currency": None,
                "confidence": "low",
                "notes": "FetchError while retrieving the page.",
            }
            parsed_price = None

        results.append(
            {
                "id": case["id"],
                "url": url,
                "task": task,                     # input / prompt
                "agent_output": agent_output,     # JSON structure from agent
                "parsed_price_from_html": parsed_price,  # heuristic baseline (may be None)
            }
        )

    Path(output_path).write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    run_use_cases()
