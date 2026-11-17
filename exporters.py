"""
Data Exporters & Output Formatters
==================================
Formats scraped data into clean JSON, text, and CSV files,
and renders formatted previews in the terminal.
"""

import csv
import json
import os
from utils import show_divider, show_header


def export_to_json(data: list[dict], filename: str) -> bool:
    """Saves data list as clean, indented JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Saved {len(data)} items to JSON: '{filename}'")
        return True
    except Exception as e:
        print(f"  [Error] Failed to write JSON file: {e}")
        return False


def export_to_txt(data: list[dict], filename: str, data_type: str = "quotes") -> bool:
    """Formats and exports data into a clean, human-readable text file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== SCRAPED {data_type.upper()} REPORT ===\n")
            f.write(f"Total Items: {len(data)}\n\n")

            if data_type == "quotes":
                for idx, item in enumerate(data, start=1):
                    tags_str = ", ".join(item.get("tags", [])) or "None"
                    f.write(f"[{idx}] \"{item['quote']}\"\n")
                    f.write(f"    — Author: {item['author']}\n")
                    f.write(f"    — Tags:   {tags_str}\n\n")
            else:
                for item in data:
                    f.write(f"#{item['rank']} {item['title']}\n")
                    f.write(f"    Source: {item['source']}\n")
                    f.write(f"    Link:   {item['url']}\n\n")

        print(f"  ✅ Saved {len(data)} items to Text: '{filename}'")
        return True
    except Exception as e:
        print(f"  [Error] Failed to write text file: {e}")
        return False


def export_to_csv(data: list[dict], filename: str, data_type: str = "quotes") -> bool:
    """Exports data into a structured CSV file."""
    if not data:
        print("  [!] No data to export.")
        return False

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            if data_type == "quotes":
                fieldnames = ["quote", "author", "tags"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow({
                        "quote": item["quote"],
                        "author": item["author"],
                        "tags": "; ".join(item.get("tags", [])),
                    })
            else:
                fieldnames = ["rank", "title", "source", "url"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)

        print(f"  ✅ Saved {len(data)} items to CSV: '{filename}'")
        return True
    except Exception as e:
        print(f"  [Error] Failed to write CSV file: {e}")
        return False


def display_quotes_preview(quotes: list[dict]) -> None:
    """Renders a clean formatted preview of scraped quotes in the console."""
    show_header(f"SCRAPED QUOTES ({len(quotes)} items)")
    for idx, item in enumerate(quotes, start=1):
        tags_str = " | ".join(f"#{t}" for t in item.get("tags", []))
        print(f"  [{idx}] \"{item['quote']}\"")
        print(f"      — {item['author']}   {tags_str}")
        print()
    show_divider()


def display_headlines_preview(headlines: list[dict]) -> None:
    """Renders a clean formatted preview of tech headlines in the console."""
    show_header(f"LATEST TECH HEADLINES ({len(headlines)} items)")
    for item in headlines:
        print(f"  #{item['rank']:<2} | {item['title']}")
        print(f"       Source: {item['source']}")
        print(f"       URL:    {item['url']}")
        print()
    show_divider()
