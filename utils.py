"""
Utility helpers for user input validation, terminal presentation, and banners.
Internship Project 04: Web Scraper for Headlines & Quotes.
"""

import sys


def show_header(title: str, line_char: str = "=") -> None:
    """Prints a styled header line for terminal menus."""
    width = 62
    bar = line_char * width
    print(f"\n{bar}")
    print(f" {title.upper()}")
    print(f"{bar}")


def show_divider(length: int = 62) -> None:
    """Prints a simple horizontal separator."""
    print("-" * length)


def read_choice(prompt: str, valid_options: list[str]) -> str:
    """Prompts for and validates menu choices (case-insensitive)."""
    opts = [opt.strip().upper() for opt in valid_options]
    while True:
        try:
            user_input = input(prompt).strip().upper()
            if user_input in opts:
                return user_input
            print(f"   [!] Please pick one of: {', '.join(opts)}")
        except (KeyboardInterrupt, EOFError):
            print("\n   [!] Exiting.")
            sys.exit(0)


def read_int(prompt: str, min_val: int = 1, max_val: int = 100, default_val: int = 10) -> int:
    """Prompts for an integer count with a default value."""
    full_prompt = f"{prompt} [Press Enter for {default_val}]: "
    while True:
        try:
            raw = input(full_prompt).strip()
            if not raw:
                return default_val
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"   [!] Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("   [!] That was not a valid number. Try again.")
        except (KeyboardInterrupt, EOFError):
            print("\n   [!] Input cancelled.")
            sys.exit(0)


def pause() -> None:
    """Pauses until user presses Enter."""
    try:
        input("\nPress Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
