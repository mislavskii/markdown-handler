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

def test_space_out_references_single_pair():
    # Test case: Two adjacent references
    text = "Check this [^1_5][^1_3] and more"
    expected = "Check this [^1_5] [^1_3] and more"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_three_adjacent():
    # Three adjacent references
    text = "[^a][^b][^c]"
    expected = "[^a] [^b] [^c]"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_already_spaced():
    # Already spaced references should stay unchanged
    text = "[^foo] [^bar]"
    expected = "[^foo] [^bar]"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_mixed_spacing():
    # Mixed spacing
    text = "[^x][^y] [^z]"
    expected = "[^x] [^y] [^z]"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_no_references():
    # No references
    text = "Hello world"
    expected = "Hello world"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_with_underscores():
    # References with underscores
    text = "[^1_5][^2_3]"
    expected = "[^1_5] [^2_3]"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_with_hyphens():
    # References with hyphens
    text = "[^foo-bar][^baz-qux]"
    expected = "[^foo-bar] [^baz-qux]"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_references_adjacent_to_text():
    # References adjacent to other text
    text = "text[^1][^2]text"
    expected = "text[^1] [^2]text"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_references()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_single_entry():
    # Single timestamped entry: timecode and content become separate paragraphs
    text = "0:00\nសូមជម្រាបសួរប្រិយមិត្ត"
    expected = "0:00\n\nសូមជម្រាបសួរប្រិយមិត្ត"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_multiple_entries():
    # Multiple entries should each become their own paragraph
    text = "0:00\nfirst content\n0:29\nsecond content\n0:59\nthird content"
    expected = "0:00\n\nfirst content\n\n0:29\n\nsecond content\n\n0:59\n\nthird content"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_already_spaced():
    # Already spaced timecodes should stay unchanged (idempotent)
    text = "0:00\n\nfirst content\n\n0:29\n\nsecond content"
    expected = "0:00\n\nfirst content\n\n0:29\n\nsecond content"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_no_timestamps():
    # Text without timestamps should stay unchanged
    text = "Hello world\nplain text"
    expected = "Hello world\nplain text"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_with_hours():
    # Timestamps with an hours component (hh:mm:ss)
    text = "12:34:56\ncontent"
    expected = "12:34:56\n\ncontent"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_at_file_start():
    # No leading blank line should be introduced
    text = "0:00\ncontent"
    expected = "0:00\n\ncontent"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_at_file_end():
    # No trailing blank line should be left behind
    text = "content\n0:59"
    expected = "content\n\n0:59"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_mixed_spacing():
    # Some entries already spaced, some not
    text = "0:00\n\nfirst\n0:29\nsecond"
    expected = "0:00\n\nfirst\n\n0:29\n\nsecond"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_after_heading():
    # Timecode after a markdown heading gets a blank line between them
    text = "## Sophearyn Hang\n0:00\ncontent"
    expected = "## Sophearyn Hang\n\n0:00\n\ncontent"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_embedded_in_text():
    # A timestamp embedded within a sentence must not be treated as a timecode line
    text = "See the video at 0:00 for the intro"
    expected = "See the video at 0:00 for the intro"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_collapses_extra_blank_lines():
    # Repeated blank lines should be collapsed into a single blank line
    text = "0:00\n\n\n\ncontent"
    expected = "0:00\n\ncontent"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_adjacent_timestamps():
    # Two timestamps with no content between them get a single blank line
    text = "0:00\n0:30"
    expected = "0:00\n\n0:30"
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"

def test_space_out_timecodes_khmer_transcript():
    # Realistic excerpt mirroring the Khmer transcript file structure
    text = ("# Title\n"
            "\n"
            "## Sophearyn Hang\n"
            "0:00\n"
            "សូមជម្រាបសួរប្រិយមិត្ត\n"
            "0:29\n"
            "ថ្ងៃនេះរៀងគួរឲ្យចាប់អារម្មណ៍\n"
            "0:59\n"
            "ទស្សនាទាំងអស់គ្នា")
    expected = ("# Title\n"
                "\n"
                "## Sophearyn Hang\n"
                "\n"
                "0:00\n"
                "\n"
                "សូមជម្រាបសួរប្រិយមិត្ត\n"
                "\n"
                "0:29\n"
                "\n"
                "ថ្ងៃនេះរៀងគួរឲ្យចាប់អារម្មណ៍\n"
                "\n"
                "0:59\n"
                "\n"
                "ទស្សនាទាំងអស់គ្នា")
    mdw = formatters.MDWrangler.__new__(formatters.MDWrangler)
    mdw.text = text
    mdw.space_out_timecodes()
    result = mdw.text
    assert result == expected, f"Expected '{expected}', but got '{result}'"