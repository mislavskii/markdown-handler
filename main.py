#!/usr/bin/env python3
"""
Markdown Link Formatter

This script converts link-containing text fragments into properly formatted
Markdown links using the MDWrangler class.
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
        
        # Get the link text to look for
        link_text = input("Enter the link text (e.g., '👉 '): ")#.strip()
        
        # Use default link text if none provided
        if not link_text:
            link_text = "👉 "
            print(f"Using default link text: '{link_text}'")
        
        # Process the file
        print("Processing file...")
        mdw.make_markdown_links(link_text)
        mdw.save()
        
        print(f"File '{path}' has been successfully processed and saved.")
        
    except PermissionError:
        print(f"Error: Permission denied when accessing '{path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()