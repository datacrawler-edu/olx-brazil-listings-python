"""Keep the public guide, examples and affiliate profile consistent."""
import json
import re
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]


def test_template_section_order():
    text = (ROOT / 'README.md').read_text(encoding='utf-8')
    headings = re.findall(r'^## (.+)$', text, re.M)
    expected = [
        'What this repository helps you do', 'Example result', 'Run without code',
        "Try it with Apify's free plan", 'Quick start for developers', 'Input example',
        'Request examples', 'Output fields', 'Common use cases',
        'How to export OLX Brazil listings to CSV with Python',
        'How to search OLX Brazil by keyword instead of URL',
        'FAQ', 'Limits and pricing', 'Hosted version', 'Responsible use', 'Support', 'License',
    ]
    assert headings == expected
    profile = json.loads((ROOT / 'config/actor-profile.json').read_text())
    assert profile['content']['readmeSectionOrder'] == expected


def test_markdown_links_resolve_and_actor_links_are_affiliated():
    profile = json.loads((ROOT / 'config/actor-profile.json').read_text())
    for path in ROOT.rglob('*.md'):
        if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding='utf-8')
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if link.startswith(profile['actor']['storeUrl']):
                assert link == profile['affiliate']['actorUrl']
            elif '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).is_file(), (path, link)


def test_readme_json_examples_match_real_sample_and_input_contract():
    text = (ROOT / 'README.md').read_text(encoding='utf-8')
    examples = [json.loads(block) for block in re.findall(r'```json\n(.*?)\n```', text, re.S)]
    sample = json.loads((ROOT / 'data/sample-output.json').read_text(encoding='utf-8'))
    assert examples[0] == sample[0]
    assert examples[1] == json.loads((ROOT / 'data/sample-input.json').read_text())
    validator = Draft7Validator(json.loads((ROOT / 'data/input-schema.json').read_text()))
    for value in examples[1:]:
        validator.validate(value)
