/* ============================================================
   SITE CONFIG — the only file you edit to reskin this template.
   Change brand, colours, fonts, copy, products. Nothing else.
   ============================================================ */

window.SITE = {

  /* ---------- 1. BRAND ---------- */
  brand: {
    name: "Lumora Skin",
    wordmark: "LUMORA",
    wordmarkMark: "L",
    tagline: "Skincare that knows Lagos weather",
    established: "MADE IN LAGOS · SINCE 2019",
    email: "care@lumoraskin.example",
    phone: "+234 811 750 0831",
    whatsapp: "2348117500831",
    whatsappMessage: "Hi Ridwan, I saw the Lumora demo store. I'd like to talk about a build for my brand.",
    social: { instagram: "#", tiktok: "#", x: "#" },
    year: 2026,
    /* Set to null to hide the disclaimer ribbon on a real client build. */
    conceptNotice: "Lumora Skin is a fictitious brand. This is a demo store, nothing here is for sale."
  },

  /* ---------- 1b. WHO BUILT IT (watermark + credits) ---------- */
  builtBy: {
    /* Set to null to remove the watermark, ribbon credit and footer credit. */
    name: "Koolestpro",
    url: "https://koolestpro.com",
    domain: "koolestpro.com",
    ribbonCredit: "Built by",
    watermark: "Built by Koolestpro",
    footerCredit: "Demo store designed and built by Koolestpro"
  },

  /* ---------- 2. THEME ---------- */
  theme: {
    bg:        "#FBF6EF",
    bg2:       "#F5ECE0",
    surface:   "#EFE3D3",
    ink:       "#201B16",
    accent:    "#AE5B34",
    accentDim: "#8C4726",
    onAccent:  "#FFF7EF",
    line:      "rgba(32,27,22,.16)",
    lineSoft:  "rgba(32,27,22,.09)",
    ink2:      "rgba(32,27,22,.74)",
    ink3:      "rgba(32,27,22,.56)",
    scrim:     "251,246,239",
    shadow:    "0 18px 50px -28px rgba(70,44,26,.42)",
    radius:    "6px",
    radiusLg:  "22px",
    fontDisplay: "'Fraunces', 'Iowan Old Style', Georgia, serif",
    fontBody:    "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    googleFonts: "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Inter:wght@300;400;500"
  },

  /* ---------- 3. MONEY ---------- */
  currency: { symbol: "₦", locale: "en-NG", decimals: 0 },

  /* ---------- 3b. LABELS (wording the engine uses; changes per vertical) ---------- */
  labels: {
    itemSingular: "product",
    itemPlural: "products",
    buyerNoun: "reviews",
    addToCart: "Add to bag",
    cartTitle: "Your bag",
    cartEmpty: "Your bag is empty.",
    cartEmptyLink: "Have a look at the range",
    checkout: "Order on WhatsApp",
    keepLooking: "Keep looking",
    collectionTitle: "The range",
    collectionCrumb: "The range",
    relatedIndex: "Goes with",
    relatedTitle: "What people pair it with.",
    relatedLink: "The full range",
    specTitle: "The details",
    taxNote: "Delivery calculated when you message us.",
    inStock: "In stock, leaves Lagos within 24 hours",
    lowStock: "Only {n} left in this size",
    assurances: [
      "Same-day Lagos delivery, 2 to 4 days nationwide",
      "Pay on delivery anywhere in Lagos",
      "7-day swap on anything unopened",
      "Full ingredient list before you order"
    ],
    footerBlurb: "Made in small batches in Lagos, for skin that has to survive Lagos.",
    faqAside: "Still not sure which one is right for your skin? Message us and a person will answer.",
    faqCta: "Ask on WhatsApp"
  },

  /* ---------- 4. NAV ---------- */
  nav: [
    { label: "The range", href: "collection.html" },
    { label: "Best sellers", href: "collection.html?c=Treat" },
    { label: "The formula", href: "index.html#formula" },
    { label: "Reviews", href: "index.html#reviews" },
    { label: "Help", href: "index.html#faq" }
  ],

  /* ---------- 5. TICKER ---------- */
  ticker: [
    "Free Lagos delivery over ₦25,000",
    "Order straight to WhatsApp",
    "Pay on delivery in Lagos",
    "Made for melanin-rich skin",
    "Nationwide in 2 to 4 days"
  ],

  /* ---------- 6. HERO ---------- */
  hero: {
    eyebrow: "Made in Lagos, for Lagos skin",
    headline: ["Skincare that knows", "Lagos weather."],
    italicWord: "weather.",
    sub: "Humidity, dust, harmattan and office AC all take a turn at your skin before 9am. Every Lumora formula is built around that, not around a routine written for somewhere cold.",
    ctaPrimary: { label: "Shop the range", href: "collection.html" },
    ctaSecondary: { label: "Ask us on WhatsApp", href: "wa" },
    image: "assets/img/hero.webp",
    caption: "The morning four · Cleanse, treat, seal, protect",
    anchor: "top"
  },

  /* ---------- 7. FEATURED ---------- */
  featured: {
    index: "01",
    label: "The Range",
    title: "Twelve products. Nothing filler.",
    sub: "We would rather sell you four things that work together than twelve that sit in a drawer. Every product here earns its place in a real morning.",
    linkLabel: "See all twelve",
    linkHref: "collection.html",
    anchor: "range",
    ids: ["lum-serum", "lum-spf", "lum-cleanser", "lum-moisturizer"]
  },

  /* ---------- 8. EDITORIAL — THE FORMULA ---------- */
  movement: {
    index: "02",
    label: "The Formula",
    anchor: "formula",
    title: "Tested on Lagos skin, in Lagos weather, before it ever went on a shelf.",
    body: "Most of what gets sold here was formulated for a climate that has a real winter. That is why the moisturiser your cousin swears by in London sits on your face like a film by midday. Every batch we make gets worn through a full Lagos day, in traffic and under AC, by people who will say so if it fails.",
    image: "assets/img/editorial-ingredients.webp",
    imageAlt: "Raw shea butter, clay and botanical oils on a warm stone surface",
    stats: [
      { value: 12,  suffix: "",  label: "Products in the range" },
      { value: 94,  suffix: "%", label: "Reorder within 90 days" },
      { value: 3600, suffix: "+", label: "Orders taken on WhatsApp" },
      { value: 7,   suffix: " day", label: "Swap on anything unopened" }
    ]
  },

  /* ---------- 9. PINNED HORIZONTAL STORY ---------- */
  story: {
    index: "03",
    label: "The Routine",
    anchor: "routine",
    title: "Four steps. Ten minutes. That is the whole thing.",
    panels: [
      { n: "I",   title: "Cleanse",   body: "Sulphate-free, so it lifts sunscreen and Lagos dust without leaving your face tight by the time you reach the car.", image: "assets/img/product-cleanser.webp" },
      { n: "II",  title: "Treat",     body: "Vitamin C in the morning for dark spots, clay twice a week for congestion. This is the step that actually changes something.", image: "assets/img/product-serum.webp" },
      { n: "III", title: "Seal",      body: "Shea and ceramides, light enough to disappear under makeup and strong enough to survive eight hours of air conditioning.", image: "assets/img/product-moisturizer.webp" },
      { n: "IV",  title: "Protect",   body: "SPF 50 with no white cast, reapplied at lunch. Skip this one and the first three steps are a waste of money.", image: "assets/img/product-spf.webp" }
    ]
  },

  /* ---------- 10. GIFT / PROMO BANNER ---------- */
  promo: {
    kicker: "Save 17% on the set",
    title: "The set people keep buying twice.",
    body: "Cleanser, moisturiser and a detox bar, ribboned in a box. Bought once for a birthday, then again for themselves about a month later.",
    cta: { label: "See the gift set", href: "collection.html?c=Sets" },
    image: "assets/img/promo-sets.webp",
    anchor: "sets"
  },

  /* ---------- 11. VALUE PROPS ---------- */
  valueProps: {
    index: "04",
    label: "Ordering",
    anchor: "care",
    title: "What happens after you tap the button.",
    image: "assets/img/lifestyle-skin.webp",
    items: [
      { title: "You message, we reply", body: "No account, no card details typed into a form. You send a message, a person confirms what is in stock and what it comes to." },
      { title: "Pay when it reaches you", body: "Pay on delivery anywhere in Lagos. Nationwide is a transfer confirmed in the same chat before we hand it to the courier." },
      { title: "Same day where we can", body: "Anything confirmed before 2pm goes out in Lagos that day. Everywhere else in Nigeria lands inside two to four working days." },
      { title: "Tell us your skin first", body: "Send a photo or describe what your skin does at 3pm and we will tell you which two products to start with. Usually it is two, not six." }
    ]
  },

  /* ---------- 12. THE KITCHEN ---------- */
  atelier: {
    index: "05",
    label: "The Kitchen",
    anchor: "kitchen",
    title: "It started on a stove in Surulere. It is still made the same way.",
    body: [
      "The first batch was shea butter whipped in a kitchen pot and sold to neighbours who kept coming back for more. Nothing about that has been industrialised since, mostly on purpose. We make in runs of a few hundred so a bad batch never reaches more than a few hundred people.",
      "Lumora is a demo brand, but this is the exact story most of the founders we build for are trying to tell and cannot, because their website is a link tree."
    ],
    image: "assets/img/editorial-kitchen.webp",
    signature: "Adaeze O. · Founder"
  },

  /* ---------- 13. REVIEWS ---------- */
  reviews: {
    index: "06",
    label: "Customers",
    anchor: "reviews",
    title: "What people say about a month in.",
    items: [
      { rating: 5, text: "My skin has never held up this well through harmattan. The eye cream is non-negotiable now, I have bought it three times.", name: "Bisola A.", place: "Lekki, Lagos", product: "lum-eye-cream" },
      { rating: 5, text: "Ordered on WhatsApp on a Tuesday, had it Thursday morning in Enugu. The serum genuinely faded my dark spots in about three weeks.", name: "Chiamaka O.", place: "Enugu", product: "lum-serum" },
      { rating: 5, text: "Bought the set for my sister's birthday and she has reordered twice since. The packaging alone made it feel like a proper gift.", name: "Tunde K.", place: "Abuja", product: "lum-gift-set" },
      { rating: 5, text: "Finally a sunscreen that does not go grey on my skin tone. I sent it to my whole office group chat the same week.", name: "Ifeoma N.", place: "Port Harcourt", product: "lum-spf" },
      { rating: 5, text: "I have oily skin and every moisturiser I tried used to slide off by midday. This one just sits there and behaves.", name: "Halima S.", place: "Kaduna", product: "lum-moisturizer" }
    ]
  },

  /* ---------- 14. FAQ ---------- */
  faq: {
    index: "07",
    label: "Questions",
    anchor: "faq",
    title: "Before you order.",
    items: [
      { q: "How long does delivery take?", a: "Anything confirmed before 2pm goes out the same day within Lagos and usually reaches you that evening. Nationwide is two to four working days by courier, tracked, with the number sent to you in the same WhatsApp chat." },
      { q: "Can I return something?", a: "Unopened items can be swapped within seven days if the order was confirmed wrong on size or scent. Message us with the order details and we will sort it out. We cannot take back anything already opened, for obvious reasons." },
      { q: "How do I pay?", a: "Pay on delivery anywhere in Lagos. Nationwide is a bank transfer confirmed in chat before we dispatch. No card details are collected on this site at all." },
      { q: "Is this suitable for oily or sensitive skin?", a: "Yes, and it is worth telling us which before you order. Everything is fragrance-light and reviewed by a dermatologist. Send us a message describing what your skin does by mid afternoon and we will point you at two products rather than selling you six." },
      { q: "Will the sunscreen leave a white cast?", a: "No. It was reformulated twice specifically because the first version did, and we tested it on deeper skin tones in daylight rather than in a studio." },
      { q: "Where can I see the full ingredient list?", a: "Ask on WhatsApp and we will send the full INCI list for any product before you buy it. We do not hide it behind a form." }
    ]
  },

  /* ---------- 15. NEWSLETTER + FOOTER ---------- */
  newsletter: {
    title: "One note a month.",
    body: "Restocks, a new product when there is one, and the occasional straight answer about an ingredient everyone is arguing about online. No countdown timers.",
    placeholder: "Your email address",
    cta: "Subscribe"
  },
  footer: {
    columns: [
      { title: "Shop", links: [
        { label: "The full range", href: "collection.html" },
        { label: "Cleanse", href: "collection.html?c=Cleanse" },
        { label: "Treat", href: "collection.html?c=Treat" },
        { label: "Body", href: "collection.html?c=Body" },
        { label: "Gift sets", href: "collection.html?c=Sets" }
      ]},
      { title: "Help", links: [
        { label: "Delivery", href: "index.html#faq" },
        { label: "Swaps", href: "index.html#faq" },
        { label: "Payment", href: "index.html#faq" },
        { label: "Ingredients", href: "index.html#faq" },
        { label: "Build me a routine", href: "index.html#faq" }
      ]},
      { title: "Brand", links: [
        { label: "The formula", href: "index.html#formula" },
        { label: "The routine", href: "index.html#routine" },
        { label: "The kitchen", href: "index.html#kitchen" },
        { label: "Reviews", href: "index.html#reviews" }
      ]}
    ],
    legal: "All rights reserved.",
    payments: ["Transfer", "Pay on delivery", "Card on request", "Verve", "USSD"]
  },

  /* ---------- 16. PRODUCTS ---------- */
  categories: ["All", "Cleanse", "Treat", "Moisturise", "Protect", "Body", "Sets"],

  products: [
    {
      id: "lum-cleanser", name: "Gentle Foaming Cleanser", ref: "150ml",
      category: "Cleanse", badge: "Best seller",
      price: 9500, compareAt: 0,
      image: "assets/img/product-cleanser.webp",
      gallery: ["assets/img/product-cleanser.webp", "assets/img/editorial-ingredients.webp", "assets/img/lifestyle-skin.webp"],
      short: "Sulphate-free daily wash, lifts SPF without stripping.",
      blurb: "A soft daily cleanser that takes off sunscreen, sweat and a day of Lagos dust without leaving your face tight. No sulphates, no squeaky feeling, which is the thing people mistake for clean and then wonder why their skin is producing oil by noon.",
      rating: 4.8, reviewCount: 132, stock: 24,
      variants: { label: "Size", options: ["150ml", "Travel 50ml"] },
      specs: [
        ["Key actives", "Glycerin, panthenol, coconut-derived surfactants"],
        ["Skin type", "All, including sensitive"],
        ["Texture", "Low-foam gel"],
        ["Use", "Morning and night"],
        ["Fragrance", "Light, botanical"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-serum", name: "Vitamin C Brightening Serum", ref: "30ml",
      category: "Treat", badge: "Best seller",
      price: 18000, compareAt: 21000,
      image: "assets/img/product-serum.webp",
      gallery: ["assets/img/product-serum.webp", "assets/img/editorial-ingredients.webp", "assets/img/lifestyle-skin.webp"],
      short: "10% stabilised vitamin C for dark spots and uneven tone.",
      blurb: "The product that changes something you can actually see. Ten percent stabilised vitamin C with vitamin E, for dark spots left behind by old breakouts and the uneven patches that show up in photographs. It absorbs in about thirty seconds and leaves nothing behind for your sunscreen to fight with.",
      rating: 4.9, reviewCount: 208, stock: 16,
      variants: { label: "Size", options: ["30ml", "Travel 10ml"] },
      specs: [
        ["Key actives", "10% sodium ascorbyl phosphate, vitamin E, ferulic acid"],
        ["Skin type", "All, patch test if very sensitive"],
        ["Texture", "Light fluid"],
        ["Use", "Mornings, before SPF"],
        ["Fragrance", "None"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-moisturizer", name: "Shea and Ceramide Moisturiser", ref: "50ml",
      category: "Moisturise", badge: "",
      price: 14500, compareAt: 17000,
      image: "assets/img/product-moisturizer.webp",
      gallery: ["assets/img/product-moisturizer.webp", "assets/img/lifestyle-skin.webp", "assets/img/editorial-ingredients.webp"],
      short: "Locally sourced shea and ceramides, light under makeup.",
      blurb: "Shea butter sourced from a co-operative in Kwara, blended with ceramides so it holds moisture through a full day of air conditioning. Light enough that makeup sits on top of it properly, which is the reason most people switch to it from something heavier.",
      rating: 4.7, reviewCount: 96, stock: 21,
      variants: { label: "Size", options: ["50ml", "Jumbo 100ml"] },
      specs: [
        ["Key actives", "Shea butter, ceramide NP, niacinamide"],
        ["Skin type", "Normal to dry, works for oily in AC"],
        ["Texture", "Whipped cream"],
        ["Use", "Morning and night"],
        ["Fragrance", "Light, warm"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-toner", name: "Rosewater Balancing Toner", ref: "100ml",
      category: "Cleanse", badge: "",
      price: 11000, compareAt: 0,
      image: "assets/img/product-toner.webp",
      gallery: ["assets/img/product-toner.webp", "assets/img/editorial-ingredients.webp"],
      short: "Alcohol-free mist that preps skin to take a serum.",
      blurb: "An alcohol-free rosewater mist for the gap between washing your face and putting something on it. It brings your skin back to neutral and leaves it slightly damp, which is when a serum actually absorbs instead of sitting there.",
      rating: 4.6, reviewCount: 74, stock: 30,
      variants: { label: "Size", options: ["100ml"] },
      specs: [
        ["Key actives", "Rosa damascena water, glycerin, allantoin"],
        ["Skin type", "All"],
        ["Texture", "Fine mist"],
        ["Use", "After cleansing"],
        ["Fragrance", "Natural rose"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-mask", name: "Purifying Clay Mask", ref: "60g",
      category: "Treat", badge: "Low stock",
      price: 13000, compareAt: 0,
      image: "assets/img/product-mask.webp",
      gallery: ["assets/img/product-mask.webp", "assets/img/editorial-ingredients.webp"],
      short: "Black clay and charcoal, twice a week, no tightness.",
      blurb: "Black clay and activated charcoal for congestion around the nose and chin. Twice a week is the whole instruction. It draws out oil without that drum-tight feeling that makes people reach for a heavy cream afterwards and start the cycle again.",
      rating: 4.8, reviewCount: 61, stock: 4,
      variants: { label: "Size", options: ["60g"] },
      specs: [
        ["Key actives", "Kaolin, bentonite, activated charcoal"],
        ["Skin type", "Oily and combination"],
        ["Texture", "Soft clay"],
        ["Use", "Twice weekly, 10 minutes"],
        ["Fragrance", "None"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-spf", name: "Daily Defence SPF 50", ref: "50ml",
      category: "Protect", badge: "Best seller",
      price: 16500, compareAt: 0,
      image: "assets/img/product-spf.webp",
      gallery: ["assets/img/product-spf.webp", "assets/img/lifestyle-skin.webp", "assets/img/editorial-ingredients.webp"],
      short: "SPF 50, no white cast, reapplies clean over makeup.",
      blurb: "Reformulated twice because the first version went grey on deeper skin tones and we were not going to sell that. Weightless, no cast, and it reapplies over makeup at lunch without turning into a mess. If you only buy one thing here, buy this one.",
      rating: 4.9, reviewCount: 154, stock: 12,
      variants: { label: "Size", options: ["50ml"] },
      specs: [
        ["Protection", "SPF 50 PA++++, broad spectrum"],
        ["Key actives", "Tinosorb S, niacinamide, vitamin E"],
        ["Skin type", "All, tested on deep tones"],
        ["Texture", "Weightless fluid"],
        ["Use", "Every morning, again at midday"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-body-butter", name: "Whipped Shea Body Butter", ref: "200g",
      category: "Body", badge: "",
      price: 15000, compareAt: 0,
      image: "assets/img/product-body-butter.webp",
      gallery: ["assets/img/product-body-butter.webp", "assets/img/editorial-kitchen.webp"],
      short: "For elbows, knees and everywhere the AC dries out.",
      blurb: "The product Lumora started with, still whipped in small runs. Deeply hydrating for elbows, knees and shins, and it sinks in fast enough that you can get dressed straight after instead of standing around waiting.",
      rating: 4.8, reviewCount: 88, stock: 19,
      variants: { label: "Size", options: ["200g", "Jumbo 400g"] },
      specs: [
        ["Key actives", "Unrefined shea butter, sweet almond oil, vitamin E"],
        ["Skin type", "Dry and very dry body skin"],
        ["Texture", "Whipped butter"],
        ["Use", "After a shower, while skin is damp"],
        ["Fragrance", "Light vanilla"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-soap", name: "Charcoal Detox Bar", ref: "120g",
      category: "Body", badge: "",
      price: 6500, compareAt: 0,
      image: "assets/img/product-soap.webp",
      gallery: ["assets/img/product-soap.webp", "assets/img/editorial-kitchen.webp"],
      short: "Handmade charcoal bar for body and back.",
      blurb: "A handmade bar for body and back congestion, cut from a loaf so no two are exactly the same size. Gentle enough for daily use, which is unusual for anything with charcoal in the name.",
      rating: 4.5, reviewCount: 47, stock: 40,
      variants: { label: "Size", options: ["120g"] },
      specs: [
        ["Key actives", "Activated charcoal, shea, tea tree"],
        ["Skin type", "Body, back and shoulders"],
        ["Texture", "Cold-process bar"],
        ["Use", "Daily in the shower"],
        ["Fragrance", "Tea tree"],
        ["Made", "Lagos, cut by hand"]
      ]
    },
    {
      id: "lum-eye-cream", name: "Renewing Eye Cream", ref: "15ml",
      category: "Moisturise", badge: "New",
      price: 17500, compareAt: 20500,
      image: "assets/img/product-eye-cream.webp",
      gallery: ["assets/img/product-eye-cream.webp", "assets/img/lifestyle-skin.webp"],
      short: "Light peptide cream for tired mornings and long AC days.",
      blurb: "A light peptide cream for the mornings after a night you should not have had. It softens fine lines and takes down puffiness without dragging at skin that thin. Pat it on, do not rub it.",
      rating: 4.7, reviewCount: 52, stock: 9,
      variants: { label: "Size", options: ["15ml"] },
      specs: [
        ["Key actives", "Matrixyl 3000, caffeine, hyaluronic acid"],
        ["Skin type", "All"],
        ["Texture", "Light cream"],
        ["Use", "Morning and night, ring finger"],
        ["Fragrance", "None"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-lip-balm", name: "Shea Tinted Lip Balm", ref: "4g",
      category: "Body", badge: "New",
      price: 5500, compareAt: 0,
      image: "assets/img/product-lip-balm.webp",
      gallery: ["assets/img/product-lip-balm.webp", "assets/img/lifestyle-skin.webp"],
      short: "Sheer terracotta tint, survives harmattan.",
      blurb: "A sheer terracotta tint with shea and vitamin E. It keeps lips soft right through harmattan and reads as your own colour rather than as lipstick, which is why people buy three at a time.",
      rating: 4.6, reviewCount: 39, stock: 35,
      variants: { label: "Shade", options: ["Terracotta", "Clear", "Deep berry"] },
      specs: [
        ["Key actives", "Shea butter, vitamin E, castor oil"],
        ["Skin type", "All"],
        ["Texture", "Balm"],
        ["Use", "Whenever, honestly"],
        ["Fragrance", "None"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-scrub", name: "Brown Sugar Body Scrub", ref: "200g",
      category: "Body", badge: "",
      price: 12500, compareAt: 0,
      image: "assets/img/product-scrub.webp",
      gallery: ["assets/img/product-scrub.webp", "assets/img/editorial-kitchen.webp"],
      short: "Coarse sugar in shea oil, for dry patches in the shower.",
      blurb: "Coarse brown sugar in a shea oil base. It buffs off dry patches without the sandpaper feeling of a salt scrub, and the oil stays on your skin after you rinse so you may not need anything else afterwards.",
      rating: 4.7, reviewCount: 58, stock: 22,
      variants: { label: "Size", options: ["200g"] },
      specs: [
        ["Key actives", "Brown sugar, shea oil, coconut oil"],
        ["Skin type", "Body, dry and flaky patches"],
        ["Texture", "Coarse scrub"],
        ["Use", "Once or twice a week"],
        ["Fragrance", "Warm sugar"],
        ["Made", "Lagos, in batches of 300"]
      ]
    },
    {
      id: "lum-gift-set", name: "Lumora Essentials Gift Set", ref: "3 pieces",
      category: "Sets", badge: "Save 17%",
      price: 32000, compareAt: 38500,
      image: "assets/img/product-gift-set.webp",
      gallery: ["assets/img/product-gift-set.webp", "assets/img/promo-sets.webp", "assets/img/editorial-kitchen.webp"],
      short: "Cleanser, moisturiser and a detox bar in a ribboned box.",
      blurb: "The cleanser, the moisturiser and a detox bar, ribboned in a box that does not need wrapping. Our most-gifted set, and the one people buy a second time about a month later for themselves.",
      rating: 4.9, reviewCount: 44, stock: 7,
      variants: { label: "Presentation", options: ["Gift box", "Plain box"] },
      specs: [
        ["Contains", "Foaming Cleanser 150ml, Shea Moisturiser 50ml, Charcoal Bar 120g"],
        ["Value", "₦38,500 bought separately"],
        ["Skin type", "All"],
        ["Presentation", "Ribboned rigid box, card included"],
        ["Use", "A full starter routine"],
        ["Made", "Lagos, packed by hand"]
      ]
    }
  ]
};
