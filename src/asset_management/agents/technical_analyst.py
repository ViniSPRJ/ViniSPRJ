"""Simple technical analysis using sample price data."""
from __future__ import annotations
from pathlib import Path
from typing import List
import csv
import statistics


def load_prices() -> List[float]:
    """Load closing prices from a CSV file."""
    data_path = Path(__file__).resolve().parents[3] / 'data' / 'prices.csv'
    prices: List[float] = []
    try:
        with data_path.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                prices.append(float(row['close']))
    except FileNotFoundError:
        pass
    return prices


def simple_moving_average(prices: List[float], period: int = 30) -> float:
    if len(prices) < period:
        return statistics.mean(prices)
    return statistics.mean(prices[-period:])


def exponential_moving_average(prices: List[float], period: int = 30) -> float:
    if not prices:
        return 0.0
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return ema


def volatility(prices: List[float], period: int = 30) -> float:
    if len(prices) < period:
        period = len(prices)
    return statistics.stdev(prices[-period:])


def rate_of_change(prices: List[float], period: int = 30) -> float:
    if len(prices) <= period:
        return 0.0
    return (prices[-1] - prices[-period]) / prices[-period] * 100


def rsi(prices: List[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0
    gains = []
    losses = []
    for i in range(-period, 0):
        change = prices[i] - prices[i - 1]
        if change >= 0:
            gains.append(change)
        else:
            losses.append(abs(change))
    avg_gain = statistics.mean(gains) if gains else 0
    avg_loss = statistics.mean(losses) if losses else 0
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def analyze(asset_id: str) -> str:
    """Compute simple technical indicators for the asset."""
    prices = load_prices()
    if not prices:
        return 'No price data available.'
    indicators = {
        'SMA': round(simple_moving_average(prices), 2),
        'EMA': round(exponential_moving_average(prices), 2),
        'Volatility': round(volatility(prices), 2),
        'ROC': round(rate_of_change(prices), 2),
        'RSI': round(rsi(prices), 2),
    }
    parts = [f'{name}: {value}' for name, value in indicators.items()]
    joined = '; '.join(parts)
    return f'Technical analysis for {asset_id}: {joined}'
