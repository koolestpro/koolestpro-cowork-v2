# BEBEMOSS — Social Media Content
**Brand:** Bebemoss (Ginger the Sleepy Bunny) · Unofficial concept work. Not affiliated with or commissioned by Bebemoss.
**Posts covered:** Static Ad Showcase (2026-07-17) · CRO Fix teardown, soft toys collection page (2026-08-18)
**Machine-readable version:** `bebemoss-social-content.json` — same keys, used by automation. Update both together.

> Note: product photography is AI-generated (gpt-image-2) and flagged as such. Every claim traces to bebemoss.com or Faire — nothing was invented.

---

## HOW TO USE THIS FILE

| Platform | What to post | Caption key |
|---|---|---|
| LinkedIn | Combined 2x2 showcase | SA-BEBEMOSS-COMBO |
| LinkedIn / Instagram | Any single ad concept | SA-BEBEMOSS-PROBLEM, -BENEFIT, -PROOF, -OFFER |
| Twitter/X | Combined showcase | SA-BEBEMOSS-X1 |
| Twitter/X | Social proof ad | SA-BEBEMOSS-X2 |
| Twitter/X | Offer/urgency ad | SA-BEBEMOSS-X3 |
| LinkedIn / Instagram | Before/after graphic | CRO-BEBEMOSS-BA |
| LinkedIn / Instagram | Annotated rebuilt fold | CRO-BEBEMOSS-ANNO |
| LinkedIn / Instagram | 7-slide teardown carousel | CRO-BEBEMOSS-CAROUSEL |
| Twitter/X | Single posts, 3 angles | CRO-BEBEMOSS-X1, -X2, -X3 |
| Twitter/X | 7-tweet thread | CRO-BEBEMOSS-XTHREAD |

Static Ad assets live in `outputs/static-ads/bebemoss_ginger-sleepy-bunny_20260717/`. CRO Fix assets live in `outputs/cro-fixes/bebemoss/`. Every caption already carries the "concept, not affiliated" framing — keep it in when posting.

---

## STATIC AD SHOWCASE — 2026-07-17

**SA-BEBEMOSS-COMBO — `combined-showcase.png`** (LinkedIn)
```
Bebemoss sells a $44 crocheted bunny. No discount codes, no countdown timers, no "10,000 reviews" banner slapped across the page.

So I set myself a rule: build 4 ad directions for one of their toys and don't invent a single claim.

Where each one came from:

Problem: most "first toys" are plastic and in a landfill before the kid starts school. This one gets kept.

Benefit: GOTS organic cotton, crocheted by hand, made to EU toy-safety standards. Real specs, no filler.

Social proof: one actual review, "she's actually a work of art." Plus their 4.9 from wholesale buyers on Faire.

Offer: they have no sale to run, so I told the truth instead. It's made to order, by hand. That's the reason to act, not a fake timer.

Same bunny. Same photo. Four different reasons to care, depending on where the buyer's head is when they see it.

That's most of the job with ad creative. Not "make it pop." Figure out what the person needs to hear first.

Concept work. I'm not affiliated with Bebemoss, I just liked the product enough to think about how I'd sell it.

#ecommerce #dtc #advertising #adcreative #cro #brandstrategy
```

**SA-BEBEMOSS-PROBLEM — `ad-1-problem-solution.png`**
```
Most "first toys" are plastic, and in a landfill before the kid starts school. A hand-crocheted organic cotton one is the toy they actually keep. (Concept ad for Bebemoss, not affiliated.)
```

**SA-BEBEMOSS-BENEFIT — `ad-2-benefit-result.png`**
```
Made by hand, made to keep. GOTS organic cotton, every stitch crocheted by an artisan mom, built to EU toy-safety standards. (Concept ad for Bebemoss, not affiliated.)
```

**SA-BEBEMOSS-PROOF — `ad-3-social-proof.png`**
```
"When she peeked out of the bag, I was amazed, she's actually a work of art." 4.9 from wholesale buyers, made by 120+ artisan moms. (Concept ad for Bebemoss, not affiliated.)
```

**SA-BEBEMOSS-OFFER — `ad-4-offer-urgency.png`**
```
Not mass-stocked. Each Bebemoss bunny gets crocheted when you order it. Real scarcity, no fake timer. Meet Ginger the Sleepy Bunny, $44. (Concept ad, not affiliated.)
```

**SA-BEBEMOSS-X1 — combined showcase (X)**
```
4 ad directions from one $44 crocheted bunny.

No fake discounts. No made-up review counts. Every line traces back to something real about the brand.

Same product, 4 different reasons to buy it. That's the whole game.

(concept work, not affiliated with Bebemoss)
```

**SA-BEBEMOSS-X2 — social proof (X)**
```
Best social proof isn't "10,000 reviews."

It's one specific line: "when she peeked out of the bag, I was amazed, she's actually a work of art."

Built a whole ad around that one real review. Specific beats big every time.

(concept, not affiliated)
```

**SA-BEBEMOSS-X3 — offer/urgency (X)**
```
Bebemoss has no discount to run. So how do you write an "act now" ad without lying?

You don't fake a countdown. You tell the truth: it's crocheted by hand, made to order, not sitting in a warehouse.

Real scarcity does the work a fake timer can't.
```

---

## CRO FIX TEARDOWN — soft toys collection page — 2026-08-18

