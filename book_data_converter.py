#!/usr/bin/env python3
"""
Book Database to CSV Converter
Converts the markdown book database files (A-Z) into structured CSV format for data analysis.
"""

import os
import re
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import Counter

class BookDataConverter:
    def __init__(self):
        self.books_data = []
        self.unique_authors = set()
        self.duplicate_titles = []

    def parse_book_entry(self, line: str, letter: str) -> Optional[Dict]:
        """Parse a single book entry from markdown format."""
        line = line.strip()

        # Pattern: Number. Title - Author
        pattern = r'^(\d+)\.\s+(.+?)\s+-\s+(.+)$'
        match = re.match(pattern, line)

        if not match:
            return None

        number, title, author = match.groups()

        return {
            'title': title.strip(),
            'author': author.strip(),
            'letter': letter.upper(),
            'entry_number': int(number),
            'title_length': len(title.strip()),
            'author_last_name': self.extract_last_name(author.strip())
        }

    def extract_last_name(self, author: str) -> str:
        """Extract the last name from author for sorting purposes."""
        # Handle cases like "Dr. Seuss", "J.K. Rowling", etc.
        parts = author.split()
        if len(parts) == 0:
            return author

        # Return the last part (surname)
        return parts[-1]

    def extract_genre_hints(self, title: str, author: str) -> List[str]:
        """Extract possible genre hints from title and author."""
        genres = []

        title_lower = title.lower()
        author_lower = author.lower()

        # Genre indicators in titles
        if any(word in title_lower for word in ['mystery', 'murder', 'detective', 'crime']):
            genres.append('Mystery/Crime')
        if any(word in title_lower for word in ['love', 'heart', 'romance']):
            genres.append('Romance')
        if any(word in title_lower for word in ['war', 'battle', 'soldier', 'army']):
            genres.append('War/Military')
        if any(word in title_lower for word in ['history', 'biography', 'life of', 'memoir']):
            genres.append('Biography/History')
        if any(word in title_lower for word in ['science', 'space', 'future', 'robot']):
            genres.append('Science Fiction')
        if any(word in title_lower for word in ['magic', 'dragon', 'wizard', 'fantasy']):
            genres.append('Fantasy')
        if any(word in title_lower for word in ['children', 'kid', 'little']):
            genres.append('Children')

        # Well-known genre authors
        if any(name in author_lower for name in ['christie', 'doyle', 'chandler']):
            genres.append('Mystery/Crime')
        if any(name in author_lower for name in ['asimov', 'bradbury', 'clarke']):
            genres.append('Science Fiction')
        if any(name in author_lower for name in ['tolkien', 'lewis', 'gaiman']):
            genres.append('Fantasy')
        if any(name in author_lower for name in ['seuss', 'dahl', 'potter']):
            genres.append('Children')

        return genres if genres else ['General Fiction']

    def process_file(self, filepath: str) -> List[Dict]:
        """Process a single markdown file and extract book data."""
        filename = os.path.basename(filepath)

        # Extract letter from filename (books_A.md -> A)
        if not filename.startswith('books_') or not filename.endswith('.md'):
            return []

        letter = filename.replace('books_', '').replace('.md', '')
        books = []

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

                for line in content.split('\n'):
                    line = line.strip()

                    # Parse book entries
                    if re.match(r'^\d+\.', line):
                        book = self.parse_book_entry(line, letter)
                        if book:
                            # Add genre hints
                            book['genre_hints'] = ' | '.join(
                                self.extract_genre_hints(book['title'], book['author'])
                            )
                            books.append(book)

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

        return books

    def process_all_files(self) -> None:
        """Process all book database files."""
        current_dir = Path('.')

        # Process files A-Z in order
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            file_path = current_dir / f'books_{letter}.md'
            if file_path.exists():
                print(f"Processing books_{letter}.md...")
                books = self.process_file(str(file_path))
                self.books_data.extend(books)
                print(f"  Found {len(books)} entries")

                # Track unique authors
                for book in books:
                    self.unique_authors.add(book['author'])

    def analyze_duplicates(self) -> Dict:
        """Analyze duplicate titles and popular authors."""
        title_counts = Counter(book['title'] for book in self.books_data)
        author_counts = Counter(book['author'] for book in self.books_data)

        duplicates = {title: count for title, count in title_counts.items() if count > 1}
        popular_authors = author_counts.most_common(10)

        return {
            'duplicate_titles': duplicates,
            'popular_authors': popular_authors,
            'total_unique_titles': len(title_counts),
            'total_unique_authors': len(author_counts)
        }

    def save_to_csv(self, output_file: str = 'book_database.csv') -> None:
        """Save processed data to CSV file."""
        if not self.books_data:
            print("No data to save!")
            return

        # Create main dataset
        df = pd.DataFrame(self.books_data)

        # Sort by letter and entry number
        df = df.sort_values(['letter', 'entry_number'])

        df.to_csv(output_file, index=False, encoding='utf-8')

        print(f"\nSuccessfully created CSV file:")
        print(f"  {output_file} ({len(self.books_data)} entries)")

        # Create author-focused dataset
        author_file = output_file.replace('.csv', '_by_authors.csv')
        df_authors = df.sort_values(['author_last_name', 'author', 'title'])
        df_authors.to_csv(author_file, index=False, encoding='utf-8')

        print(f"  {author_file} (sorted by author)")

        # Print summary statistics
        analysis = self.analyze_duplicates()
        print(f"\nSummary Statistics:")
        print(f"  Total books: {len(self.books_data)}")
        print(f"  Unique titles: {analysis['total_unique_titles']}")
        print(f"  Unique authors: {analysis['total_unique_authors']}")
        print(f"  Duplicate titles: {len(analysis['duplicate_titles'])}")

        if analysis['duplicate_titles']:
            print(f"\n  Most duplicated titles:")
            for title, count in sorted(analysis['duplicate_titles'].items(),
                                     key=lambda x: x[1], reverse=True)[:5]:
                print(f"    '{title}' appears {count} times")

        print(f"\n  Most prolific authors:")
        for author, count in analysis['popular_authors'][:5]:
            print(f"    {author}: {count} books")

    def generate_analysis_report(self) -> None:
        """Generate a comprehensive analysis report."""
        if not self.books_data:
            return

        df = pd.DataFrame(self.books_data)

        print(f"\nDetailed Analysis Report:")

        # Books per letter
        print(f"  Books by Starting Letter:")
        letter_counts = df['letter'].value_counts().sort_index()
        for letter, count in letter_counts.items():
            print(f"    {letter}: {count}")

        # Title length analysis
        avg_title_length = df['title_length'].mean()
        max_title = df.loc[df['title_length'].idxmax()]
        min_title = df.loc[df['title_length'].idxmin()]

        print(f"\n  Title Length Analysis:")
        print(f"    Average title length: {avg_title_length:.1f} characters")
        print(f"    Longest title: '{max_title['title']}' ({max_title['title_length']} chars)")
        print(f"    Shortest title: '{min_title['title']}' ({min_title['title_length']} chars)")

        # Genre distribution
        genre_counts = Counter()
        for book in self.books_data:
            for genre in book['genre_hints'].split(' | '):
                genre_counts[genre.strip()] += 1

        print(f"\n  Estimated Genre Distribution:")
        for genre, count in genre_counts.most_common(8):
            print(f"    {genre}: {count} books")

def main():
    """Main function to run the converter."""
    print("Book Database to CSV Converter")
    print("=" * 40)

    converter = BookDataConverter()

    # Process all files
    converter.process_all_files()

    # Save to CSV
    converter.save_to_csv()

    # Generate analysis report
    converter.generate_analysis_report()

    print("\nConversion completed successfully!")
    print("\nFiles created:")
    print("  - book_database.csv - All books sorted by letter")
    print("  - book_database_by_authors.csv - All books sorted by author")
    print("\nThese CSV files are now ready for data analysis and research!")

if __name__ == "__main__":
    main()