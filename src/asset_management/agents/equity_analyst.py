from pathlib import Path

def analyze(asset_id: str) -> str:
    """Read the equity report and return an opinion."""
    report_path = Path(__file__).resolve().parents[3] / 'data' / 'equity_report.txt'
    try:
        text = report_path.read_text().strip()
    except FileNotFoundError:
        text = 'No equity report found.'
    return f'Equity analyst opinion for {asset_id}: {text}'
