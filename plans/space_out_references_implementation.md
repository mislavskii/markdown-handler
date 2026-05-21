# Implementation Plan for `space_out_references` Method

## Objective
Add spaces between adjacent footnote references in markdown text, e.g., convert `[^1_5][^1_3]` to `[^1_5] [^1_3]`.

## Assumptions
- Only footnote references (starting with `[^`) are targeted.
- Existing spaces between references should be left untouched.
- Multiple adjacent references (e.g., `[^a][^b][^c]`) should become `[^a] [^b] [^c]`.
- References may contain underscores, numbers, letters, hyphens, etc. inside the brackets.
- The method modifies `self.text` in-place, similar to `make_markdown_links`.

## Implementation Details

### Regex Pattern
Pattern to match two adjacent footnote references without spaces:
```
(\[\^[^\]]*\])(\[\^[^\]]*\])
```
- `\[\^` matches literal `[^`
- `[^\]]*` matches any character except `]` (non-greedy)
- `\]` matches closing bracket
- Capture groups allow us to insert a space between them.

### Algorithm
Because there may be more than two adjacent references, we apply the substitution repeatedly until no change occurs.

```python
def space_out_references(self):
    import re
    pattern = r'(\[\^[^\]]*\])(\[\^[^\]]*\])'
    while True:
        new_text = re.sub(pattern, r'\1 \2', self.text)
        if new_text == self.text:
            break
        self.text = new_text
```

### Edge Cases
1. **Already spaced references**: `[^a] [^b]` → unchanged.
2. **Mixed spacing**: `[^a][^b] [^c]` → `[^a] [^b] [^c]` (space inserted between a and b).
3. **No references**: text remains unchanged.
4. **References inside code blocks or links**: Should we ignore? The regex will still match because it doesn't consider context. This may be acceptable as footnote references inside code blocks are rare. Could be a future improvement.

## Test Cases

### Unit Tests (to be added to `test/test_formatters.py`)
1. **Single pair**: `[^1_5][^1_3]` → `[^1_5] [^1_3]`
2. **Three adjacent**: `[^a][^b][^c]` → `[^a] [^b] [^c]`
3. **Already spaced**: `[^a] [^b]` → unchanged
4. **Mixed spacing**: `[^a][^b] [^c]` → `[^a] [^b] [^c]`
5. **No references**: `Hello world` → unchanged
6. **References with underscores**: `[^1_5][^2_3]` → `[^1_5] [^2_3]`
7. **References with hyphens**: `[^foo-bar][^baz-qux]` → `[^foo-bar] [^baz-qux]`
8. **References with numbers**: `[^1][^2]` → `[^1] [^2]`
9. **References adjacent to other text**: `text[^a][^b]text` → `text[^a] [^b]text`
10. **Multiple lines**: Should work across newlines? The regex uses `.` which doesn't match newline, but pattern uses `[^\]]*` which does not include newline? Actually `[^\]]` matches any character except `]`, including newline. That's fine.

### Integration Test
- Load a sample markdown file with adjacent references, run the method, verify spaces inserted correctly.

## Next Steps
1. Switch to **Code mode** to edit `src/formatters.py` and implement the method.
2. Add unit tests to `test/test_formatters.py`.
3. Run existing tests to ensure no regression.
4. Optionally update the main script to optionally call this method.

## Questions for User
- Should we also handle regular citation references (e.g., `[1]`, `[Smith2020]`)?
- Should we ignore references inside code blocks (```) or inline code (`...`)?
- Any performance concerns with while loop? (Likely fine as references are few.)