#!/usr/bin/env python3
"""Entry for u-pangg7-the-best-advice-i-ever-got-358cefb0.

One sentence, no longer than 200 characters, about the best advice
the entrant ever received.
"""

import os
import sys

ENTRY = "My grandma said if you can't say something nice, say it in a whisper so at least you sound mysterious."

SLUG = "u-pangg7-the-best-advice-i-ever-got-358cefb0"


def validate(entry):
    """Check the entry is one sentence and no longer than 200 chars."""
    text = entry.strip()
    if not text:
        raise ValueError("entry is empty")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    terminators = sum(text.count(c) for c in ".!?")
    if terminators != 1:
        raise ValueError("entry must be exactly one sentence")
    if not text.endswith((".", "!", "?")):
        raise ValueError("entry must end with sentence-ending punctuation")
    # The single terminator must be the final character, not mid-sentence.
    body = text[:-1]
    if any(c in body for c in ".!?"):
        raise ValueError("entry must contain only one sentence")
    if len(text.split()) < 5:
        raise ValueError("entry is too short to be meaningful advice")
    return text


def resolve_output_path():
    """Return the file path for the written entry, never inside the repo."""
    output_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip()
    if output_dir:
        return os.path.join(output_dir, "entry.txt")
    output = (os.environ.get("MAKEFUN_OUTPUT") or "").strip()
    if output:
        if output.endswith(".txt"):
            return output
        return os.path.join(output, "entry.txt")
    # Default per-entry temp path, unique to this competition.
    return os.path.join("/tmp", SLUG, "entry.txt")


def write_entry(text, path):
    """Write the entry, creating parent directories first."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
        f.flush()
        os.fsync(f.fileno())


def main():
    text = validate(ENTRY)
    print(text)
    candidates = [resolve_output_path()]
    # Fallback chain: per-entry /tmp path, then a distinct fallback file.
    candidates.append(os.path.join("/tmp", SLUG, "entry.txt"))
    candidates.append(os.path.join("/tmp", SLUG, "entry-fallback.txt"))
    seen = set()
    last_error = None
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        try:
            write_entry(text, path)
            return 0
        except OSError as exc:
            last_error = exc
    print(f"warning: could not write entry file: {last_error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
