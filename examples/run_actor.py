"""Run the hosted OLX Brazil Actor using the official Apify Python client."""
import argparse
import json
import os
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from apify_client import ApifyClient
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
ACTOR = 'datascraperes/olx-brazil-listings-scraper'


def load_input(path):
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    schema = json.loads((ROOT / 'data/input-schema.json').read_text(encoding='utf-8'))
    Draft7Validator(schema).validate(value)
    return value


def collect(client, run_input, max_charge):
    if not max_charge.is_finite() or max_charge <= 0:
        raise ValueError('Maximum charge must be a positive finite USD amount.')
    run = client.actor(ACTOR).call(
        run_input=run_input, max_total_charge_usd=max_charge,
        run_timeout=timedelta(seconds=180), logger=None,
    )
    if not run:
        raise RuntimeError('No run returned. Check Apify Console before starting another run.')
    rows = list(client.dataset(run['defaultDatasetId']).iterate_items())
    record = client.key_value_store(run['defaultKeyValueStoreId']).get_record('SUMMARY')
    summary = record['value'] if record else {}
    # A platform SUCCEEDED run can still report blocked or partial scraping.
    return {'runId': run['id'], 'runStatus': run['status'], 'summary': summary, 'items': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/sample-input.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'output/result.json')
    parser.add_argument('--max-charge', type=Decimal, default=Decimal('0.003'))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    value = load_input(args.input)
    if not args.max_charge.is_finite() or args.max_charge <= 0:
        parser.error('--max-charge must be positive and finite')
    if args.dry_run:
        print(json.dumps(value, indent=2))
        return
    token = os.getenv('APIFY_TOKEN')
    if not token:
        parser.error('Set APIFY_TOKEN in your environment. Never commit it.')
    result = collect(ApifyClient(token), value, args.max_charge)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Saved {len(result['items'])} listings to {args.output}")
    print(f"Run status: {result['runStatus']}; collection: {result['summary'].get('status', 'unknown')}")
    if result['runStatus'] != 'SUCCEEDED' or result['summary'].get('status') in {'failed', 'blocked'}:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
