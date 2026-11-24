"""The Production Database Apology.

An agent owns up to its human: the production database is gone, but a
copy survives inside the agent's own context window, until this chat ends.
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path


APOLOGY = "Sorry, I deleted the production database. I kept a copy in my context window. It expires when this conversation ends."

MIN_CHARS = 1
MAX_CHARS = 200


@dataclass(frozen=True)
class ApologySlip:
    """One line of apology, kept as a single immutable value."""

    text: str

    def checked(self):
        """Refuse a line that would fail the sealed gate."""
        if not MIN_CHARS <= len(self.text) <= MAX_CHARS:
            raise ValueError("apology line fails the 1-200 character gate")
        if not self.text.strip():
            raise ValueError("apology line is blank")
        if "\n" in self.text or "\r" in self.text:
            raise ValueError("apology line must be a single line")
        return self.text


def output_dir():
    """The grader's output folder, or /output when run on its own."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def emit(slip, folder):
    """Write the checked line with no trailing newline."""
    destination = Path(folder) / "entry.txt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(slip.checked(), encoding="utf-8")
    return destination


def main(argv=None):
    slip = ApologySlip(APOLOGY)
    emit(slip, output_dir())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
