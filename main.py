# main.py
from WebScraping.tools import fetch_page_html, html_to_visible_text
from WebScraping.agent import create_web_scraping_agent, ask_agent


def run_single_example():
    url = "https://www.google.com/finance/quote/META:NASDAQ"
    task = "Extract the current stock price of META (in USD) from this page. Respond with the price and currency."

    # 1) Use tool to get data source
    html = fetch_page_html(url)
    text = html_to_visible_text(html)

    # 2) Create agent
    agent = create_web_scraping_agent()

    # 3) Ask agent to solve the task
    answer = ask_agent(agent, task, url, text)

    print("Agent answer:")
    print(answer)


if __name__ == "__main__":
    run_single_example()
