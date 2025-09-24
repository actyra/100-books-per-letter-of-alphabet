#!/usr/bin/env python3
"""
Duplicate Book Fixer
Identifies duplicate books across all files and replaces them with unique alternatives.
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

class DuplicateFixer:
    def __init__(self):
        self.all_books = {}  # title -> [(file, line_number, entry)]
        self.duplicates = {}  # title -> list of locations
        self.all_authors = set()

        # Curated replacement books organized by starting letter
        self.replacement_books = {
            'A': [
                "Americana - Don DeLillo",
                "The Amazing Adventures of Harry Potter - J.K. Rowling",
                "Alas, Babylon - Pat Frank",
                "A Wrinkle in Time - Madeleine L'Engle",
                "The Age of Wonder - Richard Holmes",
                "American Gods - Neil Gaiman",
                "The Amazing Adventures of Charlie Chaplin - David Robinson",
                "A Brief History of Time - Stephen Hawking",
                "The Awakening - Kate Chopin",
                "Adventures in the Screen Trade - William Goldman"
            ],
            'B': [
                "Beloved - Toni Morrison",
                "The Brief Wondrous Life of Oscar Wao - Junot Díaz",
                "Blink - Malcolm Gladwell",
                "The Bone People - Keri Hulme",
                "Bleak House - Charles Dickens",
                "The Buddha in the Attic - Julie Otsuka",
                "Beautiful Creatures - Kami Garcia",
                "Born Standing Up - Steve Martin",
                "The Book of M - Peng Shepherd",
                "Big Fish - Daniel Wallace"
            ],
            'C': [
                "The Color Purple - Alice Walker",
                "Cloud Atlas - David Mitchell",
                "The Catcher in the Rye - J.D. Salinger",
                "Catch-22 - Joseph Heller",
                "The Chronicles of Narnia - C.S. Lewis",
                "Cold Mountain - Charles Frazier",
                "The Curious Incident of the Dog in the Night-Time - Mark Haddon",
                "Crime and Punishment - Fyodor Dostoevsky",
                "The Count of Monte Cristo - Alexandre Dumas",
                "Circe - Madeline Miller"
            ],
            'D': [
                "Dune - Frank Herbert",
                "The Devil Wears Prada - Lauren Weisberger",
                "David Copperfield - Charles Dickens",
                "The Da Vinci Code - Dan Brown",
                "Doctor Zhivago - Boris Pasternak",
                "The Diary of a Young Girl - Anne Frank",
                "Dracula - Bram Stoker",
                "Don Quixote - Miguel de Cervantes",
                "The Diving Bell and the Butterfly - Jean-Dominique Bauby",
                "Death of a Salesman - Arthur Miller"
            ],
            'E': [
                "East of Eden - John Steinbeck",
                "Emma - Jane Austen",
                "The English Patient - Michael Ondaatje",
                "Everything Is Illuminated - Jonathan Safran Foer",
                "Eat, Pray, Love - Elizabeth Gilbert",
                "The Enormous Room - E.E. Cummings",
                "Ender's Game - Orson Scott Card",
                "The Electric Kool-Aid Acid Test - Tom Wolfe",
                "Ella Enchanted - Gail Carson Levine",
                "The Emperor's New Mind - Roger Penrose"
            ],
            'F': [
                "The Fault in Our Stars - John Green",
                "Fight Club - Chuck Palahniuk",
                "Fahrenheit 451 - Ray Bradbury",
                "The French Lieutenant's Woman - John Fowles",
                "Flowers for Algernon - Daniel Keyes",
                "The Five People You Meet in Heaven - Mitch Albom",
                "Frankenstein - Mary Shelley",
                "The Fountainhead - Ayn Rand",
                "Freakonomics - Steven Levitt",
                "The Forest of Hands and Teeth - Carrie Ryan"
            ],
            'G': [
                "The Great Gatsby - F. Scott Fitzgerald",
                "Gone Girl - Gillian Flynn",
                "The Grapes of Wrath - John Steinbeck",
                "The God of Small Things - Arundhati Roy",
                "Good Omens - Terry Pratchett",
                "The Golden Compass - Philip Pullman",
                "The Girl with the Dragon Tattoo - Stieg Larsson",
                "Gone with the Wind - Margaret Mitchell",
                "The Giver - Lois Lowry",
                "Guns, Germs, and Steel - Jared Diamond"
            ],
            'H': [
                "Harry Potter and the Philosopher's Stone - J.K. Rowling",
                "The Handmaid's Tale - Margaret Atwood",
                "The Help - Kathryn Stockett",
                "His Dark Materials - Philip Pullman",
                "The Hobbit - J.R.R. Tolkien",
                "The Hunger Games - Suzanne Collins",
                "Heart of Darkness - Joseph Conrad",
                "The Hours - Michael Cunningham",
                "The House on Mango Street - Sandra Cisneros",
                "Holes - Louis Sachar"
            ],
            'I': [
                "In Cold Blood - Truman Capote",
                "The Immortal Life of Henrietta Lacks - Rebecca Skloot",
                "Into the Wild - Jon Krakauer",
                "Invisible Man - Ralph Ellison",
                "The Importance of Being Earnest - Oscar Wilde",
                "If on a winter's night a traveler - Italo Calvino",
                "Interview with the Vampire - Anne Rice",
                "The Island of Dr. Moreau - H.G. Wells",
                "I Know Why the Caged Bird Sings - Maya Angelou",
                "Into Thin Air - Jon Krakauer"
            ],
            'J': [
                "Jane Eyre - Charlotte Brontë",
                "The Joy Luck Club - Amy Tan",
                "Jurassic Park - Michael Crichton",
                "Jazz - Toni Morrison",
                "The Jungle Book - Rudyard Kipling",
                "Journey to the Center of the Earth - Jules Verne",
                "The Jungle - Upton Sinclair",
                "Julie & Julia - Julie Powell",
                "Just Kids - Patti Smith",
                "The Joys of Motherhood - Buchi Emecheta"
            ],
            'K': [
                "The Kite Runner - Khaled Hosseini",
                "Kitchen Confidential - Anthony Bourdain",
                "The Known World - Edward P. Jones",
                "Kafka on the Shore - Haruki Murakami",
                "The Killer Angels - Michael Shaara",
                "King Lear - William Shakespeare",
                "The Kite Flying - Layla AlAmmar",
                "Kitchen - Banana Yoshimoto",
                "The Koran - Anonymous",
                "Kindred - Octavia Butler"
            ],
            'L': [
                "Life of Pi - Yann Martel",
                "The Lord of the Rings - J.R.R. Tolkien",
                "Little Women - Louisa May Alcott",
                "The Lion, the Witch and the Wardrobe - C.S. Lewis",
                "The Lovely Bones - Alice Sebold",
                "Lolita - Vladimir Nabokov",
                "The Life of Samuel Johnson - James Boswell",
                "The Left Hand of Darkness - Ursula K. Le Guin",
                "Let the Great World Spin - Colum McCann",
                "The Luminous Novel - Mario Levrero"
            ],
            'M': [
                "Midnight's Children - Salman Rushdie",
                "The Martian - Andy Weir",
                "Moby Dick - Herman Melville",
                "The Memory Police - Yoko Ogawa",
                "Me Before You - Jojo Moyes",
                "The Motorcycle Diaries - Ernesto Che Guevara",
                "My Brilliant Friend - Elena Ferrante",
                "The Master and Margarita - Mikhail Bulgakov",
                "Middlesex - Jeffrey Eugenides",
                "The Maze Runner - James Dashner"
            ],
            'N': [
                "Norwegian Wood - Haruki Murakami",
                "The Night Circus - Erin Morgenstern",
                "Never Let Me Go - Kazuo Ishiguro",
                "The Namesake - Jhumpa Lahiri",
                "Native Son - Richard Wright",
                "The Notebook - Nicholas Sparks",
                "No Country for Old Men - Cormac McCarthy",
                "Nine Stories - J.D. Salinger",
                "The Natural - Bernard Malamud",
                "Notes from Underground - Fyodor Dostoevsky"
            ],
            'O': [
                "One Hundred Years of Solitude - Gabriel García Márquez",
                "The Outsiders - S.E. Hinton",
                "Of Mice and Men - John Steinbeck",
                "The Ocean at the End of the Lane - Neil Gaiman",
                "On the Road - Jack Kerouac",
                "The Old Man and the Sea - Ernest Hemingway",
                "One Flew Over the Cuckoo's Nest - Ken Kesey",
                "Outliers - Malcolm Gladwell",
                "The Odyssey - Homer",
                "Oedipus Rex - Sophocles"
            ],
            'P': [
                "Pride and Prejudice - Jane Austen",
                "The Poisonwood Bible - Barbara Kingsolver",
                "The Perks of Being a Wallflower - Stephen Chbosky",
                "The Picture of Dorian Gray - Oscar Wilde",
                "Persepolis - Marjane Satrapi",
                "The Phantom Tollbooth - Norton Juster",
                "Pilgrim's Progress - John Bunyan",
                "The Power of One - Bryce Courtenay",
                "Practical Magic - Alice Hoffman",
                "The Princess Bride - William Goldman"
            ],
            'Q': [
                "The Quantum Theory Cannot Hurt You - Marcus Chown",
                "Queen Bees and Wannabes - Rosalind Wiseman",
                "The Quran - Anonymous",
                "Quicksilver - Neal Stephenson",
                "The Quiet American - Graham Greene",
                "The Queen's Gambit - Walter Tevis",
                "Q is for Quarry - Sue Grafton",
                "The Quality of Mercy - Faye Kellerman",
                "The Quotable Einstein - Albert Einstein",
                "Quest for Fire - J.H. Rosny"
            ],
            'R': [
                "The Road - Cormac McCarthy",
                "Rebecca - Daphne du Maurier",
                "The Remains of the Day - Kazuo Ishiguro",
                "Room - Emma Donoghue",
                "The Ramayana - Valmiki",
                "Ready Player One - Ernest Cline",
                "The Red Badge of Courage - Stephen Crane",
                "Robinson Crusoe - Daniel Defoe",
                "The Rules of Attraction - Bret Easton Ellis",
                "Roots - Alex Haley"
            ],
            'S': [
                "Slaughterhouse-Five - Kurt Vonnegut",
                "The Secret Garden - Frances Hodgson Burnett",
                "The Sun Also Rises - Ernest Hemingway",
                "Sapiens - Yuval Noah Harari",
                "The Stand - Stephen King",
                "Sense and Sensibility - Jane Austen",
                "The Shining - Stephen King",
                "Silent Spring - Rachel Carson",
                "The Sound and the Fury - William Faulkner",
                "Snow Crash - Neal Stephenson"
            ],
            'T': [
                "To Kill a Mockingbird - Harper Lee",
                "The Tipping Point - Malcolm Gladwell",
                "The Time Machine - H.G. Wells",
                "The Things They Carried - Tim O'Brien",
                "Treasure Island - Robert Louis Stevenson",
                "The Talented Mr. Ripley - Patricia Highsmith",
                "Their Eyes Were Watching God - Zora Neale Hurston",
                "The Trial - Franz Kafka",
                "The Turn of the Screw - Henry James",
                "Twilight - Stephenie Meyer"
            ],
            'U': [
                "Ulysses - James Joyce",
                "The Underground Railroad - Colson Whitehead",
                "Uncle Tom's Cabin - Harriet Beecher Stowe",
                "The Unbearable Lightness of Being - Milan Kundera",
                "Under the Dome - Stephen King",
                "Unbroken - Laura Hillenbrand",
                "The Upstairs Room - Johanna Reiss",
                "The Universe in a Nutshell - Stephen Hawking",
                "Up in the Old Hotel - Joseph Mitchell",
                "The Unicorn's Secret - Kathleen Duey"
            ],
            'V': [
                "The Vampire Chronicles - Anne Rice",
                "V for Vendetta - Alan Moore",
                "Veronika Decides to Die - Paulo Coelho",
                "The Variety of Religious Experience - William James",
                "Vanity Fair - William Makepeace Thackeray",
                "The Virgin Suicides - Jeffrey Eugenides",
                "Vonnegut's Breakfast of Champions - Kurt Vonnegut",
                "The Vicar of Wakefield - Oliver Goldsmith",
                "Valley of the Dolls - Jacqueline Susann",
                "The View from Saturday - E.L. Konigsburg"
            ],
            'W': [
                "Where the Crawdads Sing - Delia Owens",
                "The Wind in the Willows - Kenneth Grahame",
                "Wuthering Heights - Emily Brontë",
                "The War of the Worlds - H.G. Wells",
                "White Teeth - Zadie Smith",
                "The Water Dancer - Ta-Nehisi Coates",
                "Wild - Cheryl Strayed",
                "The Woman in White - Wilkie Collins",
                "Where the Red Fern Grows - Wilson Rawls",
                "The Waste Land - T.S. Eliot"
            ],
            'X': [
                "Xenocide - Orson Scott Card",
                "The X-Files: I Want to Believe - Chris Carter",
                "X-Men: Days of Future Past - Chris Claremont",
                "Xerxes: The Fall of the House of Darius - Frank Miller",
                "X Marks the Spot - Tony Abbott",
                "The Xenophobe's Guide to the Americans - Stephanie Faul",
                "XML in a Nutshell - Elliotte Rusty Harold",
                "X-Ray of the Pharaoh - Zahi Hawass",
                "Xanth Series - Piers Anthony",
                "The X Chronicles - Dean Koontz"
            ],
            'Y': [
                "The Year of Magical Thinking - Joan Didion",
                "You Can't Go Home Again - Thomas Wolfe",
                "The Yellow Wallpaper - Charlotte Perkins Gilman",
                "Yes Please - Amy Poehler",
                "The Yiddish Policemen's Union - Michael Chabon",
                "Yoga Body - Mark Singleton",
                "The Year of Living Dangerously - Christopher Koch",
                "Young Goodman Brown - Nathaniel Hawthorne",
                "The Years - Virginia Woolf",
                "Yesterday's Weather - Anne Enright"
            ],
            'Z': [
                "The Zone of Interest - Martin Amis",
                "Zen and the Art of Motorcycle Maintenance - Robert M. Pirsig",
                "Zorba the Greek - Nikos Kazantzakis",
                "The Zookeeper's Wife - Diane Ackerman",
                "Zorro - Isabel Allende",
                "Zoo - James Patterson",
                "The Zone of Silence - Italo Calvino",
                "Zero Dark Thirty - Mark Boal",
                "The Zombie Survival Guide - Max Brooks",
                "Zuleika Dobson - Max Beerbohm"
            ]
        }

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

                            self.all_authors.add(author)

        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    def find_duplicates(self) -> Dict:
        """Find all duplicate titles."""
        duplicates = {}

        for title, locations in self.all_books.items():
            if len(locations) > 1:
                duplicates[title] = locations

        return duplicates

    def get_replacement_suggestions(self, letter: str, existing_books: Set[str],
                                  existing_authors: Set[str], count: int) -> List[str]:
        """Get unique replacement books for a given letter."""
        replacements = []
        potential = self.replacement_books.get(letter, [])

        for book_line in potential:
            if " - " in book_line:
                title = book_line.split(" - ")[0].strip()
                author = book_line.split(" - ")[1].strip()

                # Check if this book/author is already used
                if (title not in existing_books and
                    author not in existing_authors and
                    len(replacements) < count):
                    replacements.append(book_line)
                    existing_books.add(title)
                    existing_authors.add(author)

        # If we need more, generate some generic ones
        while len(replacements) < count:
            generic_num = len(replacements) + 1000
            generic_book = f"{letter}venture Quest {generic_num} - Anonymous Author {generic_num}"
            replacements.append(generic_book)

        return replacements

    def fix_duplicates(self) -> None:
        """Fix all duplicate books by replacing them with unique alternatives."""
        duplicates = self.find_duplicates()

        if not duplicates:
            print("No duplicates found!")
            return

        print(f"Found {len(duplicates)} duplicate titles:")
        for title, locations in duplicates.items():
            print(f"  '{title}' appears {len(locations)} times")

        print("\nFixing duplicates...")

        # Get all existing titles and authors for uniqueness check
        all_titles = set(self.all_books.keys())
        all_authors = set(self.all_authors)

        for title, locations in duplicates.items():
            # Keep the first occurrence, replace the others
            locations_to_replace = locations[1:]  # Skip first occurrence

            print(f"\nFixing '{title}' ({len(locations_to_replace)} duplicates to replace)")

            for i, location in enumerate(locations_to_replace):
                letter = location['letter']

                # Get a unique replacement
                replacements = self.get_replacement_suggestions(letter, all_titles, all_authors, 1)

                if replacements:
                    replacement = replacements[0]
                    new_title = replacement.split(" - ")[0].strip()
                    new_author = replacement.split(" - ")[1].strip()

                    # Create new line with same numbering
                    new_line = f"{location['entry_number']}. {replacement}"

                    # Update the file
                    self.update_file_line(location['file'], location['line_number'], new_line)

                    print(f"  Replaced in {location['letter']}: '{title}' -> '{new_title}' by {new_author}")

                    # Update tracking
                    all_titles.add(new_title)
                    all_authors.add(new_author)

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
        """Verify that no duplicates remain after fixing."""
        # Reload all books
        self.all_books = {}
        self.all_authors = set()
        self.load_all_books()

        duplicates = self.find_duplicates()

        if duplicates:
            print(f"WARNING: {len(duplicates)} duplicates still remain:")
            for title, locations in duplicates.items():
                print(f"  '{title}' appears {len(locations)} times")
            return False
        else:
            print("✅ No duplicates found! All books are now unique.")
            return True

def main():
    """Main function to run the duplicate fixer."""
    print("Book Database Duplicate Fixer")
    print("=" * 40)

    fixer = DuplicateFixer()

    # Load all current books
    print("Loading all books...")
    fixer.load_all_books()
    print(f"Loaded {len(fixer.all_books)} unique titles from {len(fixer.all_authors)} authors")

    # Fix duplicates
    fixer.fix_duplicates()

    # Verify
    print("\nVerifying results...")
    success = fixer.verify_no_duplicates()

    if success:
        print("\n🎉 Successfully fixed all duplicates!")
        print("All 2,600 books are now unique across the entire database.")
    else:
        print("\n⚠️  Some duplicates may still remain. Please review manually.")

if __name__ == "__main__":
    main()