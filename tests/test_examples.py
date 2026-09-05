import importlib.util
import json
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import pytest
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'examples' / f'{name}.py')
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


runner = module('run_actor')
exporter = module('export_csv')


def test_current_sample_is_valid():
    value = runner.load_input(ROOT / 'data/sample-input.json')
    assert value['maxResults'] == 3
    assert value['includeDetails'] is False


def test_unknown_template_input_is_rejected(tmp_path):
    path = tmp_path / 'input.json'
    path.write_text('{"helloWorld": 123}', encoding='utf-8')
    with pytest.raises(ValidationError):
        runner.load_input(path)


@pytest.mark.parametrize('status,collection', [('SUCCEEDED', 'succeeded'), ('SUCCEEDED', 'blocked'),
                                             ('FAILED', 'failed'), ('SUCCEEDED', 'partial')])
def test_client_preserves_results_and_both_statuses(status, collection):
    calls = []
    def call(**kwargs):
        calls.append(kwargs)
        return dict(id='fixture', status=status, defaultDatasetId='dataset', defaultKeyValueStoreId='store')
    client = SimpleNamespace(
        actor=lambda name: SimpleNamespace(call=call),
        dataset=lambda name: SimpleNamespace(iterate_items=lambda: iter([{'listingId': '1'}])),
        key_value_store=lambda name: SimpleNamespace(get_record=lambda key: {'value': {'status': collection}}),
    )
    result = runner.collect(client, {}, Decimal('0.003'))
    assert result['items'] == [{'listingId': '1'}]
    assert result['runStatus'] == status and result['summary']['status'] == collection
    assert calls[0]['max_total_charge_usd'] == Decimal('0.003')
    assert calls[0]['run_timeout'].total_seconds() == 180


@pytest.mark.parametrize('value', ['0', '-1', 'NaN', 'Infinity'])
def test_invalid_spending_cap_does_not_start_a_run(value):
    with pytest.raises(ValueError):
        runner.collect(None, {}, Decimal(value))


def test_csv_preserves_nested_fields_and_missing_values(tmp_path):
    import csv
    source, target = tmp_path / 'input.json', tmp_path / 'output.csv'
    source.write_text(json.dumps({'items': [{'title': 'Apartamento', 'price': None,
                                          'location': {'city': 'São Paulo'}}]}), encoding='utf-8')
    exporter.export_csv(source, target)
    with target.open(encoding='utf-8-sig', newline='') as stream:
        row = next(csv.DictReader(stream))
    assert row['price'] == ''
    assert json.loads(row['location']) == {'city': 'São Paulo'}
