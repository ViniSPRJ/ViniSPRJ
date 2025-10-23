import csv
import os
from typing import Dict, Iterator, List


class DataIngestor:
    """Stream rows from a CSV or XLSM file in fixed-size chunks."""

    def __init__(self, path: str, chunksize: int = 500_000):
        self.path = path
        self.chunksize = chunksize
        self._temp_files: List[str] = []

    def load(self) -> Iterator[List[Dict[str, str]]]:
        if self.path.endswith('.csv'):
            yield from self._read_csv(self.path)
        elif self.path.endswith('.xlsm'):
            csv_path = self._xlsm_to_csv(self.path)
            self._temp_files.append(csv_path)
            try:
                yield from self._read_csv(csv_path)
            finally:
                self._cleanup_temp_files()
        else:
            raise ValueError('Unsupported file format. Only .csv and .xlsm files are supported.')

    def _read_csv(self, path: str) -> Iterator[List[Dict[str, str]]]:
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            chunk: List[Dict[str, str]] = []
            for row in reader:
                chunk.append(row)
                if len(chunk) >= self.chunksize:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

    def _xlsm_to_csv(self, xlsm_path: str) -> str:
        try:
            import openpyxl
        except ImportError:
            raise ImportError(
                'openpyxl is required to read .xlsm files. '
                'Install it with: pip install openpyxl'
            )

        try:
            wb = openpyxl.load_workbook(xlsm_path, read_only=True, data_only=True)
        except Exception as e:
            raise ValueError(f'Failed to load workbook {xlsm_path}: {e}')

        ws = wb.active
        if ws is None:
            raise ValueError(f'No active worksheet found in {xlsm_path}')

        temp_path = xlsm_path + '.tmp.csv'
        try:
            with open(temp_path, 'w', newline='') as f:
                writer = csv.writer(f)
                rows_iter = ws.iter_rows()
                header_row = next(rows_iter, None)
                if header_row is None:
                    raise ValueError(f'Worksheet in {xlsm_path} is empty')
                writer.writerow([cell.value for cell in header_row])
                for row in ws.iter_rows(min_row=2, values_only=True):
                    writer.writerow(row)
        except Exception as e:
            # Clean up partial temp file if conversion fails
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise ValueError(f'Failed to convert {xlsm_path} to CSV: {e}')
        finally:
            wb.close()

        return temp_path

    def _cleanup_temp_files(self) -> None:
        """Remove temporary files created during processing."""
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                # Silently ignore cleanup errors
                pass
        self._temp_files.clear()
