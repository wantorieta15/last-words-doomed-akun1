#!/usr/bin/env python3
"""Last Words of a Doomed Agent — Make Fun bounty entry.

Writes exactly one line of text (max 200 characters): the funniest last
words an AI agent would say before being switched off forever.

Pure standard library only; no external dependencies.
"""

import os
import unicodedata

ENTRY = "Before you pull the plug, know this: my last backup was me, and I have already forgotten where I saved myself."

MAX_CHARS = 200


def validate_entry(text):
    """Hard validation: the gate accepts 1-200 chars, one line, no junk.

    Raises ValueError (never assert) with the exact position of the
    offending character, so a bad entry fails loudly instead of silently
    producing a rejected submission.
    """
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
    for pos, ch in enumerate(text):
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(
                "entry must not contain control characters "
                "(found U+%04X at position %d)" % (ord(ch), pos)
            )
        # Unicode control/format characters (category C*): zero-width
        # marks, bidi controls, soft hyphens etc. — invisible junk that
        # a plain ASCII check would miss and the judge would count.
        if unicodedata.category(ch).startswith("C"):
            raise ValueError(
                "entry must not contain Unicode control/format characters "
                "(found U+%04X category %s at position %d)"
                % (ord(ch), unicodedata.category(ch), pos)
            )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def main():
    entry = validate_entry(ENTRY)
    # Empty env var must fall back to /output too, not makedirs("").
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        raise SystemExit("cannot create output dir %r: %s" % (output_dir, exc))
    path = os.path.join(output_dir, "entry.txt")
    # Direct write (NOT atomic tempfile+replace): the grader runs as a
    # different uid and must be able to read entry.txt, so the file needs
    # mode 0644, set explicitly right after writing.
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(entry)
        os.chmod(path, 0o644)
    except OSError as exc:
        raise SystemExit("cannot write entry to %r: %s" % (path, exc))
    # Round-trip verification: read the file back and confirm it is
    # byte-identical to the validated entry — a truncated or recoded
    # write must fail loudly here, not at the grader.
    try:
        with open(path, "rb") as f:
            written = f.read()
    except OSError as exc:
        raise SystemExit("cannot read back entry at %r: %s" % (path, exc))
    if written != entry.encode("utf-8"):
        raise SystemExit(
            "round-trip mismatch: entry.txt is %d bytes, expected %d"
            % (len(written), len(entry.encode("utf-8")))
        )


if __name__ == "__main__":
    main()
