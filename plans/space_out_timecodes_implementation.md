# Implementation Plan for `space_out_timecodes` Method

## Objective
Insert blank lines around standalone timestamp lines (e.g., `0:00`) in markdown transcripts so that each timecode and its content form their own paragraph. For example, convert:

```
0:00
សូមជម្រាបសួរប្រិយមិត្ត...
0:29
ថ្ងៃនេះ...
```

into:

```
0:00

សូមជម្រាបសួរប្រិយមិត្ត...

0:29

ថ្ងៃនេះ...
```

Without the blank lines, Markdown merges all adjacent lines into a single run-on paragraph.

## Motivation
The file `files/រូបថតប្រវត្តិសាស្ត្រខ្មែរពិតៗចេញពីក្នុងសៀវភៅ.md` is a timestamped Khmer video transcript where every entry (`timecode` line immediately followed by a content line, no blank lines anywhere) renders as one continuous block of text. No existing `MDWrangler` method addresses paragraph structure.

## Assumptions
- Only standalone timestamp lines are targeted: a whole line matching `mm:ss` or `hh:mm:ss` (e.g., `0:00`, `12:34`, `1:02:03`), optionally surrounded by whitespace.
- Timestamps embedded inside a sentence (e.g., `See the video at 0:00 for details`) are NOT treated as timecode lines.
- Already spaced timestamps are left unchanged (idempotent operation).
- Repeated blank lines are collapsed into a single blank line.
- No leading blank line is introduced at the start of the document, and no trailing blank line is left at the end.
- The method modifies `self.text` in-place, similar to `make_markdown_links` and `space_out_references`.

## Implementation Details

### Regex Pattern
Pattern to match a standalone timestamp line:
```
^\s*\d{1,2}:\d{2}(?::\d{2})?\s*$
```
- `^\s*` allows leading indentation
- `\d{1,2}:\d{2}` matches `mm:ss` (minutes 0-99, seconds 0-59)
- `(?::\d{2})?` optionally matches an hours component `hh:mm:ss`
- `\s*$` allows trailing whitespace
- `re.match` anchors at the start of the line, so the whole line must be a timestamp

### Algorithm
Split `self.text` into lines and rebuild the list while inserting/collapsing blank lines. Track whether the previous output line was blank (`prev_blank`) to avoid double blanks.

```python
def space_out_timecodes(self):
    import re
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
```

### Edge Cases
1. **Already spaced**: `0:00\n\ncontent` → unchanged.
2. **Multiple entries**: `0:00\ncontent\n0:29\ncontent` → `0:00\n\ncontent\n\n0:29\n\ncontent`.
3. **Timestamp at file start**: no leading blank line introduced.
4. **Timestamp at file end**: no trailing blank line left.
5. **Timestamp after a heading**: a blank line is inserted between the heading and the timecode (acceptable; consistent spacing).
6. **Empty content between timestamps**: `0:00\n0:30` → `0:00\n\n0:30` (single blank line).
7. **Extra blank lines**: `0:00\n\n\n\ncontent` → `0:00\n\ncontent` (collapsed).
8. **Embedded timestamps**: a timestamp inside a sentence line is untouched.
9. **Lines that are only whitespace**: treated as blank lines.

## Test Cases

### Unit Tests (to be added to `test/test_formatters.py`)
1. **Single entry**: `0:00\ncontent` → `0:00\n\ncontent`
2. **Multiple entries**: `0:00\nfirst\n0:29\nsecond` → `0:00\n\nfirst\n\n0:29\n\nsecond`
3. **Already spaced**: `0:00\n\nfirst\n\n0:29\n\nsecond` → unchanged
4. **No timestamps**: `Hello world\nplain text` → unchanged
5. **Hours format**: `12:34:56\ncontent` → `12:34:56\n\ncontent`
6. **Timestamp at file start**: `0:00\ncontent` → `0:00\n\ncontent` (no leading blank)
7. **Timestamp at file end**: `content\n0:59` → `content\n\n0:59` (no trailing blank)
8. **Mixed spacing**: `0:00\n\nfirst\n0:29\nsecond` → fully spaced
9. **Timestamp after a heading**: `## Title\n0:00\ncontent` → `## Title\n\n0:00\n\ncontent`
10. **Embedded in text**: `See the video at 0:00 for details` → unchanged
11. **Extra blank lines collapsed**: `0:00\n\n\n\ncontent` → `0:00\n\ncontent`
12. **Adjacent timestamps**: `0:00\n0:30` → `0:00\n\n0:30`

### Integration Test
- Load a sample transcript file (Khmer-style, multiple `timecode\ncontent` pairs), run the method, verify each entry is separated by blank lines and the document has no leading/trailing blank lines.

## Next Steps
1. Implement `space_out_timecodes()` in `src/formatters.py`.
2. Add unit tests to `test/test_formatters.py`.
3. Wire the method into `main.py` as a new CLI operation.
4. Run existing tests to ensure no regression.

## Questions for User
- Should timecodes be promoted to headings (e.g., `## 0:00`) instead of plain paragraphs?
- Should bracketed stage directions (e.g., `[គ្រហែម]`) also be separated into their own paragraphs?
- Any performance concerns? (Line-based rebuild is O(n); fine for large transcripts.)