import json
from pathlib import Path

from WebScraping.tools import (
    fetch_page_html,
    html_to_visible_text,
    FetchError,
)
from WebScraping.agent import (
    create_web_scraping_agent,
    create_verifier_agent,
    ask_agent,
    verify_agent,
)

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

{
    "id": "aapl_price",
    "url": "https://www.google.com/finance/quote/AAPL:NASDAQ",
    "task": (
        "Extract the current stock price of AAPL in USD from this Google Finance page. "
        "Use the price that is clearly associated with Apple Inc."
    ),
},
{
    "id": "msft_summary",
    "url": "https://www.google.com/finance/quote/MSFT:NASDAQ",
    "task": "Summarize the key information about Microsoft (MSFT) from this page.",
},
]


def run_multi_agent_use_cases(output_path: str = "multi_use_cases_outputs.json") -> None:
    """Run all use-cases with an extractor + verifier pipeline and save results to a file."""
    extractor = create_web_scraping_agent()
    verifier = create_verifier_agent()
    results = []

    for case in USE_CASES:
        url = case["url"]
        task = case["task"]

        try:
            html = fetch_page_html(url)
            text = html_to_visible_text(html)

            extractor_output = ask_agent(extractor, task, url, text)
            verifier_output = verify_agent(verifier, extractor_output, task, url, text)

        except FetchError as exc:
            error_output = {
                "answer": f"ERROR: {exc}",
                "extracted_value": None,
                "unit_or_currency": None,
                "confidence": "low",
                "notes": "FetchError while retrieving the page.",
            }
            extractor_output = error_output
            verifier_output = error_output

        results.append(
            {
                "id": case["id"],
                "url": url,
                "task": task,
                "extractor_output": extractor_output,
                "verifier_output": verifier_output,
            }
        )

    Path(output_path).write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    run_multi_agent_use_cases()


