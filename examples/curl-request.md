# Request OLX Brazil Dataset items with cURL

Run from the repository root with curl installed and APIFY_TOKEN set in your environment. Live requests require access to the currently private Actor and can incur charges. The input file is the same small sample used by the Python example.

PowerShell:

```powershell
curl.exe --fail-with-body --max-time 240 --request POST `
  --header "Authorization: Bearer $env:APIFY_TOKEN" `
  --header "Content-Type: application/json" `
  --data-binary "@data/sample-input.json" `
  --output listings.json `
  "https://api.apify.com/v2/acts/datascraperes~olx-brazil-listings-scraper/run-sync-get-dataset-items?timeout=180&maxTotalChargeUsd=0.003&format=json"
```

This uses a 180-second Actor timeout and USD 0.003 event-charge cap. The cap does not cover every possible account-level platform charge. The synchronous endpoint returns Dataset rows rather than the Python wrapper's collection summary. Inspect the run in Console if the array is empty or the request fails. Do not automatically repeat a timed-out request: the run may already have started.

See the [official synchronous endpoint](https://docs.apify.com/api/v2/actor-run-sync-get-dataset-items-post).
