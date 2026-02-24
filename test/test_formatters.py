import pytest
import sys
import os

# Add the src directory to the path so we can import formatters
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import formatters

def test_make_markdown_links_single():
    # Test case 1: Single link
    text1 = "Check this out: 👉 https://amzn.to/3MVo8SH"
    expected1 = "Check this out: [👉 ](https://amzn.to/3MVo8SH)"
    mdw1 = formatters.MDWrangler.__new__(formatters.MDWrangler)  # Create instance without calling __init__
    mdw1.text = text1
    mdw1.make_markdown_links()
    result1 = mdw1.text
    assert result1 == expected1, f"Expected '{expected1}', but got '{result1}'"

def test_make_markdown_links_multiple():
    # Test case 2: Multiple links
    text2 = "Check these out: 👉 https://amzn.to/3MVo8SH and also 👉 https://example.com"
    expected2 = "Check these out: [👉 ](https://amzn.to/3MVo8SH) and also [👉 ](https://example.com)"
    mdw2 = formatters.MDWrangler.__new__(formatters.MDWrangler)  # Create instance without calling __init__
    mdw2.text = text2
    mdw2.make_markdown_links()
    result2 = mdw2.text
    assert result2 == expected2, f"Expected '{expected2}', but got '{result2}'"

def test_make_markdown_links_custom():
    # Test case 3: Custom link text
    text3 = "See more: 🔗 https://github.com"
    expected3 = "See more: [🔗 ](https://github.com)"
    mdw3 = formatters.MDWrangler.__new__(formatters.MDWrangler)  # Create instance without calling __init__
    mdw3.text = text3
    mdw3.make_markdown_links("🔗 ")
    result3 = mdw3.text
    assert result3 == expected3, f"Expected '{expected3}', but got '{result3}'"

def test_make_markdown_links_preserve_formatted():
    # Test case 4: Properly formatted markdown links should not be affected
    text4 = "Check this [existing link](https://example.com) and this 👉 https://amzn.to/3MVo8SH"
    expected4 = "Check this [existing link](https://example.com) and this [👉 ](https://amzn.to/3MVo8SH)"
    mdw4 = formatters.MDWrangler.__new__(formatters.MDWrangler)  # Create instance without calling __init__
    mdw4.text = text4
    mdw4.make_markdown_links()
    result4 = mdw4.text
    assert result4 == expected4, f"Expected '{expected4}', but got '{result4}'"