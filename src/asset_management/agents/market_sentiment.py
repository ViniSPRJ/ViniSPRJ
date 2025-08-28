"""Simulated market sentiment analyzer."""
from random import choice

SENTIMENTS = [
    'Bullish sentiment detected.',
    'Bearish sentiment detected.',
    'Neutral sentiment across sources.'
]

def analyze(asset_id: str) -> str:
    """Return a random sentiment for demonstration purposes."""
    sentiment = choice(SENTIMENTS)
    return f'Market sentiment for {asset_id}: {sentiment}'