Real teardown of the live page at https://bebemoss.com/collections/toys, not concept work.
Every finding was observed on the live site at a 390x844 mobile viewport and is written up in
`outputs/audits/bebemoss_toys-collection_audit.md`. The "after" is a rebuild by Ridwan, using
Bebemoss's own product photos and real prices. No metrics, no lift claims, none were measured.

Content pack: `outputs/cro-fixes/bebemoss_toys-collection_content.html`
Images: `outputs/cro-fixes/bebemoss/`

**CRO-BEBEMOSS-BA — `koolestpro_bebemoss_before-after.png` (LinkedIn, long caption)**
```
Bebemoss makes handmade toys. Every one crocheted by a woman artisan, a lot of them refugees. I like the brand, which is exactly why the collection page bothered me.

It opens with five sentences about the mission. On a phone that block is 519px tall and the screen is 844, so the whole first screen is copy. The first toy creeps in at the bottom edge with its name and price still cut off.

Nobody taps "Soft Toys" to read a mission statement. They tap it to see toys.

Two other things while I was in there.

A pink "Save 10%" tab is docked to the bottom left. The page runs 8,200px and that tab rides the whole way down. On my screen it sat right on top of a toy's name and price.

And there are 48 products with no filter and no sort. Bebemoss already names its ranges in its own copy, Safari, Ocean, Woodland, Garden Life, Dreams. None of that is something a shopper can tap.

So I rebuilt the top of the page. Same photos, same prices, same brand.

- Mission down to one line, with a "Read our story" link for anyone who wants the rest
- Those five ranges as filter chips, price sort sitting next to them
- Grid starts at the fold, four toys with names and prices before you scroll
- Save pill shrunk and moved bottom right, clear of the card text

The story still sells. It just sells better standing next to the toys instead of in front of them.

If your collection page opens with a paragraph, go look at it on your phone right now.

Ridwan

#ecommerce #cro #shopify #dtc #conversionrateoptimization
```

**CRO-BEBEMOSS-ANNO — `koolestpro_bebemoss_annotated-changes.png` (Instagram)**
```
This toy brand's story is beautiful. It's also the entire first screen.

Bebemoss sells handmade crochet toys. Their collection page opens with five sentences about the mission. On a phone that paragraph is 519px tall, the screen is 844, so you scroll past all of it before you see a single toy.

Two more things I found:
A pink "Save 10%" tab docked bottom left, riding the full 8,200px scroll, sitting on top of a toy's name and price.
48 products with no filter and no sort, even though the brand names its own ranges in its own copy.

I rebuilt the top. Same photos, same prices:
Mission to one line, story link kept
Five ranges as filter chips
Price sort added
Grid starts at the fold
Save pill moved clear of the text

Save this if your collection page opens with a paragraph.

@koolestpro
#ecommerce #cro #shopify #dtc #collectionpage
```

**CRO-BEBEMOSS-CAROUSEL — `koolestpro_bebemoss_toys-collection_slide1-7.png`**
Same caption as CRO-BEBEMOSS-BA.

**CRO-BEBEMOSS-X1 — X single, angle A**
```
Bebemoss sells handmade crochet toys. Lovely brand.

Their collection page opens with a 519px mission paragraph on an 844px screen.

You scroll past the whole first screen before you see a toy.
```

**CRO-BEBEMOSS-X2 — X single, angle B**
```
Found a "Save 10%" tab docked to the bottom left of a collection page.

The page is 8,200px long. The tab rides the whole way down.

It was sitting on top of a product's name and price.
```

**CRO-BEBEMOSS-X3 — X single, angle C**
```
48 products. No filter. No sort.

The brand names its own ranges in its own copy: Safari, Ocean, Woodland, Garden Life, Dreams.

None of it is tappable. The taxonomy exists, it just never made it onto the page.
```

**CRO-BEBEMOSS-XTHREAD — X thread, 7 tweets**
```
1/ Bebemoss makes handmade crochet toys, each one made by a woman artisan.

Good brand. Their collection page still buries the toys. Quick teardown.

2/ The page opens with five sentences about the mission.

That block is 519px tall. A phone screen is 844.

So the entire first screen is copy.

3/ The first toy only reaches the bottom edge, with its name and price still cut off.

Someone who tapped "Soft Toys" already decided they want toys. The first screen answers a question they did not ask.

4/ Second thing: a pink "Save 10%" tab docked bottom left.

The page runs 8,200px and the tab rides all of it. On my screen it covered a toy's name and its price.

5/ Third: 48 products, no filter, no sort.

Bebemoss names its ranges in its own copy. Safari, Ocean, Woodland, Garden Life, Dreams. None of it is tappable.

6/ Rebuild, same photos and same prices:

Mission to one line with a story link. Five ranges as filter chips. Price sort. Grid starts at the fold. Save pill moved clear of the card text.

7/ The story still sells. It sells better standing next to the toys than in front of them.

If your collection page opens with a paragraph, open it on your phone.
```

## SA-BEBEMOSS-IG-SINGLE (added 2026-09-28)

Instagram single-image post, `outputs/static-ads/bebemoss_ginger-sleepy-bunny_20260717/ad-1-problem-solution.png` only. Written for this one image; the single post used to borrow the 4-ad LinkedIn caption.

```
Most first toys are landfill before kindergarten.

A hand-crocheted organic cotton bunny is the one they actually keep. The ad says the problem out loud and lets the toy sit there as the answer.

Concept ad for Bebemoss, not affiliated.

Follow @koolestpro for more ad and CRO breakdowns.

#ecommerce #dtc #advertising #adcreative #cro #brandstrategy
```
