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
        Space out references in the text.
        Modifies self.text in-place.
        """
        pass


# Example usage
if __name__ == "__main__":
    # Test the function
    test_text = "Check this out: 👉 https://amzn.to/3MVo8SH and also 👉 https://example.com"
    # For testing purposes, we would need to create an MDWrangler instance
    print("Function converted to method. To test, create an MDWrangler instance.")