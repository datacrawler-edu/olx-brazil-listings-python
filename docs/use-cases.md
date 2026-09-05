# OLX Brazil workflows

## Property comparisons

Start with data/sample-input.json, replace the property search URL with your target location, then run examples/run_actor.py and examples/export_csv.py as shown in the README. Compare price and location alongside source attributes. Listing attributes vary and may need normalization in your spreadsheet.

## Product keyword comparisons

Use searchQueries with a category term, remove searchUrls and set small result and page caps. Inspect the actual returned attributes before comparing products; the Actor does not decide whether two listings describe equivalent products.

## Your own dated exports

Run the Python example with --output output/listings-date.json and export that file to CSV. Keep separate files for later comparisons using listingId. This is a user-managed workflow; the Actor does not provide historical price data or built-in alerts.
