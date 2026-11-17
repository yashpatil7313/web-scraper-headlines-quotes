# Python Internship Project 04: Web Scraper for Headlines & Quotes

**Submitted by:** Yashraj  
**Technology:** Python 3.10+, Requests, BeautifulSoup4  
**Project Category:** Web Scraping, HTML Parsing & Structured Data Extraction  

---

## 1. Project Overview

This repository contains my submission for **Project 04** of the Python Developer Internship: an automated **Web Scraper** designed to fetch, parse, and structure real-world web content into clean JSON, text, and CSV files.

The project demonstrates:
- Sending HTTP GET requests with custom user-agent headers and timeout handling via `requests`.
- Inspecting DOM hierarchies and extracting clean elements using `BeautifulSoup` (CSS classes, tags, and attributes).
- Defensive exception handling for network timeouts, bad HTTP status codes, and connection failures.
- Multi-format file export (indented JSON, formatted text reports, and structured CSV).
- A client-side web showcase (`index.html`) deployed to GitHub Pages for instant interactive testing.

---

## 2. Project Architecture

The application separates network retrieval, HTML parsing, export routines, and CLI menus into modular files:

```text
web_scraper_headlines_quotes/
│
├── main.py              # CLI entry point and user interaction loop
├── scraper.py           # HTTP retrieval and BeautifulSoup HTML tag parsing
├── exporters.py         # Multi-format data exporters (JSON, TXT, CSV) and console previews
├── utils.py             # User input readers and terminal formatting helpers
├── requirements.txt     # Project dependencies (requests, beautifulsoup4)
├── test_app.py          # Automated unit test suite with mock HTML fixtures
├── sample_data/         # Pre-scraped reference data (sample_quotes.json, sample_headlines.json)
├── index.html           # Standalone web demo for GitHub Pages
├── .gitignore           # Excludes local caches and runtime generated files
└── README.md            # Project documentation and guide
```

---

## 3. Data Sources & Extraction Logic

### 1. Famous Quotes (`http://quotes.toscrape.com/`)
- **Target Container:** `div.quote`
- **Quote Text:** `span.text` (stripped of decorative typographical quotes)
- **Author:** `small.author`
- **Tags:** `div.tags a.tag` (collected as a list of keyword strings)

### 2. Tech News Headlines (`https://news.ycombinator.com/`)
- **Target Row:** `tr.athing`
- **Rank:** `span.rank`
- **Headline Title & URL:** `span.titleline > a` (extracts text and external `href` destination)
- **Source Domain:** `span.sitestr`

### 3. Defensive Network Handling
The network helper `fetch_html()` wraps HTTP calls with:
- A custom desktop `User-Agent` string to prevent bot blocking.
- A 10-second request timeout to avoid hanging processes.
- Status code validation (`response.raise_for_status()`).
- Granular error catching (`requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, `requests.exceptions.HTTPError`).

---

## 4. How to Run the Application

### 1. Installation
Clone the repository and install the dependencies:

```bash
cd web_scraper_headlines_quotes
pip install -r requirements.txt
```

### 2. Running the Terminal Scraper
Launch the interactive CLI menu:

```bash
python main.py
```

Follow the on-screen prompts to select your target (Quotes or Tech Headlines), specify how many items you wish to extract, and export them to JSON, TXT, or CSV.

### 3. Running the Automated Tests
Run the unit test suite:

```bash
python -m unittest test_app.py
```

Expected output:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.022s

OK
```
*Note: Unit tests execute against static mock HTML strings, ensuring 100% deterministic testing without requiring an active internet connection.*

---

## 5. Sample Outputs

### JSON Output Sample (`sample_quotes.json`):
```json
[
  {
    "quote": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
    "author": "Albert Einstein",
    "tags": [
      "change",
      "deep-thoughts",
      "thinking",
      "world"
    ]
  },
  {
    "quote": "It is our choices, Harry, that show what we truly are, far more than our abilities.",
    "author": "J.K. Rowling",
    "tags": [
      "abilities",
      "choices"
    ]
  }
]
```

### Text Output Sample:
```text
=== SCRAPED QUOTES REPORT ===
Total Items: 2

[1] "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking."
    — Author: Albert Einstein
    — Tags:   change, deep-thoughts, thinking, world

[2] "It is our choices, Harry, that show what we truly are, far more than our abilities."
    — Author: J.K. Rowling
    — Tags:   abilities, choices
```
