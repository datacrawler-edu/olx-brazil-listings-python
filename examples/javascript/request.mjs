// Run from the repository root with Node.js 22+ and APIFY_TOKEN in the environment.
import { readFile, mkdir, writeFile } from 'node:fs/promises';

const input = JSON.parse(await readFile(new URL('../../data/sample-input.json', import.meta.url), 'utf8'));
if (process.argv.includes('--dry-run')) {
  console.log(JSON.stringify(input, null, 2));
} else {
  const token = process.env.APIFY_TOKEN;
  if (!token) throw new Error('Set APIFY_TOKEN; never commit it.');
  const endpoint = 'https://api.apify.com/v2/acts/datascraperes~olx-brazil-listings-scraper/run-sync-get-dataset-items?timeout=180&maxTotalChargeUsd=0.003&format=json';
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
    signal: AbortSignal.timeout(240000),
  });
  if (!response.ok) throw new Error(`Apify returned HTTP ${response.status}; inspect Console before retrying.`);
  const items = await response.json();
  if (!Array.isArray(items)) throw new Error('Expected a Dataset array. Inspect the run in Console.');
  await mkdir('output', { recursive: true });
  await writeFile('output/javascript-listings.json', JSON.stringify(items, null, 2));
  console.log(`Saved ${items.length} Dataset rows. Inspect the run in Console for collection status.`);
  if (items.length === 0) process.exitCode = 2;
}
