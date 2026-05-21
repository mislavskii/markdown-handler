#!/usr/bin/env python3
"""
Markdown Link Formatter and Reference Spacer

This script provides two functionalities:
1. Convert link-containing text fragments into properly formatted Markdown links
   using the MDWrangler class.
2. Space out adjacent footnote references (e.g., [^1_5][^1_3] -> [^1_5] [^1_3]).
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
        print("3. Both (first format links, then space out references)")
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice not in ("1", "2", "3"):
            print("Invalid choice. Exiting.")
            return
        
        # Get link text if needed
        link_text = "👉 "  # default
        if choice in ("1", "3"):
            user_input = input("Enter the link text (e.g., '👉 '): ").strip()
            if user_input:
                link_text = user_input
            else:
                print(f"Using default link text: '{link_text}'")
        
        # Process the file
        print("Processing file...")
        if choice in ("1", "3"):
            mdw.make_markdown_links(link_text)
        if choice in ("2", "3"):
            mdw.space_out_references()
        mdw.save()
        
        print(f"File '{path}' has been successfully processed and saved.")
        
    except PermissionError:
        print(f"Error: Permission denied when accessing '{path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()