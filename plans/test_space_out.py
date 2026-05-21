#!/usr/bin/env python3
"""
Test the space_out_references method on a sample markdown file.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import formatters

def test_sample():
    # Read the sample file
    with open('plans/test_references.md', 'r') as f:
        content = f.read()
    print("Original content:")
    print(content)
    print("\n---\n")
    
    # Create MDWrangler instance (without loading from file)
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = content
    mdw.space_out_references()
    
    print("After space_out_references:")
    print(mdw.text)
    
    # Check if changes are as expected
    # We'll just print a diff
    import difflib
    diff = list(difflib.unified_diff(content.splitlines(), mdw.text.splitlines(), lineterm=''))
    if diff:
        print("\nChanges:")
        for line in diff:
            print(line)
    else:
        print("\nNo changes.")

if __name__ == '__main__':
    test_sample()