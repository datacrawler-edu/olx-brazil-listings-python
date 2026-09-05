# OLX Brazil Listings Python

Python examples for collecting OLX Brazil listing data through the hosted
[OLX Brazil Scraper](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata).
Export advertised BRL prices, locations, attributes, photos and listing URLs
for property research and marketplace price comparisons.

**Availability:** this repository is public; the hosted Actor is currently
private on Apify. Live execution requires an account with access to the Actor.
The sample-data exporter and offline tests work without an Apify account.

## What is included

- An official Apify Python-client example with a per-run spending cap.
- The Actor's current input schema and small example input.
- One complete listing from a real successful run, with no seller contacts.
- A CSV exporter that retains nested values as JSON cells.
- Offline tests and GitHub Actions validation.

This is an integration repository. The hosted scraper implementation is
maintained separately. It is an unofficial tool, not affiliated with OLX.

## Quick start

Use Python 3.13. Install the example dependencies:

```powershell
python -m pip install -r requirements.txt
python examples/run_actor.py --dry-run
```

The dry run validates and prints the input without starting or charging a run.
The example uses the same values as the Actor's initial form:

```json
{
  "searchUrls": ["https://www.olx.com.br/imoveis/venda/estado-sp"],
  "maxResults": 3,
  "maxPagesPerSearch": 1,
  "maxPagesTotal": 1,
  "includeDetails": false
}
```

For live execution, set `APIFY_TOKEN` in your environment using your usual
secret-management method, then run:

```powershell
python examples/run_actor.py --input data/sample-input.json --max-charge 0.003
```

This starts a paid Actor run with a USD 0.003 event-charge cap and a three-minute
run timeout. Results are written to `output/result.json`, including the run
status, collection summary and every returned listing. The command does not
restart failed runs automatically. Access-denied responses require access to
the hosted Actor; a public GitHub repository does not grant that access.

## Choose your search

Replace the sample search URL with a search-result URL copied from OLX Brazil.
For a keyword-only search, remove `searchUrls` and use `searchQueries`, such as
`["apartamento"]`. If both arrays contain entries, both sets of searches run.

| Input | Meaning |
| --- | --- |
| `searchUrls` | Up to 1,000 OLX Brazil search-result URLs |
| `searchQueries` | Up to 1,000 keyword searches |
| `maxResults` | Result cap, 1–10,000; default 100 when omitted |
| `maxPagesPerSearch` | Pages per source, 1–20; default 1 |
| `maxPagesTotal` | Pages across the run, 1–1,000; default 1,000 |
| `includeDetails` | Optional available description, image and seller enrichment; default false |

Pacing and retries are managed by the Actor. There are no user-facing HTTP
retry or delay settings. [data/input-schema.json](data/input-schema.json)
contains the precise validation rules.

## Export sample data without a live run

```powershell
python examples/export_csv.py data/sample-output.json output/sample.csv
```

After a live run, use `output/result.json` as the source instead. The exporter
also accepts a plain array of listing objects. [The complete sample](data/sample-output.json)
shows nullable fields and nested objects exactly as delivered. Empty seller
fields in that sample reflect a run with details disabled.

## Results, limits and charging

The hosted Actor charges per unique listing saved. Available enrichment is
included when enabled; a saved base listing remains billable if its optional
details are incomplete. Empty searches, blocked requests, duplicates and
rejected rows do not create listing charges. Consult the Actor's Pricing tab
for current tier prices.

Prices represent asking prices at collection time. The Actor does not provide
historical prices or calculate price-drop alerts. Missing source fields remain
empty; seller phone/email data is not guaranteed. OLX can deny access to a
search or detail page.

Always inspect `summary.status` as well as `runStatus`: a platform-successful
run can return a blocked or partial collection. The client retains returned
rows even when the run is unsuccessful; its exit code is 2 for failed runs or
blocked/failed collection summaries. Partial/empty collections are reported in
the output, without being mislabeled as complete data coverage.

## Development

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check examples tests
```

CI uses mocked clients and local sample data; it does not require secrets or
start paid runs. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[SECURITY.md](SECURITY.md).

## Documentation and support

- [Official Apify Python client](https://docs.apify.com/api/client/python)
- [Actor input schema](https://docs.apify.com/actors/development/actor-definition/input-schema/specification/v1)
- [Apify Dataset export formats](https://docs.apify.com/storage/dataset)

Open a GitHub issue for these examples. For hosted scraping issues, use the
Actor's Issues tab with a sanitized input and run ID. Never include tokens.
Use returned data in accordance with applicable rules and source restrictions.

Apify links in this guide contain the affiliate identifier `fpr=edudata`.

## License

Example code is provided under the [MIT License](LICENSE). The license does not
grant rights to third-party listing content or access to the hosted Actor.
