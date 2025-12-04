# WebScraping/tools.py
import requests
from bs4 import BeautifulSoup


def fetch_page_html(url: str) -> str:
    """Download the raw HTML of a webpage."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def html_to_visible_text(html: str) -> str:
    """Convert HTML to plain text (removes tags, scripts, etc.)."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style tags – they are usually not helpful to the LLM
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())  # normalize whitespace
