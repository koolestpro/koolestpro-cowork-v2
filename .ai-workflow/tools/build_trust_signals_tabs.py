DST = "outputs/tips/trust-signals-over-credibility_2026-08-14.html"
with open(DST, "r", encoding="utf-8") as f:
    text = f.read()

# LinkedIn long-form
old = '''    <pre>Your store's animations aren't making it look premium. They're making it convert worse.

I know that's not what you want to hear after a weekend of adding scroll effects.

Here's the trap most Shopify brands fall into: more motion feels more high-end, and high-end feels like it should sell more. So they animate everything.

But motion isn't free. Amazon found that every 100ms of extra delay cost them about 1% in sales. Animations are the easiest way to add that delay without realising it.

The fix is to treat motion as a budget, not decoration. You get a small amount of attention and speed to spend on a page. Every animation spends some of it, so it has to buy something back.

Where it actually earns its place:

Selection feedback, so a shopper trusts their variant or bundle registered.
Add-to-cart confirmation, right when money is on the line.
Proof reveal, so reviews and guarantees land as they scroll to decide.

Everything else is spending budget for nothing: hero parallax, section-by-section fades, floating shapes.

Run every animation through one question: does it fire on a decision the shopper is making? If not, cut it.

Save this before your next build. And if you want to know which animations are quietly costing you sales, my DMs are open.</pre>'''
new = '''    <pre>You think more trust badges build more trust. That's exactly what's making shoppers bounce.

You spent an afternoon adding every trust signal you could find. Secure checkout badge. Money-back guarantee. As seen in. Free shipping banner. Verified reviews widget. All stacked above the fold.

Conversion didn't move. If anything it got worse.

Here's the part nobody tells you: past a certain number, trust badges stop reading as proof and start reading as defense. A wall of logos doesn't say "you can trust us." It says "something here needs explaining."

I see this on Shopify product pages constantly. Founders keep adding badges because each one feels safe on its own. Stacked together they read as anxious.

The fix isn't zero trust signals. It's one real one, said clearly.

One specific review with a name and a photo beats five generic star ratings.
Your actual return policy in plain words beats a "guarantee" badge.
A real founder photo beats a "featured in" logo strip.
Cut until only the signals answering a real objection are left.

Every page is a product. Every click is a choice. Stop performing trust. Start earning it.

Save this before your next PDP audit.</pre>'''
assert text.count(old) == 1, "linkedin tab not found"
text = text.replace(old, new)

# Hook
old = '''    <pre>Your store's animations aren't making it look premium. They're making it convert worse.

Motion isn't free. Every effect adds delay, and delay costs sales.

Spend it on decisions. Cut it everywhere else.

What's the first animation you'd defend to the death, and are you sure it's earning its place?</pre>'''
new = '''    <pre>You think more trust badges build more trust.

That's exactly what's making shoppers bounce.

Past three badges, people stop reading proof and start reading defense.

What's the one trust signal on your page actually doing any work?</pre>'''
assert text.count(old) == 1, "hook tab not found"
text = text.replace(old, new)

# X thread
old = '''    <pre>1/ Your store's animations aren't making it look premium. They're making it convert worse. A thread on the motion myth quietly killing your Shopify sales:

2/ The myth: more motion = more premium = more sales. So brands animate every section. Fade-ins everywhere. Parallax heroes. It looks high-end in the Figma preview.

3/ The problem: motion isn't free. Amazon found every 100ms of extra delay cost about 1% in sales. Animations are the easiest way to add that delay without noticing.

4/ The reframe: motion is a budget, not decoration. You get a little attention and speed to spend per page. Every animation spends some of it. It has to buy something back.

5/ Where it earns its place: selection feedback (variant registered), add-to-cart confirmation (money's on the line), proof reveal (reviews land as they decide).

6/ Everything else is spending budget for nothing: hero parallax, section-by-section fades, floating shapes. Cut them.

7/ One question for every animation: does it fire on a decision the shopper is making? If not, kill it. Follow @koolestpro for more Shopify CRO.</pre>'''
new = '''    <pre>1/ You think more trust badges build more trust. Past three, they read as defense, not proof.

2/ Secure checkout. Money-back guarantee. As seen in. Free shipping. Verified reviews. Six badges in one row above the fold.

3/ Each one feels safe alone. Stacked together they read as anxious, not credible.

4/ Shoppers don't count your badges. They notice the wall of them.

5/ One specific review with a name and a face beats five generic star icons.

6/ Your real return policy in plain words beats a "guarantee" badge every time.

7/ Cut the badges until only the ones answering a real objection are left. Follow @koolestpro for more Shopify CRO.</pre>'''
assert text.count(old) == 1, "x thread tab not found"
text = text.replace(old, new)

# X singles
old = '''    <pre>THE RULE
Motion is a budget, not decoration. You get a little attention and speed per page. Every animation spends some of it, so it had better buy something back.

THE CONTRAST
A scroll reveal on your reviews: earns its place. A parallax hero: spends the same budget and hands you nothing back.

THE HOT TAKE
Most of the animations you added to look premium are quietly lowering your add-to-cart rate. Fancy and converting are not the same thing.</pre>'''
new = '''    <pre>THE RULE
A trust badge only works if it answers a question the shopper already has. Everything else is decoration wearing a costume of proof.

THE CONTRAST
Six generic badges: ignored. One specific review with a name and a photo: read every time.

THE HOT TAKE
Most "trust signal" sections are founders trying to convince themselves, not the shopper. If your page needs seven badges to feel safe, the product page has a bigger problem.</pre>'''
assert text.count(old) == 1, "x singles tab not found"
text = text.replace(old, new)

# Instagram
old = '''    <pre>Your store's animations aren't making it look premium. They're making it convert worse.

Motion isn't free. Every effect adds delay, and Amazon found 100ms of delay costs about 1% in sales.

Treat motion as a budget. Spend it on decisions: selection feedback, add-to-cart confirmation, proof reveals.

Cut the parallax and the section-by-section fades. They're spending budget for nothing.

Save this. Follow @koolestpro for more Shopify CRO tips.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign #DigitalMarketing #ShopifyLiquid</pre>'''
new = '''    <pre>You think more trust badges build more trust. That's exactly what's making shoppers bounce.

Past three badges, shoppers stop reading proof. They start reading defense.

One real review with a name beats five generic stars.

Your actual return policy beats a guarantee icon.

Save this. Follow @koolestpro for more Shopify CRO tips.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign #DigitalMarketing #ShopifyLiquid</pre>'''
assert text.count(old) == 1, "ig tab not found"
text = text.replace(old, new)

with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

opens = text.count("<div")
closes = text.count("</div>")
print(f"div open={opens} close={closes} balanced={opens==closes}")
print("OK all tabs replaced")
