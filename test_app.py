"""
Automated unit tests for Web Scraper parsing and export routines.
Uses static mock HTML strings so tests run deterministically without internet reliance.
Run with: python -m unittest test_app.py
"""

import json
import os
import tempfile
import unittest
from exporters import export_to_csv, export_to_json, export_to_txt
from scraper import parse_headlines_html, parse_quotes_html

MOCK_QUOTES_HTML = """
<html>
<body>
  <div class="quote">
    <span class="text">“The world as we have created it is a process of our thinking.”</span>
    <span>by <small class="author">Albert Einstein</small></span>
    <div class="tags">
      <a class="tag">change</a>
      <a class="tag">deep-thoughts</a>
    </div>
  </div>
  <div class="quote">
    <span class="text">“It is our choices, that show what we truly are, far more than our abilities.”</span>
    <span>by <small class="author">J.K. Rowling</small></span>
    <div class="tags">
      <a class="tag">abilities</a>
      <a class="tag">choices</a>
    </div>
  </div>
</body>
</html>
"""

MOCK_HEADLINES_HTML = """
<html>
<body>
  <table>
    <tr class="athing">
      <td><span class="rank">1.</span></td>
      <td>
        <span class="titleline">
          <a href="https://example.com/ai-breakthrough">Open Source AI Model Breakthrough</a>
          <span class="sitebit comhead"><span class="sitestr">example.com</span></span>
        </span>
      </td>
    </tr>
    <tr class="athing">
      <td><span class="rank">2.</span></td>
      <td>
        <span class="titleline">
          <a href="https://github.com/fast-python">Fast Python 3.14 Compiler Published</a>
          <span class="sitebit comhead"><span class="sitestr">github.com</span></span>
        </span>
      </td>
    </tr>
  </table>
</body>
</html>
"""


class TestScraperParsing(unittest.TestCase):
    def test_parse_quotes(self):
        quotes = parse_quotes_html(MOCK_QUOTES_HTML, max_items=5)
        self.assertEqual(len(quotes), 2)

        # Check first quote details
        q1 = quotes[0]
        self.assertIn("The world as we have created it", q1["quote"])
        self.assertEqual(q1["author"], "Albert Einstein")
        self.assertEqual(q1["tags"], ["change", "deep-thoughts"])

        # Check second quote
        q2 = quotes[1]
        self.assertEqual(q2["author"], "J.K. Rowling")
        self.assertIn("abilities", q2["tags"])

    def test_quotes_max_items_limit(self):
        quotes = parse_quotes_html(MOCK_QUOTES_HTML, max_items=1)
        self.assertEqual(len(quotes), 1)

    def test_parse_headlines(self):
        headlines = parse_headlines_html(MOCK_HEADLINES_HTML, max_items=5)
        self.assertEqual(len(headlines), 2)

        h1 = headlines[0]
        self.assertEqual(h1["rank"], 1)
        self.assertEqual(h1["title"], "Open Source AI Model Breakthrough")
        self.assertEqual(h1["url"], "https://example.com/ai-breakthrough")
        self.assertEqual(h1["source"], "example.com")


class TestExporters(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.dummy_data = [
            {"quote": "Stay hungry, stay foolish.", "author": "Steve Jobs", "tags": ["inspiration"]},
            {"quote": "Simplicity is prerequisite for reliability.", "author": "Edsger Dijkstra", "tags": ["computing"]}
        ]

    def test_json_export(self):
        json_path = os.path.join(self.temp_dir, "test.json")
        success = export_to_json(self.dummy_data, json_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(json_path))

        with open(json_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["author"], "Steve Jobs")

    def test_txt_export(self):
        txt_path = os.path.join(self.temp_dir, "test.txt")
        success = export_to_txt(self.dummy_data, txt_path, data_type="quotes")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(txt_path))

    def test_csv_export(self):
        csv_path = os.path.join(self.temp_dir, "test.csv")
        success = export_to_csv(self.dummy_data, csv_path, data_type="quotes")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(csv_path))


if __name__ == "__main__":
    unittest.main()
