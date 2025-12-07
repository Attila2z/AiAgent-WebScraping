from WebScraping.tools import (
    fetch_page_html,
    html_to_visible_text,
    extract_google_finance_price,
    FetchError,
)
from WebScraping.agent import create_web_scraping_agent, ask_agent


def run_single_example() -> None:
    """Run a single hard-coded example (META stock price) and show JSON output."""
    url = "https://www.google.com/finance/quote/META:NASDAQ"
    base_task = (
        "Extract the current stock price of META in USD from this Google Finance page. "
        "Ignore any global indices such as DAX, FTSE 100, CAC 40, etc. "
        "Use the price that is clearly associated with Meta Platforms Inc."
    )

    try:
        html = fetch_page_html(url)
    except FetchError as exc:
        print(f"Failed to fetch page: {exc}")
        return

    # Optional debug: save HTML and cleaned text to inspect what the agent sees.
    # with open("debug_meta.html", "w", encoding="utf-8") as f:
    #     f.write(html)

    text = html_to_visible_text(html)

    # with open("debug_meta_text.txt", "w", encoding="utf-8") as f:
    #     f.write(text)

    # Heuristic parser – only for debug/evaluation, not as ground truth.
    candidate_price = extract_google_finance_price(html)
    print("DEBUG – parsed candidate_price from HTML:", candidate_price)

    # Do NOT tell the model this value is "likely" correct; just use the base task.
    task = base_task

    agent = create_web_scraping_agent()
    result = ask_agent(agent, task, url, text)  # dict with JSON structure

    print("Agent JSON result:")
    print(result)
    print("\nHuman-readable answer:")
    print(result.get("answer"))


if __name__ == "__main__":
    run_single_example()
