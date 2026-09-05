# Frequently asked questions

## Is the hosted Actor accessible to everyone?

It is currently private. You need an account with access for web or API execution. The public repository's sample exporter works offline.

## Do I need an OLX login for the examples?

The exposed input schema has no OLX login or cookie fields. API calls require your Apify token and access to the Actor. Source access can still fail.

## Can I combine searches?

Yes. URL and keyword arrays are combined. Global result and page caps still apply. Remove searchUrls for keyword-only requests.

## Are seller contacts guaranteed?

No. The paid `enrichProfiles` option can return partial data and does not guarantee contact fields. Listing-page details remain separate. Check detailsStatus and sellerDetailsStatus.

## Are empty searches billed as saved listings?

No. Billing events correspond to unique listings saved, including listings with incomplete optional enrichment. The optional profile event costs the plan-specific price per unique identifiable seller with useful endpoint data saved per run, including partial profiles. Empty, blocked and unidentified profiles are not charged. Review the Actor Pricing tab for applicable charges.

## Is this a historical-price API?

No. It returns current advertised data at collection time. Store dated exports yourself if you need subsequent comparison.

## What does a blocked collection mean?

The source did not allow collection. Do not interpret empty output as zero matching listings or repeat requests indefinitely. Inspect the run and contact support with a sanitized input and run ID.
