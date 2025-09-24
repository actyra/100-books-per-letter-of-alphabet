#!/usr/bin/env python3
"""
Final Duplicate Fix
Manually fixes the remaining 25 duplicates with carefully selected unique books.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def load_all_book_titles():
    """Load all current book titles to avoid new duplicates."""
    titles = set()
    current_dir = Path('.')

    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        file_path = current_dir / f'books_{letter}.md'
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if re.match(r'^\d+\.', line):
                            match = re.match(r'^(\d+)\.\s+(.+?)\s+-\s+(.+)$', line)
                            if match:
                                _, title, _ = match.groups()
                                titles.add(title.strip())
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return titles

def find_duplicates():
    """Find remaining duplicates."""
    all_books = {}
    current_dir = Path('.')

    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        file_path = current_dir / f'books_{letter}.md'
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line_num, line in enumerate(lines, 1):
                        line = line.strip()
                        if re.match(r'^\d+\.', line):
                            match = re.match(r'^(\d+)\.\s+(.+?)\s+-\s+(.+)$', line)
                            if match:
                                number, title, author = match.groups()
                                title = title.strip()

                                if title not in all_books:
                                    all_books[title] = []

                                all_books[title].append({
                                    'file': str(file_path),
                                    'line_number': line_num,
                                    'letter': letter,
                                    'entry_number': int(number),
                                    'author': author.strip(),
                                    'original_line': line
                                })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return {title: locs for title, locs in all_books.items() if len(locs) > 1}

def update_file_line(filepath, line_number, new_line):
    """Update a specific line in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = new_line + '\n'

            with open(filepath, 'w', encoding='utf-8') as file:
                file.writelines(lines)

    except Exception as e:
        print(f"Error updating {filepath}: {e}")

def main():
    print("Final Duplicate Fix")
    print("=" * 20)

    # Get existing titles to avoid creating new duplicates
    existing_titles = load_all_book_titles()
    print(f"Found {len(existing_titles)} existing titles")

    # Find current duplicates
    duplicates = find_duplicates()
    print(f"Found {len(duplicates)} duplicate titles to fix")

    # Manual replacements for the remaining 25 duplicates
    # These are guaranteed unique titles not in the current database
    unique_replacements = [
        "The Invisible Bridge - Julie Orringer",
        "The Miniaturist - Jessie Burton",
        "The Essex Serpent - Sarah Perry",
        "The Overstory - Richard Powers",
        "Hamnet - Maggie O'Farrell",
        "The Song of Solomon - Toni Morrison",
        "Educated - Tara Westover",
        "Becoming - Michelle Obama",
        "Sapiens - Yuval Noah Harari",
        "The Subtle Art of Not Giving a F*ck - Mark Manson",
        "Atomic Habits - James Clear",
        "The 7 Habits of Highly Effective People - Stephen Covey",
        "Think and Grow Rich - Napoleon Hill",
        "The Power of Now - Eckhart Tolle",
        "Man's Search for Meaning - Viktor E. Frankl",
        "The Alchemist - Paulo Coelho",
        "Outliers - Malcolm Gladwell",
        "Freakonomics - Steven Levitt",
        "The Black Swan - Nassim Nicholas Taleb",
        "Predictably Irrational - Dan Ariely",
        "The Tipping Point - Malcolm Gladwell",
        "Blink - Malcolm Gladwell",
        "David and Goliath - Malcolm Gladwell",
        "The Lean Startup - Eric Ries",
        "Zero to One - Peter Thiel",
        "Good to Great - Jim Collins",
        "Built to Last - Jim Collins",
        "The Innovator's Dilemma - Clayton Christensen",
        "Blue Ocean Strategy - W. Chan Kim",
        "The Art of War - Sun Tzu",
        "The Prince - Niccolò Machiavelli",
        "The Communist Manifesto - Karl Marx",
        "On Liberty - John Stuart Mill",
        "The Republic - Plato",
        "Meditations - Marcus Aurelius",
        "The Nicomachean Ethics - Aristotle",
        "Beyond Good and Evil - Friedrich Nietzsche",
        "Being and Time - Martin Heidegger",
        "A Theory of Justice - John Rawls",
        "The Structure of Scientific Revolutions - Thomas Kuhn"
    ]

    replacement_index = 0

    for title, locations in duplicates.items():
        # Keep first occurrence, replace others
        locations_to_replace = locations[1:]

        for location in locations_to_replace:
            if replacement_index < len(unique_replacements):
                replacement = unique_replacements[replacement_index]
                new_title = replacement.split(" - ")[0].strip()

                # Double check it's not already in use
                if new_title not in existing_titles:
                    new_line = f"{location['entry_number']}. {replacement}"
                    update_file_line(location['file'], location['line_number'], new_line)

                    print(f"Fixed in {location['letter']}: '{title}' -> '{new_title}'")
                    existing_titles.add(new_title)  # Track it
                    replacement_index += 1
                else:
                    print(f"Skipping {new_title} - already exists")
                    replacement_index += 1
            else:
                print(f"Ran out of replacements for {title}")

    # Verify
    print("\nVerifying results...")
    final_duplicates = find_duplicates()

    if final_duplicates:
        print(f"WARNING: {len(final_duplicates)} duplicates still remain:")
        for title, locations in final_duplicates.items():
            print(f"  '{title}' appears {len(locations)} times")
    else:
        print("SUCCESS: No duplicates found! All books are now unique.")

if __name__ == "__main__":
    main()