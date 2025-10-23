import logging
import math
from typing import Dict, List, Union

logger = logging.getLogger(__name__)


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
                    # Skip NaN and infinite values
                    if math.isnan(num) or math.isinf(num):
                        continue
                except (TypeError, ValueError):
                    continue

                self._sum[key] = self._sum.get(key, 0.0) + num
                self._count[key] = self._count.get(key, 0) + 1

                if key not in self._min:
                    self._min[key] = num
                    self._max[key] = num
                else:
                    self._min[key] = min(self._min[key], num)
                    self._max[key] = max(self._max[key], num)

    def finalize(self) -> Dict[str, Dict[str, Union[int, float]]]:
        # Safely compute mean, handling division by zero
        mean: Dict[str, float] = {}
        for key in self._sum:
            count = self._count.get(key, 0)
            if count > 0:
                mean[key] = self._sum[key] / count
            else:
                mean[key] = 0.0
                logger.warning(f"Column '{key}' has no valid numeric values")

        # Ensure all dictionaries have consistent keys
        all_keys = set(self._sum.keys()) | set(self._count.keys())

        result = {
            'count': {k: self._count.get(k, 0) for k in all_keys},
            'mean': {k: mean.get(k, 0.0) for k in all_keys},
            'min': {k: self._min.get(k, 0.0) for k in all_keys},
            'max': {k: self._max.get(k, 0.0) for k in all_keys},
        }

        logger.info(f"Statistics computed for {len(all_keys)} columns")
        return result
