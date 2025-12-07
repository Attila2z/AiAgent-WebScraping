from WebScraping.tools import (
    fetch_page_html,
    html_to_visible_text,
    FetchError,
)
from WebScraping.agent import create_web_scraping_agent, ask_agent


def run_single_example() -> None:
    """Run a single hard-coded example (META stock price) and show JSON output."""
    url = "https://www.google.com/finance/quote/META:NASDAQ"
    task = (
        "Extract the current stock price of META in USD from this Google Finance page. "
        "Ignore any global indices such as DAX, FTSE 100, CAC 40, etc. "
        "Use the price that is clearly associated with Meta Platforms Inc."
    )

    try:
        html = fetch_page_html(url)
    except FetchError as exc:
        print(f"Failed to fetch page: {exc}")
        return

    text = html_to_visible_text(html)

    agent = create_web_scraping_agent()
    result = ask_agent(agent, task, url, text)  # dict with JSON structure

    print("Agent JSON result:")
    print(result)
    print("\nHuman-readable answer:")
    print(result.get("answer"))


if __name__ == "__main__":
    run_single_example()
