import csv
from typing import Dict, Iterator, List


class DataIngestor:
    """Stream rows from a CSV or XLSM file in fixed-size chunks."""

    def __init__(self, path: str, chunksize: int = 500_000):
        self.path = path
        self.chunksize = chunksize

    def load(self) -> Iterator[List[Dict[str, str]]]:
        if self.path.endswith('.csv'):
            return self._read_csv(self.path)
        if self.path.endswith('.xlsm'):
            csv_path = self._xlsm_to_csv(self.path)
            return self._read_csv(csv_path)
        raise ValueError('Unsupported file format')

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
        import openpyxl
        wb = openpyxl.load_workbook(xlsm_path, read_only=True, data_only=True)
        ws = wb.active
        temp_path = xlsm_path + '.tmp.csv'
        with open(temp_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([cell.value for cell in next(ws.iter_rows())])
            for row in ws.iter_rows(min_row=2, values_only=True):
                writer.writerow(row)
        return temp_path
