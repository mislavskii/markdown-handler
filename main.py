#!/usr/bin/env python3
"""
Markdown Link Formatter, Reference Spacer, and Timecode Spacer

This script provides three functionalities:
1. Convert link-containing text fragments into properly formatted Markdown links
   using the MDWrangler class.
2. Space out adjacent footnote references (e.g., [^1_5][^1_3] -> [^1_5] [^1_3]).
3. Space out timestamped transcript entries (e.g., "0:00" followed directly by
   content becomes its own paragraph).
"""

import os
from src.formatters import MDWrangler


def main() -> None:
    """
    Main function to handle user input and process the markdown file.
    """
    # Get the path to the Markdown file
    path = input("Enter the path to the Markdown file: ").strip()
    
    # Use default file if no path provided
    if not path:
        path = "What I've Learned Reading These 7 Books about AI.md"
        print(f"Using default file: {path}")
    
    # Validate file path
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        return
    
    if not os.path.isfile(path):
        print(f"Error: '{path}' is not a file.")
        return
    
    try:
        # Create MDWrangler instance
        mdw = MDWrangler(path)
        
        # Ask user which operation to perform
        print("\nSelect operation:")
        print("1. Format links (convert 👉 https://... to markdown links)")
        print("2. Space out footnote references (add spaces between adjacent [^...] references)")
        print("3. Space out timecodes (add blank lines around timestamp entries like 0:00)")
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice not in ("1", "2", "3"):
            print("Invalid choice. Exiting.")
            return
        
        # Get link text if needed
        link_text = "👉 "  # default
        if choice == "1":
            user_input = input("Enter the link text (e.g., '👉 '): ").strip()
            if user_input:
                link_text = user_input
            else:
                print(f"Using default link text: '{link_text}'")
        
        # Process the file
        print("Processing file...")
        if choice == "1":
            mdw.make_markdown_links(link_text)
        elif choice == "2":
            mdw.space_out_references()
        elif choice == "3":
            mdw.space_out_timecodes()
        output_path = mdw.save()
        
        print(f"File '{path}' processed and saved to '{output_path}'.")
        
    except PermissionError:
        print(f"Error: Permission denied when accessing '{path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()