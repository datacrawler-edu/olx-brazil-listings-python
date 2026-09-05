# OLX Brazil listings: scrape prices and export CSV with Python

Collect structured OLX Brazil listings from Apify's web interface, or use the Python, cURL and JavaScript examples in this repository. Inspect BRL asking prices, locations, attributes, photos and listing URLs before building a property-research or marketplace-comparison workflow.

[Open OLX Brazil Scraper on Apify](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata)

**Availability:** the repository is public; the hosted Actor is currently private. Live requests and the web workflow require an Apify account with access to the Actor. You can inspect the sample data and export it locally without an account.

## What this repository helps you do

- Collect listings from an OLX Brazil search URL or keyword search.
- Compare advertised prices alongside city, neighborhood and listing attributes.
- Request listing-page descriptions with `includeDetails`, and separately opt in to paid seller profiles with `enrichProfiles`.
- Export listings to CSV while retaining nested fields as JSON cells.

This is an unofficial OLX integration guide with executable examples and sample data. The hosted scraper implementation is maintained separately.

## Example result

This complete listing comes from a successful run with optional details disabled. Null seller and description fields reflect that input. Inspect the [JSON sample](data/sample-output.json) or [CSV sample](data/sample-output.csv) without starting a run.

```json
{
  "listingId": "1532746016",
  "title": "Apartamento à venda com 123m², 3 quartos e 2 vagas",
  "url": "https://sp.olx.com.br/sao-paulo-e-regiao/imoveis/apartamento-a-venda-com-123m-3-quartos-e-2-vagas-1532746016",
  "price": 1440000,
  "priceDisplay": "R$ 1.440.000",
  "currency": "BRL",
  "location": {
    "display": "São Paulo, Carandiru",
    "city": "São Paulo",
    "state": "SP",
    "neighborhood": "Carandiru",
    "postalCode": null
  },
  "attributes": [
    {
      "label": "area",
      "value": "123m²"
    },
    {
      "label": "bedrooms",
      "value": "4"
    },
    {
      "label": "bathrooms",
      "value": "3"
    },
    {
      "label": "parking",
      "value": "2"
    }
  ],
  "photos": [
    "https://img.olx.com.br/thumbs700x500/79/793603806921287.webp"
  ],
  "thumbnailUrl": "https://img.olx.com.br/thumbs700x500/79/793603806921287.webp",
  "description": null,
  "seller": null,
  "postedAtText": "Hoje, 08:43",
  "searchUrl": "https://www.olx.com.br/imoveis/venda/estado-sp",
  "searchQuery": null,
  "pageNumber": 1,
  "detailsCollected": false,
  "detailsStatus": "not_requested",
  "sellerDetails": null,
  "sellerDetailsStatus": "not_requested",
  "scrapedAt": "2026-09-05T11:54:23.170870+00:00"
}
```

## Run without code

If your account has access to the hosted Actor:

1. Open [OLX Brazil Scraper](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata) in Apify.
2. In **Input**, paste an OLX Brazil search-result URL into `searchUrls`.
3. For a small first run, keep `maxResults` at 3, both page limits at 1, and both `includeDetails` and `enrichProfiles` off.
4. Click **Start** and follow the progress messages.
5. Open the completed run's **Dataset**, inspect the listings, and export JSON, CSV or Excel.

Select `enrichProfiles` only if you want seller profile enrichment at an additional price per unique identifiable profile saved in the run, depending on your plan ($0.75-$1 per 1,000), including partial profiles. It works independently of listing details.

For keyword-only searches, remove the example URL and enter `searchQueries`. See the [no-code guide](docs/no-code-guide.md) for a walkthrough. Python installation and an API token are only needed for the developer workflow below.

## Try it with Apify's free plan

