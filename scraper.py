"""
Web Scraper Module
==================
Handles HTTP requests using `requests` and parses HTML elements using `BeautifulSoup`.
Supports scraping:
1. Quotes, authors, and tags from http://quotes.toscrape.com/
2. Latest tech news headlines and links from https://news.ycombinator.com/
"""

from bs4 import BeautifulSoup
import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
DEFAULT_TIMEOUT = 10


def fetch_html(url: str) -> str | None:
    """
    Sends an HTTP GET request with custom headers and timeout.
    Safely catches network exceptions (ConnectionError, Timeout, HTTPError).
    """
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        print(f"\n  [Error] Request timed out while connecting to {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"\n  [Error] Failed to connect to {url}. Please check your internet connection.")
        return None
    except requests.exceptions.HTTPError as err:
        print(f"\n  [Error] HTTP response error: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"\n  [Error] An unexpected network error occurred: {err}")
        return None


def parse_quotes_html(html_content: str, max_items: int = 10) -> list[dict]:
    """
    Extracts quote text, authors, and tag lists from quotes.toscrape.com HTML structure.
    Separated from network logic for easy, reliable offline unit testing.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    quote_cards = soup.find_all("div", class_="quote")
    extracted = []

    for card in quote_cards:
        if len(extracted) >= max_items:
            break

        # 1. Quote text
        text_elem = card.find("span", class_="text")
        raw_text = text_elem.get_text(strip=True) if text_elem else "No quote text"
        # Strip decorative typographic quotation marks if present
        clean_text = raw_text.strip("“”\"'")

        # 2. Author
        author_elem = card.find("small", class_="author")
        author = author_elem.get_text(strip=True) if author_elem else "Unknown"

        # 3. Tags
        tag_elems = card.find_all("a", class_="tag")
        tags = [t.get_text(strip=True) for t in tag_elems]

        extracted.append({
            "quote": clean_text,
            "author": author,
            "tags": tags,
        })

    return extracted


def scrape_quotes(max_items: int = 10) -> list[dict]:
    """Scrapes top quotes from quotes.toscrape.com."""
    url = "http://quotes.toscrape.com/"
    print(f"  -> Connecting to {url}...")
    html = fetch_html(url)
    if not html:
        return []
    return parse_quotes_html(html, max_items=max_items)


def parse_headlines_html(html_content: str, max_items: int = 15) -> list[dict]:
    """
    Extracts tech headlines, external links, rank, and source domain from Hacker News HTML.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all("tr", class_="athing")
    extracted = []

    for row in rows:
        if len(extracted) >= max_items:
            break

        # 1. Rank
        rank_elem = row.find("span", class_="rank")
        rank = rank_elem.get_text(strip=True).rstrip(".") if rank_elem else str(len(extracted) + 1)

        # 2. Title and Link
        title_container = row.find("span", class_="titleline")
        if not title_container:
            continue

        link_elem = title_container.find("a")
        if not link_elem:
            continue

        title = link_elem.get_text(strip=True)
        url = link_elem.get("href", "")

        # 3. Domain source (e.g. github.com, nytimes.com)
        site_elem = title_container.find("span", class_="sitestr")
        source = site_elem.get_text(strip=True) if site_elem else "news.ycombinator.com"

        extracted.append({
            "rank": int(rank) if rank.isdigit() else len(extracted) + 1,
            "title": title,
            "url": url,
            "source": source,
        })

    return extracted


def scrape_headlines(max_items: int = 15) -> list[dict]:
    """Scrapes latest tech headlines from Hacker News."""
    url = "https://news.ycombinator.com/"
    print(f"  -> Connecting to {url}...")
    html = fetch_html(url)
    if not html:
        return []
    return parse_headlines_html(html, max_items=max_items)
