import requests
from bs4 import BeautifulSoup


class FetchError(Exception):
    """Custom exception raised when a page cannot be fetched."""
    pass


def fetch_page_html(url: str) -> str:
    """Download the raw HTML of a webpage.

    Raises:
        FetchError: if the HTTP request fails or times out.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise FetchError(f"Timeout when fetching {url}") from exc
    except requests.exceptions.RequestException as exc:
        raise FetchError(f"HTTP error when fetching {url}: {exc}") from exc

    return response.text


def html_to_visible_text(html: str) -> str:
    """Convert HTML to plain visible text.

    - Removes <script>, <style>, and <noscript> tags.
    - Strips extra whitespace.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())
