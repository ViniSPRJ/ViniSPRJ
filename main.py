import sys
from pathlib import Path
from ingest import DataIngestor
from analyze import StatsAnalyzer
from report import ResultAggregator


def run(path: str) -> None:
    # Validate input path
    input_path = Path(path)
    if not input_path.exists():
        print(f"Error: File '{path}' not found.", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print(f"Error: '{path}' is not a file.", file=sys.stderr)
        sys.exit(1)

    try:
        ingestor = DataIngestor(path)
        analyzer = StatsAnalyzer()
        for chunk in ingestor.load():
            analyzer.process(chunk)
        aggregator = ResultAggregator()
        aggregator.add('basic_stats', analyzer.finalize())
        result = aggregator.consolidate()
        print(result)
    except PermissionError:
        print(f"Error: Permission denied when accessing '{path}'.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process large CSV/XLSM files and compute statistics.')
    parser.add_argument('path', help='Path to input data file')
    args = parser.parse_args()
    run(args.path)
