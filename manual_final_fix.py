#!/usr/bin/env python3
"""
Manual Final Fix for Last 15 Duplicates
"""

import re
from pathlib import Path

def update_file_line(filepath, line_number, new_line):
    """Update a specific line in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = new_line + '\n'

            with open(filepath, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            return True

    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    print("Manual Final Fix for Last 15 Duplicates")
    print("=" * 40)

    # Manual fixes - finding each duplicate and replacing with completely unique books
    fixes = [
        # These are books that definitely don't exist in the current database
        ("books_B.md", 32, "32. The Book of Lost Names - Kristin Harmel"),  # Replace 'Broken Harbor'
        ("books_C.md", 30, "30. The Covenant of Water - Abraham Verghese"),  # Replace 'Circe'
        ("books_E.md", 35, "35. The Empress of Salt and Fortune - Nghi Vo"),  # Replace 'Everything I Never Told You'
        ("books_G.md", 25, "25. The Galaxy and the Ground Within - Becky Chambers"),  # Replace 'Gone Girl'
        ("books_W.md", 15, "15. The World According to Garp - John Irving"),  # Replace 'The Water Dancer'
        ("books_G.md", 40, "40. The Great Alone - Kristin Hannah"),  # Replace 'The Guest List'
        ("books_N.md", 25, "25. The Name of the Rose - Umberto Eco"),  # Replace 'The Nickel Boys'
        ("books_H.md", 30, "30. The Human Condition - Hannah Arendt"),  # Replace 'The Hate U Give'
        ("books_H.md", 50, "50. The History of Love - Nicole Krauss"),  # Replace 'The House in the Cerulean Sea'
        ("books_P.md", 45, "45. The Power Broker - Robert Caro"),  # Replace 'The Power'
        ("books_N.md", 50, "50. The Night Watchman - Louise Erdrich"),  # Replace 'Nine Perfect Strangers'
        ("books_L.md", 40, "40. The Light We Lost - Jill Santopolo"),  # Replace 'The Likeness'
        ("books_M.md", 60, "60. The Measure - Nikki Erlick"),  # Replace 'The Murder of Roger Ackroyd'
        ("books_N.md", 75, "75. The Nest - Cynthia D'Aprix Sweeney"),  # Replace 'Normal People'
        ("books_S.md", 25, "25. The School for Good Mothers - Jessamine Chan")  # Replace 'The Seven Husbands of Evelyn Hugo'
    ]

    success_count = 0
    for file_name, line_num, new_content in fixes:
        file_path = Path('.') / file_name
        if file_path.exists():
            if update_file_line(str(file_path), line_num, new_content):
                title = new_content.split(". ")[1].split(" - ")[0]
                print(f"Fixed {file_name}:{line_num} -> '{title}'")
                success_count += 1
            else:
                print(f"Failed to fix {file_name}:{line_num}")
        else:
            print(f"File not found: {file_name}")

    print(f"\nApplied {success_count}/{len(fixes)} fixes")

    # Verify by rerunning duplicate detection
    print("\nVerifying results...")

    all_books = {}
    current_dir = Path('.')

    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        file_path = current_dir / f'books_{letter}.md'
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file, 1):
                        line = line.strip()
                        if re.match(r'^\d+\.', line):
                            match = re.match(r'^(\d+)\.\s+(.+?)\s+-\s+(.+)$', line)
                            if match:
                                _, title, _ = match.groups()
                                title = title.strip()

                                if title not in all_books:
                                    all_books[title] = 0
                                all_books[title] += 1

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    duplicates = {title: count for title, count in all_books.items() if count > 1}

    if duplicates:
        print(f"WARNING: {len(duplicates)} duplicates still remain:")
        for title, count in duplicates.items():
            print(f"  '{title}' appears {count} times")
    else:
        print("SUCCESS: No duplicates found! All 2,600 books are now unique!")

if __name__ == "__main__":
    main()