from dataclasses import dataclass


@dataclass
class SearchMatch:
    context: str
    line_number: int
    matched_text: str
