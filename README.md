# Local DeepAgent

A lightweight, memory-efficient data processing framework for analyzing large CSV and XLSM files using chunked streaming.

## Features

- **Memory Efficient**: Processes files in configurable chunks (default: 500,000 rows) to avoid loading entire datasets into memory
- **Multiple Formats**: Supports both CSV and XLSM (Excel with macros) file formats
- **Statistical Analysis**: Computes basic statistics (count, mean, min, max) for all numeric columns
- **Modular Architecture**: Clean separation between data ingestion, analysis, and reporting
- **Robust Error Handling**: Graceful handling of encoding issues, missing files, and invalid data
- **Automatic Cleanup**: Temporary files are automatically cleaned up after processing
- **Logging Support**: Configurable logging for visibility into processing pipeline

## Installation

### Requirements

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

For XLSM support only:
```bash
pip install openpyxl
```

## Usage

### Basic Usage

Process a CSV file:
```bash
python main.py data.csv
```

Process an XLSM file:
```bash
python main.py large_dataset.xlsm
```

### Command Line Options

```bash
python main.py <file_path> [OPTIONS]

Options:
  --format {json,dict}  Output format (default: json)
  -v, --verbose         Enable verbose logging
  -h, --help           Show help message
```

### Examples

1. **Process CSV with JSON output** (default):
   ```bash
   python main.py sales_data.csv
   ```

2. **Process XLSM with verbose logging**:
   ```bash
   python main.py financial_report.xlsm --verbose
   ```

3. **Output as Python dictionary**:
   ```bash
   python main.py data.csv --format dict
   ```

### Output Format

The tool outputs statistics in JSON format by default:

```json
{
  "basic_stats": {
    "count": {
      "revenue": 10000,
      "cost": 10000,
      "profit": 10000
    },
    "mean": {
      "revenue": 1523.45,
      "cost": 892.33,
      "profit": 631.12
    },
    "min": {
      "revenue": 100.0,
      "cost": 50.0,
      "profit": -200.0
    },
    "max": {
      "revenue": 50000.0,
      "cost": 30000.0,
      "profit": 20000.0
    }
  }
}
```

## Architecture

The project follows a clean modular pipeline architecture:

```
Input File → DataIngestor → StatsAnalyzer → ResultAggregator → Output
```

### Components

1. **DataIngestor** (`ingest.py`):
   - Streams rows from CSV/XLSM files in fixed-size chunks
   - Handles file format detection and conversion
   - Manages temporary file cleanup

2. **StatsAnalyzer** (`analyze.py`):
   - Computes statistics incrementally on data chunks
   - Handles non-numeric values gracefully
   - Protects against division by zero and invalid values

3. **ResultAggregator** (`report.py`):
   - Consolidates results from multiple analyzers
   - Provides extensible framework for adding new analysis types

4. **Main** (`main.py`):
   - Orchestrates the processing pipeline
   - Handles command-line interface
   - Configures logging and error handling

## Programmatic Usage

You can also use Local DeepAgent as a library in your Python code:

```python
from ingest import DataIngestor
from analyze import StatsAnalyzer
from report import ResultAggregator

# Process a file
with DataIngestor('data.csv') as ingestor:
    analyzer = StatsAnalyzer()

    for chunk in ingestor.load():
        analyzer.process(chunk)

    stats = analyzer.finalize()
    print(stats)
```

### Custom Chunk Size

Configure the chunk size for memory optimization:

```python
# Process in smaller chunks (100,000 rows)
with DataIngestor('huge_file.csv', chunksize=100_000) as ingestor:
    # ... process
```

## Performance Characteristics

- **Memory Usage**: Constant, determined by chunk size (~50-100 MB per 500K rows)
- **Processing Speed**: ~100,000 - 500,000 rows/second (varies by CPU and disk I/O)
- **File Size**: No theoretical limit (tested up to multi-GB files)

## Limitations

- Only computes basic statistics (count, mean, min, max)
- No support for categorical column analysis
- Single-threaded processing (no parallel execution)
- XLSM files are converted to temporary CSV (requires disk space)
- Assumes first row contains column headers

## Error Handling

The tool handles common errors gracefully:

- **Missing files**: Clear error message with file path
- **Unsupported formats**: Lists supported formats
- **Encoding issues**: Automatically retries with alternate encoding
- **Missing dependencies**: Provides installation instructions
- **Invalid data**: Skips non-numeric values with optional logging

## Development

### Project Structure

```
.
├── main.py          # Entry point and CLI
├── ingest.py        # Data ingestion module
├── analyze.py       # Statistical analysis module
├── report.py        # Results aggregation module
├── requirements.txt # Python dependencies
├── .gitignore      # Git ignore patterns
└── README.md       # This file
```

### Extending the Framework

#### Adding New Analyzers

Create a new analyzer following the pattern:

```python
class CustomAnalyzer:
    def __init__(self):
        # Initialize state

    def process(self, rows: List[Dict[str, str]]) -> None:
        # Process each chunk

    def finalize(self) -> Dict:
        # Return results
```

Then use it in `main.py`:

```python
custom_analyzer = CustomAnalyzer()
for chunk in ingestor.load():
    custom_analyzer.process(chunk)

aggregator.add('custom_stats', custom_analyzer.finalize())
```

#### Adding New File Formats

Extend `DataIngestor` in `ingest.py`:

```python
def load(self) -> Iterator[List[Dict[str, str]]]:
    # Add new format detection
    if self.path.lower().endswith('.parquet'):
        return self._read_parquet(self.path)
    # ...
```

## Contributing

Contributions are welcome! Areas for improvement:

- Add more statistical measures (median, variance, percentiles)
- Support for categorical column analysis
- Parallel processing for multi-core systems
- Additional file format support (Parquet, JSON, XML)
- Data validation and cleaning options
- Progress bars for long-running operations
- Unit and integration tests

## License

This project is open source and available for educational and research purposes.

## Author

ViniSPRJ - Learning AI and Code

## Changelog

### Version 2.0 (Current)
- Fixed critical temp file leak bug
- Fixed division by zero in statistics calculation
- Added proper logging support
- Added file validation and better error handling
- Added context manager support for resource cleanup
- Improved CLI with verbose mode and output format options
- Enhanced error messages and user experience

### Version 1.0
- Initial modular architecture
- Basic CSV and XLSM support
- Memory-efficient chunked processing
- Basic statistics computation
