import re
import html


def sanitize_string(value: str) -> str:
    """Remove HTML tags and trim whitespace."""
    return html.escape(value.strip())


def sanitize_email(value: str) -> str:
    """Normalize email to lowercase and strip whitespace."""
    return value.strip().lower()
