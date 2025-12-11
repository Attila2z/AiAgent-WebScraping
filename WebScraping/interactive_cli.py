from WebScraping.tools import fetch_page_html, html_to_visible_text, FetchError
from WebScraping.agent import create_web_scraping_agent, ask_agent


def build_url(ticker: str) -> str:
    # Very simple: assume NASDAQ and upper-case ticker
    ticker = ticker.strip().upper()
    return f"https://www.google.com/finance/quote/{ticker}:NASDAQ"


def main() -> None:
    ticker = input("Enter stock ticker (e.g. META, AAPL, MSFT): ").strip()
    if not ticker:
        print("No ticker given, exiting.")
        return

    url = build_url(ticker)

    # Task asks for price + 52-week range reasoning
    task = (
        f"From this Google Finance page for {ticker}, extract:\n"
        f"- the current stock price in USD,\n"
        f"- the 52-week low and 52-week high,\n"
        f"and decide whether the current price is closer to the 52-week high or the 52-week low.\n"
        f"Explain your reasoning briefly in the notes.\n\n"
        f"Ignore any global indices such as DAX, FTSE 100, CAC 40, etc., and use the price "
        f"that is clearly associated with the company card for {ticker}."
    )

    try:
        html = fetch_page_html(url)
        text = html_to_visible_text(html)
    except FetchError as exc:
        print(f"Failed to fetch page: {exc}")
        return

    agent = create_web_scraping_agent()
    result = ask_agent(agent, task, url, text)

    print("\n=== Agent JSON result ===")
    print(result)
    print("\nShort answer:")
    print(result.get("answer"))
    print("\nNotes:")
    print(result.get("notes"))


if __name__ == "__main__":
    main()
