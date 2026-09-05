"""Export complete listing fields; nested objects are preserved as JSON cells."""
import argparse
import csv
import json
from pathlib import Path


def export_csv(source, destination):
    data = json.loads(Path(source).read_text(encoding='utf-8'))
    rows = data['items'] if isinstance(data, dict) else data
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError('Expected a listing array or a result object containing items.')
    fields = list(dict.fromkeys(key for row in rows for key in row))
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    with Path(destination).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False)
                             if isinstance(value, (dict, list)) else value
                             for key, value in row.items()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    export_csv(args.source, args.destination)
