import csv
from dataclasses import dataclass
from datetime import datetime
from prettytable import PrettyTable
from tkinter import Tk
from tkinter.filedialog import askopenfilename


@dataclass
class SongData:
    """Represents a single song entry from the Exportify CSV."""

    name: str
    album: str
    artist: str
    date_added: str


def parse_date(date_str: str) -> str:
    """Convert ISO datetime to readable format, fallback to raw string if invalid."""
    try:
        return datetime.fromisoformat(date_str).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return date_str  # Return as-is if parsing fails


def main():
    """Find duplicate songs in an Exportify CSV file."""
    # Hide root Tk window
    Tk().withdraw()

    # Ask user to pick CSV file
    filename = askopenfilename(
        title="Select an Exportify CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
    )

    if not filename:
        print("No file selected.")
        return

    # Dictionary: "name | artist" -> list of SongData
    duplicates: dict[str, list[SongData]] = {}

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            # Create a song data object for the relevant parts
            song = SongData(
                name=row[1],
                album=row[2],
                artist=row[3],
                date_added=row[9],
            )

            # Add to duplicates list
            key = song.name + " | " + song.artist
            duplicates.setdefault(key, []).append(song)

    # Prepare output table
    table = PrettyTable(["Name", "Artist", "Album", "Date Added"])

    for songs in duplicates.values():
        # Skip non-duplicates
        if len(songs) == 1:
            continue

        # Insert blank line between groups
        if len(table.rows) > 0:
            table.add_row(["", "", "", ""])

        # Add each song to the output table
        for song in songs:
            table.add_row(
                [
                    song.name,
                    song.artist,
                    song.album,
                    parse_date(song.date_added),
                ]
            )

    # Display the duplicates output
    if len(table.rows) == 0:
        print("No duplicate songs.")
        return
    print("\nDuplicate Songs\n")
    print(table)


if __name__ == "__main__":
    main()
