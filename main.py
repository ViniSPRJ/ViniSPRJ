from ingest import DataIngestor
from analyze import StatsAnalyzer
from report import ResultAggregator


def run(path: str) -> None:
    ingestor = DataIngestor(path)
    analyzer = StatsAnalyzer()
    for chunk in ingestor.load():
        analyzer.process(chunk)
    aggregator = ResultAggregator()
    aggregator.add('basic_stats', analyzer.finalize())
    result = aggregator.consolidate()
    print(result)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process large CSV/XLSM files and compute statistics.')
    parser.add_argument('path', help='Path to input data file')
    args = parser.parse_args()
    run(args.path)
