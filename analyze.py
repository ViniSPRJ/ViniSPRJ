from typing import Dict, List


class StatsAnalyzer:
    """Compute basic statistics for numeric columns."""

    def __init__(self):
        self._sum: Dict[str, float] = {}
        self._count: Dict[str, int] = {}
        self._min: Dict[str, float] = {}
        self._max: Dict[str, float] = {}

    def process(self, rows: List[Dict[str, str]]) -> None:
        for row in rows:
            for key, value in row.items():
                try:
                    num = float(value)
                except (TypeError, ValueError):
                    continue
                self._sum[key] = self._sum.get(key, 0.0) + num
                self._count[key] = self._count.get(key, 0) + 1
                self._min[key] = num if key not in self._min else min(self._min[key], num)
                self._max[key] = num if key not in self._max else max(self._max[key], num)

    def finalize(self) -> Dict[str, Dict[str, float]]:
        mean = {k: self._sum[k] / self._count[k] for k in self._sum}
        return {
            'count': self._count,
            'mean': mean,
            'min': self._min,
            'max': self._max,
        }
