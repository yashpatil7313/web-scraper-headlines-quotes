"""
CLI Application: Web Scraper for Headlines & Quotes
Internship Project 04 - Python 3.10+
Uses BeautifulSoup and requests to extract web data and export clean JSON / Text / CSV files.
"""

import sys
from exporters import (
    display_headlines_preview,
    display_quotes_preview,
    export_to_csv,
    export_to_json,
    export_to_txt,
)
from scraper import scrape_headlines, scrape_quotes
from utils import pause, read_choice, read_int, show_divider, show_header


def export_dialog(data: list[dict], data_type: str) -> None:
    """Prompts the user on how they want to save the scraped data."""
    if not data:
        return

    print("\n  Export Options:")
    print("  1. Save to JSON  (.json)")
    print("  2. Save to Text  (.txt)")
    print("  3. Save to CSV   (.csv)")
    print("  4. Save to All formats")
    print("  5. Skip export")
    show_divider()

    choice = read_choice("  Select export format (1-5): ", ["1", "2", "3", "4", "5"])

    if choice == "5":
        print("  Skipping file export.")
        return

    default_base = f"scraped_{data_type}"
    name_input = input(f"  Enter file base name [Press Enter for '{default_base}']: ").strip()
    base_name = name_input if name_input else default_base

    if choice == "1" or choice == "4":
        export_to_json(data, f"{base_name}.json")
    if choice == "2" or choice == "4":
        export_to_txt(data, f"{base_name}.txt", data_type=data_type)
    if choice == "3" or choice == "4":
        export_to_csv(data, f"{base_name}.csv", data_type=data_type)


def main() -> None:
    """Main application loop."""
    show_header("Web Scraper for Headlines & Quotes")
    print(" Project 04: HTTP Handling, Tag Extraction & Data Formatting")
    print(" Powered by BeautifulSoup4 & Requests")
    show_divider()

    while True:
        show_header("Scraper Main Menu")
        print("  1. Scrape Famous Quotes        (http://quotes.toscrape.com)")
        print("  2. Scrape Tech News Headlines  (https://news.ycombinator.com)")
        print("  3. Exit Application")
        show_divider()

        choice = read_choice("  Enter your selection (1-3): ", ["1", "2", "3"])

        if choice == "1":
            show_header("Scrape Quotes Setup")
            count = read_int("  How many quotes to scrape? (1-30)", min_val=1, max_val=30, default_val=10)
            quotes = scrape_quotes(max_items=count)
            if quotes:
                display_quotes_preview(quotes)
                export_dialog(quotes, "quotes")
            else:
                print("  [!] Could not retrieve quotes. Please check your internet connection.")
            pause()

        elif choice == "2":
            show_header("Scrape Tech Headlines Setup")
            count = read_int("  How many headlines to scrape? (1-30)", min_val=1, max_val=30, default_val=15)
            headlines = scrape_headlines(max_items=count)
            if headlines:
                display_headlines_preview(headlines)
                export_dialog(headlines, "headlines")
            else:
                print("  [!] Could not retrieve headlines. Please check your internet connection.")
            pause()

        elif choice == "3":
            print("\n  Thank you for using the Web Scraper. Happy scraping!\n")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Session closed by user. Exiting cleanly.")
        sys.exit(0)
