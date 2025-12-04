# WebScraping/evaluate.py
import json
from pathlib import Path

from WebScraping.tools import fetch_page_html, html_to_visible_text
from WebScraping.agent import create_web_scraping_agent, ask_agent

# Define several tasks to show your agent works on more than one page / question.
USE_CASES = [
    {
        "id": "meta_price",
        "url": "https://www.google.com/finance/quote/META:NASDAQ",
        "task": "Extract the current stock price of META in USD.",
    },
    # Add more examples, e.g. another stock or another website:
    # {
    #     "id": "some_other_case",
    #     "url": "...",
    #     "task": "...",
    # },
]


def run_use_cases(output_path: str = "use_cases_outputs.json") -> None:
    agent = create_web_scraping_agent()
    results = []

    for case in USE_CASES:
        html = fetch_page_html(case["url"])
        text = html_to_visible_text(html)
        answer = ask_agent(agent, case["task"], case["url"], text)

        results.append(
            {
                "id": case["id"],
                "url": case["url"],
                "task": case["task"],
                "answer": answer,
            }
        )

    Path(output_path).write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    run_use_cases()
