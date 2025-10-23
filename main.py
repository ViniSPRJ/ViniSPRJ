import json
import logging
import sys
from typing import Optional

from ingest import DataIngestor
from analyze import StatsAnalyzer
from report import ResultAggregator


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def run(path: str, output_format: str = 'json', verbose: bool = False) -> None:
    """
    Process a data file and compute statistics.

    Args:
        path: Path to the input CSV or XLSM file
        output_format: Output format ('json' or 'dict')
        verbose: Enable verbose logging
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        # Use context manager to ensure cleanup
        with DataIngestor(path) as ingestor:
            analyzer = StatsAnalyzer()
            logger.info(f"Starting data processing for: {path}")

            for chunk in ingestor.load():
                analyzer.process(chunk)

            # Aggregate results
            aggregator = ResultAggregator()
            aggregator.add('basic_stats', analyzer.finalize())
            result = aggregator.consolidate()

            # Output results
            if output_format == 'json':
                print(json.dumps(result, indent=2))
            else:
                print(result)

            logger.info("Processing completed successfully")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        sys.exit(1)
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=verbose)
        sys.exit(1)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Process large CSV/XLSM files and compute statistics.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.csv
  %(prog)s large_file.xlsm --format json
  %(prog)s data.csv --verbose

Supported file formats: .csv, .xlsm
        """
    )
    parser.add_argument('path', help='Path to input data file (CSV or XLSM)')
    parser.add_argument(
        '--format',
        choices=['json', 'dict'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()
    run(args.path, output_format=args.format, verbose=args.verbose)
