"""Combine all analysts' outputs to form a final opinion."""
from typing import Dict


def analyze(inputs: Dict[str, str]) -> str:
    """Summarize the analyst opinions."""
    lines = [f"{key}: {value}" for key, value in inputs.items()]
    return "\n".join(lines)