Apify's Free plan includes **$5 in monthly prepaid usage**, with no credit card required to start. Available credit can fund small tests of accessible Actors; it does not grant access to a private Actor or provide unlimited free runs. Unused credits expire at the end of the billing cycle and do not roll over. Check [Apify's current pricing](https://apify.com/pricing?fpr=edudata) before running a larger batch.

## Quick start for developers

Use Python 3.13 from the repository root:

```powershell
python -m pip install -r requirements.txt
python examples/run_actor.py --dry-run
```

The dry run validates the input without starting a paid run. For live execution, set `APIFY_TOKEN` in your environment using your usual secret-management method, then run:

```powershell
python examples/run_actor.py --input data/sample-input.json --max-charge 0.003
```

The example uses the official Apify client, a USD 0.003 event-charge cap and a three-minute run timeout. It writes `output/result.json` containing `runStatus`, `summary` and `items`. An event-charge cap is not a promise that all account-level platform charges are included. Check the run in Console before repeating a request after a connection failure.

General category URLs are supported: the Actor automatically requests their listing results while preserving the location and filters in your URL. Source access and available detail fields can vary by category.

## Input example

```json
{
  "searchUrls": [
    "https://www.olx.com.br/imoveis/venda/estado-sp"
  ],
  "maxResults": 3,
  "maxPagesPerSearch": 1,
  "maxPagesTotal": 1,
  "includeDetails": false,
  "enrichProfiles": false
}
```

Replace the URL with your intended search. When both `searchUrls` and `searchQueries` have entries, both sets of searches run. See the [input reference](docs/input-reference.md) and [machine-readable schema](data/input-schema.json).

## Request examples

- **Python:** [run_actor.py](examples/run_actor.py) validates input, starts the Actor and retrieves its Dataset and collection summary.
- **cURL:** [request instructions](examples/curl-request.md) send the sample JSON to the synchronous Dataset endpoint.
- **JavaScript:** [request.mjs](examples/javascript/request.mjs) uses Node's built-in fetch to retrieve Dataset items.

For JavaScript, use Node.js 22 or later: run `node examples/javascript/request.mjs --dry-run` first, then set `APIFY_TOKEN` and run `node examples/javascript/request.mjs` for a paid request.

The synchronous REST examples return Dataset rows, not the Python wrapper's summary object. An empty array is not proof that collection succeeded. Inspect the run in Apify Console for diagnostics. See the [official endpoint documentation](https://docs.apify.com/api/v2/actor-run-sync-get-dataset-items-post).

## Output fields

| Field | Meaning |
| --- | --- |
| `listingId`, `url` | Listing identity and source link |
| `title` | Listing headline |
| `price`, `priceDisplay`, `currency` | Numeric asking price, display text and BRL currency |
| `location` | Available city, state, neighborhood and postal code |
| `attributes` | Source-provided attribute labels and values |
| `photos`, `thumbnailUrl` | Available image URLs |
| `description`, `seller`, `sellerDetails` | Optional available enrichment; may be null |
| `detailsStatus`, `sellerDetailsStatus` | Whether optional enrichment was requested and its result |
| `searchUrl`, `searchQuery`, `pageNumber` | Search provenance |
| `scrapedAt` | Collection timestamp |

See the [output reference](docs/output-reference.md) for null values, provenance and status interpretation.

## Common use cases

- Build a property comparison sheet with asking price, city and bedroom/area attributes.
- Collect keyword results for a product category and compare available listing attributes.
- Save separate dated exports for your own subsequent analysis.

The [use-case guide](docs/use-cases.md) explains how to choose the input and interpret each export.

## How to export OLX Brazil listings to CSV with Python

Try the exporter on the included sample:

```powershell
python examples/export_csv.py data/sample-output.json output/sample.csv
```

After a live Python run, export its results:

```powershell
python examples/export_csv.py output/result.json output/listings.csv
```

The exporter retains every listing field. Nested objects and arrays become JSON cells; it does not flatten bedroom or location values into invented columns.

## How to search OLX Brazil by keyword instead of URL

Save the following as `data/keyword-input.json`, then pass it with `--input`:

```json
{"searchQueries":["apartamento"],"maxResults":3,"maxPagesPerSearch":1,"maxPagesTotal":1,"includeDetails":false}
```

```powershell
python examples/run_actor.py --input data/keyword-input.json --max-charge 0.003
```

Omitting `searchUrls` prevents the example property URL from becoming a second search. For several keywords, put each keyword in the array and remember that `maxResults` and `maxPagesTotal` apply across the run.

## FAQ

### Can I use this without writing code?

Yes, through Apify's Input form if your account has access to the Actor. The repository itself is public and its samples need no account.

### Does it include seller phone numbers or emails?

No contact field is guaranteed. Optional `enrichProfiles` enrichment only returns available source data and is billed separately; inspect the detail status fields.

### Why can a succeeded run contain no listings?

A search can be empty or blocked. In the Python result, inspect `summary.status` as well as `runStatus`. The client retains returned rows and exits with code 2 for failed runs or blocked/failed collection summaries.

Read the [full FAQ](docs/faq.md) for additional input and charging questions.

## Limits and pricing

The input accepts up to 1,000 URLs and 1,000 keyword searches. `maxResults` is 1–10,000, `maxPagesPerSearch` is 1–20, and `maxPagesTotal` is 1–1,000. These are caps, not guarantees that enough source listings are available. Retry and pacing settings are managed by the Actor.

Optional profile enrichment prices:

| Plan | Price per profile | Equivalent per 1,000 profiles |
| --- | --- | --- |
| Free | $0.00100 | $1.00 |
| Bronze | $0.00090 | $0.90 |
| Silver | $0.00080 | $0.80 |
| Gold | $0.00075 | $0.75 |
| Platinum | $0.00075 | $0.75 |
| Diamond | $0.00075 | $0.75 |

Listing billing is per unique listing saved, including a base listing whose optional listing-page details are incomplete. Empty searches, blocked requests, duplicates and rejected rows do not create listing charges. With `enrichProfiles=true`, an additional charge per unique seller profile per run applies: Free **$0.001 ($1/1,000)**, Bronze **$0.0009 ($0.90/1,000)**, Silver **$0.0008 ($0.80/1,000)**, and Gold/Platinum/Diamond **$0.00075 ($0.75/1,000)**. The charge requires useful profile endpoint data with an unambiguous `publicAccountId` saved in the Dataset; partial profiles qualify. Repeated sellers are charged once per run. Empty, blocked, unidentified and conflicting-identity profiles do not create profile charges. Basic seller data from the listing page is included in listing billing. The profile option is off by default.

The spending guard reserves budget for both events before profile requests and may stop with some budget remaining. `summary.billingCharged` counts listings and `summary.profilesCharged` counts profiles. Consult the [Actor's Pricing tab](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata) for current tier prices and applicable platform charges.

Prices in the Dataset are asking prices at collection time. The Actor does not supply historical prices or calculate price-drop alerts. Source fields may be missing, and OLX can deny access. Partial or empty collection does not establish complete market coverage.

## Hosted version

[Open OLX Brazil Scraper on Apify](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata) to use its web form or API with an authorized account. Apify hosts execution and stores the output. This public repository does not grant access to the currently private Actor.

## Responsible use

Use listing data in accordance with applicable rules, source access terms and privacy obligations. Never commit API tokens or include them in an issue. This project is not affiliated with OLX.

Links to Apify contain the affiliate identifier `fpr=edudata`; we may earn a commission from referrals.

## Support

For example-code problems, [open a GitHub issue](https://github.com/datacrawler-edu/olx-brazil-listings-python/issues) with the command and sanitized input. For hosted scraping problems, use the [Actor's Issues tab](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata) and provide the run ID without credentials.

See [CONTRIBUTING.md](CONTRIBUTING.md) for offline tests.

## License

Example code is provided under the [MIT License](LICENSE). This does not grant rights to third-party listing content or access to the hosted Actor.
