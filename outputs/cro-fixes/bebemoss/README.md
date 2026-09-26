# Bebemoss — CRO Fix, soft toys collection page

Generated 2026-08-18 by the `koolestpro-weekly-cro-fix` scheduled run. Nothing here has been posted.
Status in the content system is `Created`.

## What this is

A real teardown of the live page at https://bebemoss.com/collections/toys, reviewed on a
390x844 mobile viewport. Three findings, all observed on the live site:

1. The mission paragraph is 519px tall on an 844px screen, so the entire first screen is copy
   and the first toy only reaches the bottom edge with its name and price cut off.
2. A docked "Save 10%" tab rides the full 8,200px scroll and covers product titles and prices.
3. 48 products with no filter and no sort, even though the brand names its own ranges
   (Safari, Ocean, Woodland, Garden Life, Dreams) in its own copy.

No conversion, revenue or lift numbers appear anywhere. None were measured.

## Files

| File | What it is |
|---|---|
| `koolestpro_bebemoss_before-after.png` | 1:1 before/after, 3 numbered pins on the after image |
| `koolestpro_bebemoss_annotated-changes.png` | 1:1 annotated rebuilt fold, 8 points |
| `koolestpro_bebemoss_toys-collection_slide1-7.png` | 7-slide carousel |
| `captions.txt` | All five copy tabs as exported from the content pack |
| `manifest.json` | Machine-readable index of the above |

Every image was exported by calling the content pack's own `captureFixed()` / `captureSlide()`
html2canvas functions, so these are byte-identical to clicking the download buttons by hand.

## Where the rest lives

- Content pack (open this to re-export or edit): `outputs/cro-fixes/bebemoss_toys-collection_content.html`
- Audit brief: `outputs/audits/bebemoss_toys-collection_audit.md`
- The "after" rebuild itself: `outputs/cro-fixes/bebemoss_rebuild.html`
- Captions as the durable source of truth: `bebemoss-social-content.md` / `.json` at the project root,
  under the `CRO-BEBEMOSS-*` keys

## Worth a human look before posting

- The rebuild is Ridwan's own mockup of Bebemoss's page. It uses their real photos and real
  prices, but it is not their work and the caption should keep reading that way.
- The carousel slides sit content-top with empty space at the bottom on the shorter slides
  (3, 4, 7). That matches the existing approved CRO Fix layout used for Material Kitchen and
  Obvi, so it was left alone rather than diverging from the shared template.
