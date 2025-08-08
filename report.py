from typing import Dict


class ResultAggregator:
    """Collect statistics from analyzers and consolidate them."""

    def __init__(self) -> None:
        self._results: Dict[str, Dict[str, Dict[str, float]]] = {}

    def add(self, name: str, stats: Dict[str, Dict[str, float]]) -> None:
        self._results[name] = stats

    def consolidate(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        return self._results
