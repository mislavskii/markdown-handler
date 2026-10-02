import re


class MDWrangler:

    def __init__(self, path: str) -> None:
        self.path = path
        self.load_file(path)

    def load_file(self, path):
        with open(path, 'r') as f:
            text = f.read()
        self.text = text

    def save(self):
        with open(self.path, 'w') as f:
            f.write(self.text)

    def make_markdown_links(self, link_text="👉 "):
        """
        Convert link-containing text fragments into markdown formatted links.
        Modifies self.text in-place.
        
        Args:
            link_text (str): The text to use in square brackets for each link (default: "👉 ")
        """
        # Pattern to match link fragments with the specified format
        pattern = rf'({re.escape(link_text)}\s*)(https?://[^\s]+)'
        
        def replace_link(match):
            # Extract the link part (second group)
            link = match.group(2)
            # Return the markdown formatted link
            return f'[{link_text}]({link})'
        
        # Replace all matches with markdown formatted links
        self.text = re.sub(pattern, replace_link, self.text)

    def space_out_references(self):
        """
        Space out footnote references in the text.
        
        Finds adjacent footnote references (e.g., [^1_5][^1_3]) and inserts a space
        between them, resulting in [^1_5] [^1_3]. Already spaced references are left
        unchanged. Works for any number of adjacent references.
        
        Modifies self.text in-place.
        """
        import re
        # Pattern for footnote references: [^...]
        # Replace adjacent references without spaces with a space between them
        pattern = r'(\[\^[^\]]*\])(\[\^[^\]]*\])'
        while True:
            new_text = re.sub(pattern, r'\1 \2', self.text)
            if new_text == self.text:
                break
            self.text = new_text

    def space_out_timecodes(self):
        """
        Space out timestamped transcript entries in the text.

        Finds standalone timestamp lines (e.g., "0:00" or "12:34:56") that are
        adjacent to other text and inserts blank lines around them, so each
        timecode and its content form their own paragraph:

            "0:00\ncontent\n0:29\ncontent"
                -> "0:00\n\ncontent\n\n0:29\n\ncontent"

        Already spaced timestamps are left unchanged, and repeated blank lines
        are collapsed into a single blank line. Timestamps embedded within a
        sentence (e.g., "at 0:00 for details") are not treated as timecode
        lines. No leading blank line is introduced at the start of the document
        and no trailing blank line is left at the end.

        Modifies self.text in-place.
        """
        import re
        # Pattern for a standalone timestamp line: mm:ss or hh:mm:ss
        timestamp_pattern = re.compile(r'^\s*\d{1,2}:\d{2}(?::\d{2})?\s*$')

        lines = self.text.split('\n')
        result = []
        prev_blank = True  # treat document start as blank to avoid a leading empty line
        for line in lines:
            is_timestamp = bool(timestamp_pattern.match(line))
            is_blank = not line.strip()
            if is_timestamp:
                if not prev_blank:
                    result.append('')
                result.append(line)
                result.append('')
                prev_blank = True
            elif is_blank:
                if not prev_blank:
                    result.append('')
                prev_blank = True
            else:
                result.append(line)
                prev_blank = False

        # Remove any trailing blank lines introduced
        while result and result[-1] == '':
            result.pop()

        self.text = '\n'.join(result)


# Example usage
if __name__ == "__main__":
    # Test the function
    test_text = "Check this out: 👉 https://amzn.to/3MVo8SH and also 👉 https://example.com"
    # For testing purposes, we would need to create an MDWrangler instance
    print("Function converted to method. To test, create an MDWrangler instance.")