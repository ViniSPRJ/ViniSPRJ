"""Coordinator for the asset management workflow."""
from datetime import datetime
from typing import Dict

from .agents import (
    equity_analyst,
    economist,
    market_sentiment,
    technical_analyst,
    analysis_agent,
)


def is_business_day(date: datetime) -> bool:
    return date.weekday() < 5


def run(asset_id: str) -> None:
    """Run the workflow if it's a business day."""
    today = datetime.now()
    if not is_business_day(today):
        print('Workflow can only be run Monday to Friday.')
        return

    results: Dict[str, str] = {}
    results['equity'] = equity_analyst.analyze(asset_id)
    results['economy'] = economist.analyze()
    results['sentiment'] = market_sentiment.analyze(asset_id)
    results['technical'] = technical_analyst.analyze(asset_id)

    final_opinion = analysis_agent.analyze(results)
    print('Final Opinion:')
    print(final_opinion)


if __name__ == '__main__':
    run('SAMPLE')
