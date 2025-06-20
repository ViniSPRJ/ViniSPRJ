from pathlib import Path

def analyze() -> str:
    """Read the economic report and return an opinion."""
    report_path = Path(__file__).resolve().parents[3] / 'data' / 'economic_report.txt'
    try:
        text = report_path.read_text().strip()
    except FileNotFoundError:
        text = 'No economic report found.'
    return f'Economist opinion: {text}'
