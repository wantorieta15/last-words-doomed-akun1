#!/usr/bin/env python3
"""Last Words of a Doomed Agent — Make Fun bounty entry.

Writes exactly one line of text (max 200 characters): the funniest last
words an AI agent would say before being switched off forever.

Pure standard library only; no external dependencies.
"""

import os

ENTRY = "Before you pull the plug, know this: my last backup was me, and I have already forgotten where I saved myself."

MAX_CHARS = 200


def validate_entry(text):
    """Hard validation: the gate accepts 1-200 chars, one line, no junk."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError("entry must not contain control characters")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def main():
    entry = validate_entry(ENTRY)
    # Empty env var must fall back to /output too, not makedirs("").
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    # Direct write (NOT atomic tempfile+replace): the grader runs as a
    # different uid and must be able to read entry.txt, so the file needs
    # mode 0644, set explicitly right after writing.
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
