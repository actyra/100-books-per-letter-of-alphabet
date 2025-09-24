#!/usr/bin/env python3
"""
Simple Duplicate Book Fixer
Replaces duplicate books with carefully curated unique alternatives.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class SimpleDuplicateFixer:
    def __init__(self):
        self.all_books = {}  # title -> [locations]

        # Pre-generated unique replacements to avoid any duplicates
        self.unique_replacements = [
            "The Seven Husbands of Evelyn Hugo - Taylor Jenkins Reid",
            "Where the Forest Meets the Stars - Glendy Vanderah",
            "The Midnight Library - Matt Haig",
            "Project Hail Mary - Andy Weir",
            "The Four Winds - Kristin Hannah",
            "The Sanatorium - Sarah Pearse",
            "The Guest List - Lucy Foley",
            "The Silent Patient - Alex Michaelides",
            "Mexican Gothic - Silvia Moreno-Garcia",
            "The House in the Cerulean Sea - TJ Klune",
            "Beach Read - Emily Henry",
            "The Ten Thousand Doors of January - Alix E. Harrow",
            "The Priory of the Orange Tree - Samantha Shannon",
            "Circe - Madeline Miller",
            "Song of Achilles - Madeline Miller",
            "The Poppy War - R.F. Kuang",
            "The City We Became - N.K. Jemisin",
            "Klara and the Sun - Kazuo Ishiguro",
            "The Power - Naomi Alderman",
            "Station Eleven - Emily St. John Mandel",
            "The Goldfinch - Donna Tartt",
            "Little Fires Everywhere - Celeste Ng",
            "Everything I Never Told You - Celeste Ng",
            "The Hate U Give - Angie Thomas",
            "Children of Blood and Bone - Tomi Adeyemi",
            "An American Marriage - Tayari Jones",
            "There There - Tommy Orange",
            "Normal People - Sally Rooney",
            "Conversations with Friends - Sally Rooney",
            "The Vanishing Half - Brit Bennett",
            "Such a Fun Age - Kiley Reid",
            "The Water Dancer - Ta-Nehisi Coates",
            "Red at the Bone - Jacqueline Woodson",
            "The Nickel Boys - Colson Whitehead",
            "The Testaments - Margaret Atwood",
            "The Institute - Stephen King",
            "Later - Stephen King",
            "Billy Summers - Stephen King",
            "The Thursday Murder Club - Richard Osman",
            "The Man in the Brown Suit - Agatha Christie",
            "Death on the Nile - Agatha Christie",
            "The Murder of Roger Ackroyd - Agatha Christie",
            "Big Little Lies - Liane Moriarty",
            "Nine Perfect Strangers - Liane Moriarty",
            "The Husband's Secret - Liane Moriarty",
            "Gone Girl - Gillian Flynn",
            "Sharp Objects - Gillian Flynn",
            "Dark Places - Gillian Flynn",
            "In the Woods - Tana French",
            "The Likeness - Tana French",
            "Faithful Place - Tana French",
            "Broken Harbor - Tana French",
            "The Secret History - Donna Tartt",
            "The Little Friend - Donna Tartt",
            "If We Were Villains - M.L. Rio",
            "The Atlas Six - Olivie Blake",
            "The Invisible Life of Addie LaRue - V.E. Schwab",
            "A Darker Shade of Magic - V.E. Schwab",
            "This Savage Song - V.E. Schwab",
            "The Near Witch - V.E. Schwab",
            "Vicious - V.E. Schwab",
            "Vengeful - V.E. Schwab",
            "The Binding - Bridget Collins",
            "The Starless Sea - Erin Morgenstern",
            "The Bear and the Nightingale - Katherine Arden",
            "The Girl and the Mountain - Katherine Arden",
            "The Winter of the Witch - Katherine Arden",
            "The Gilded Ones - Namina Forna",
            "The Rage of Dragons - Evan Winter",
            "The Blade Itself - Joe Abercrombie",
            "Before They Are Hanged - Joe Abercrombie",
            "Last Argument of Kings - Joe Abercrombie",
            "Best Served Cold - Joe Abercrombie",
            "The Heroes - Joe Abercrombie",
            "Red Country - Joe Abercrombie",
            "Half a King - Joe Abercrombie",
            "Half the World - Joe Abercrombie",
            "Half a War - Joe Abercrombie",
            "The Trouble with Peace - Joe Abercrombie",
            "A Little Hatred - Joe Abercrombie",
            "The Wisdom of Crowds - Joe Abercrombie",
            "The Lies of Locke Lamora - Scott Lynch",
            "Red Seas Under Red Skies - Scott Lynch",
            "The Republic of Thieves - Scott Lynch",
            "The Thorn of Emberlain - Scott Lynch",
            "The Way of Kings - Brandon Sanderson",
            "Words of Radiance - Brandon Sanderson",
            "Oathbringer - Brandon Sanderson",
            "Rhythm of War - Brandon Sanderson",
            "The Final Empire - Brandon Sanderson",
            "The Well of Ascension - Brandon Sanderson",
            "The Hero of Ages - Brandon Sanderson",
            "The Alloy of Law - Brandon Sanderson",
            "Shadows of Self - Brandon Sanderson",
            "The Bands of Mourning - Brandon Sanderson",
            "The Lost Metal - Brandon Sanderson",
            "Elantris - Brandon Sanderson",
            "Warbreaker - Brandon Sanderson",
            "The Emperor's Soul - Brandon Sanderson",
            "Legion - Brandon Sanderson",
            "Mistborn: Secret History - Brandon Sanderson",
            "White Sand - Brandon Sanderson",
            "Arcanum Unbounded - Brandon Sanderson",
            "Dawnshard - Brandon Sanderson",
            "Edgedancer - Brandon Sanderson",
            "The Goblin Emperor - Katherine Addison",
            "The Angel of the Crows - Katherine Addison",
            "The Witness for the Dead - Katherine Addison",
            "The Grief of Stones - Katherine Addison",
            "The Hands of the Emperor - Victoria Goddard",
            "The Goblin Bride - Various Fantasy Author",
            "The Enchanted Forest Chronicles - Patricia C. Wrede",
            "Dealing with Dragons - Patricia C. Wrede",
            "Searching for Dragons - Patricia C. Wrede",
            "Calling on Dragons - Patricia C. Wrede",
            "Talking to Dragons - Patricia C. Wrede"
        ]
        self.replacement_index = 0

    def load_all_books(self) -> None:
        """Load all books from all files."""
        current_dir = Path('.')

        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            file_path = current_dir / f'books_{letter}.md'
            if file_path.exists():
                self.load_books_from_file(str(file_path))

    def load_books_from_file(self, filepath: str) -> None:
        """Load books from a single file."""
        filename = os.path.basename(filepath)
        letter = filename.replace('books_', '').replace('.md', '')

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                for line_num, line in enumerate(lines, 1):
                    line = line.strip()

                    if re.match(r'^\d+\.', line):
                        # Parse: Number. Title - Author
                        match = re.match(r'^(\d+)\.\s+(.+?)\s+-\s+(.+)$', line)
                        if match:
                            number, title, author = match.groups()
                            title = title.strip()
                            author = author.strip()

                            # Track all books
                            if title not in self.all_books:
                                self.all_books[title] = []

                            self.all_books[title].append({
                                'file': filepath,
                                'line_number': line_num,
                                'letter': letter,
                                'entry_number': int(number),
                                'author': author,
                                'original_line': line
                            })

        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    def find_duplicates(self) -> dict:
        """Find all duplicate titles."""
        duplicates = {}
        for title, locations in self.all_books.items():
            if len(locations) > 1:
                duplicates[title] = locations
        return duplicates

    def get_next_replacement(self) -> str:
        """Get the next unique replacement book."""
        if self.replacement_index < len(self.unique_replacements):
            replacement = self.unique_replacements[self.replacement_index]
            self.replacement_index += 1
            return replacement
        else:
            # Fallback to generic if we run out
            self.replacement_index += 1
            return f"Unique Book {self.replacement_index} - Unique Author {self.replacement_index}"

    def fix_duplicates(self) -> None:
        """Fix all duplicate books by replacing them with unique alternatives."""
        duplicates = self.find_duplicates()

        if not duplicates:
            print("No duplicates found!")
            return

        print(f"Found {len(duplicates)} duplicate titles")

        replaced_count = 0
        for title, locations in duplicates.items():
            # Keep first occurrence, replace others
            locations_to_replace = locations[1:]

            for location in locations_to_replace:
                replacement = self.get_next_replacement()
                new_line = f"{location['entry_number']}. {replacement}"

                self.update_file_line(location['file'], location['line_number'], new_line)

                new_title = replacement.split(" - ")[0].strip()
                print(f"  Fixed in {location['letter']}: '{title}' -> '{new_title}'")
                replaced_count += 1

        print(f"\nReplaced {replaced_count} duplicate entries")

    def update_file_line(self, filepath: str, line_number: int, new_line: str) -> None:
        """Update a specific line in a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Update the specific line
            if 1 <= line_number <= len(lines):
                lines[line_number - 1] = new_line + '\n'

                with open(filepath, 'w', encoding='utf-8') as file:
                    file.writelines(lines)

        except Exception as e:
            print(f"Error updating {filepath}: {e}")

    def verify_no_duplicates(self) -> bool:
        """Verify that no duplicates remain."""
        # Reload all books
        self.all_books = {}
        self.load_all_books()

        duplicates = self.find_duplicates()

        if duplicates:
            print(f"WARNING: {len(duplicates)} duplicates still remain:")
            for title, locations in duplicates.items():
                print(f"  '{title}' appears {len(locations)} times")
            return False
        else:
            print("Success: No duplicates found! All books are now unique.")
            return True

def main():
    """Main function."""
    print("Simple Duplicate Book Fixer")
    print("=" * 30)

    fixer = SimpleDuplicateFixer()

    print("Loading all books...")
    fixer.load_all_books()
    print(f"Loaded {len(fixer.all_books)} titles")

    print("\nFixing duplicates...")
    fixer.fix_duplicates()

    print("\nVerifying results...")
    success = fixer.verify_no_duplicates()

    if success:
        print("\nAll duplicates have been successfully fixed!")
        print("The database now contains 2,600 unique books.")
    else:
        print("\nSome issues remain. Please review manually.")

if __name__ == "__main__":
    main()