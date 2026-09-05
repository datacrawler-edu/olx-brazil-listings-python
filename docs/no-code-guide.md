# Run OLX Brazil searches without code

Open [the Actor](https://apify.com/datascraperes/olx-brazil-listings-scraper?fpr=edudata) with an account that has access. The Actor is currently private.

1. In Input, replace `searchUrls` with your OLX Brazil search-result URL.
2. Alternatively, remove all URLs and enter words in `searchQueries`.
3. Begin with `maxResults=3`, `maxPagesPerSearch=1`, `maxPagesTotal=1`.
4. Leave `includeDetails=false` for base listings. Enable it for available listing-page descriptions and photos. Independently select `enrichProfiles` for paid seller profile data: $0.001 per unique identifiable profile saved per run ($1/1,000), including partial profiles. Leave it off to avoid profile charges.
5. Click Start, follow progress, then inspect the run's Dataset and export JSON, CSV or Excel.

If no listings appear, review the collection outcome before repeating the search. A successful platform status can accompany an empty or blocked collection. See [input reference](input-reference.md).
