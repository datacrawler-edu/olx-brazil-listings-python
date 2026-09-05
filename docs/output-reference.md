# Output reference

The [complete JSON sample](../data/sample-output.json) lists every delivered field. `listingId` identifies a listing; `url` links to its source. `price` is numeric when available, while `priceDisplay` preserves the source formatting. `location` contains available location components. `attributes` preserves source label/value pairs. `photos` and `thumbnailUrl` contain image links.

`description`, `seller` and `sellerDetails` may be null. `detailsCollected`, `detailsStatus` and `sellerDetailsStatus` describe enrichment; `not_requested` in the sample means the corresponding enrichment option was false. Listing details and seller profile requests have separate switches. Do not treat a missing seller as evidence that no seller exists.

`postedAtText` preserves source text; it is not a normalized posting timestamp. `scrapedAt` records collection time. `searchUrl`, `searchQuery` and `pageNumber` retain provenance. Nullable fields and empty arrays are meaningful; do not replace them with guessed data.

The Python client wraps rows in `items` alongside `runId`, `runStatus` and `summary`. These wrapper keys are not listing fields. Inspect summary.status before treating a run as complete. The CSV exporter retains nested fields as JSON strings.

`summary.profilesCharged` counts distinct billed seller profiles, while `summary.billingCharged` counts billed listings. Several listings can contain the same profile without creating additional profile events in the same run.
