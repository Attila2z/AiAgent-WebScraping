import re
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
        # Use default headers – some sites behave differently for custom User-Agents.
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

    Args:
        html: Raw HTML string.

    Returns:
        Cleaned plain-text representation of the page.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove tags that are usually not useful for content.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    # Normalize whitespace
    return " ".join(text.split())


def extract_google_finance_price(html: str) -> float | None:
    """Try to extract a numeric price from a Google Finance quote page.

    This is a heuristic parser: it looks for elements that usually contain
    the current price (e.g. class names used by Google Finance) and returns
    the first reasonable number it finds.

    IMPORTANT:
        - This is only a heuristic.
        - We use it for debugging/evaluation, not as guaranteed truth.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Common pattern on Google Finance: price inside elements with class 'YMlKec'
    candidates = soup.find_all(["div", "span"], class_=lambda c: c and "YMlKec" in c)

    for tag in candidates:
        text = tag.get_text(strip=True)
        # Look for something that looks like a number, e.g. 355.23 or 1,234.56
        match = re.search(r"-?\d[\d,]*\.?\d*", text)
        if not match:
            continue

        num_str = match.group(0).replace(",", "")
        try:
            value = float(num_str)
        except ValueError:
            continue

        # Filter out obviously unrealistic values for a single stock.
        # For example, ignore large index levels like DAX 24028.14.
        if not (0 < value < 5000):
            continue

        return value

    return None
