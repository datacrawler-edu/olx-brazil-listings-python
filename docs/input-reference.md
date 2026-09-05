# Input reference

| Input | Type | Limit and behavior |
| --- | --- | --- |
| searchUrls | Array of strings | Up to 1,000 OLX Brazil search-result URLs |
| searchQueries | Array of strings | Up to 1,000 keywords, each up to 200 characters |
| maxResults | Integer | 1–10,000; default 100; initial form uses 3 |
| maxPagesPerSearch | Integer | 1–20; default and initial form 1 |
| maxPagesTotal | Integer | 1–1,000; default 1,000; initial form 1 |
| includeDetails | Boolean | Listing-page details; default and initial form false |
| enrichProfiles | Boolean | Separately billed seller profile endpoints; default and initial form false; independent of includeDetails |

Both search arrays are combined when populated. For keyword-only searches, remove the initial URL. With neither search array populated, the Actor uses its example property search. Limits apply to the whole run except maxPagesPerSearch. Retry and delay inputs are not supported. The [schema](../data/input-schema.json) is the precise validation contract.
