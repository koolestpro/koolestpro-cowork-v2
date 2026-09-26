/* ============================================================
   SITE CONFIG — the only file you edit to reskin this template.
   Change brand, colours, fonts, copy, products. Nothing else.
   ============================================================ */

window.SITE = {

  /* ---------- 1. BRAND ---------- */
  brand: {
    name: "MERIDIAN",
    wordmark: "MERIDIAN",
    wordmarkMark: "M",
    tagline: "Instruments of time",
    established: "EST. 1978 · GENEVA",
    email: "care@meridian.example",
    phone: "+234 800 000 0000",
    whatsapp: "2348117500831",
    whatsappMessage: "Hi Ridwan, I saw the MERIDIAN demo store. I'd like to talk about a build.",
    social: { instagram: "#", tiktok: "#", x: "#" },
    year: 2026,
    /* Set to null to hide the disclaimer ribbon on a real client build. */
    conceptNotice: "MERIDIAN is a fictitious brand. This is a demo store, nothing here is for sale."
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
    bg:        "#0A0A0B",
    bg2:       "#101012",
    surface:   "#16161A",
    ink:       "#F2EFE9",
    accent:    "#C8A96A",
    accentDim: "#8A6C34",
    radius:    "2px",
    fontDisplay: "'Bodoni Moda', 'Times New Roman', serif",
    fontBody:    "'Jost', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    googleFonts: "family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@200;300;400;500"
  },

  /* ---------- 3. MONEY ---------- */
  currency: { symbol: "₦", locale: "en-NG", decimals: 0 },

  /* ---------- 4. NAV ---------- */
  nav: [
    { label: "Collection", href: "collection.html" },
    { label: "Chronographs", href: "collection.html?c=Chronograph" },
    { label: "Atelier", href: "index.html#atelier" },
    { label: "Journal", href: "index.html#reviews" },
    { label: "Support", href: "index.html#faq" }
  ],

  /* ---------- 5. TICKER ---------- */
  ticker: [
    "Complimentary nationwide delivery",
    "Five-year international warranty",
    "Hand-assembled in-house",
    "Pay on delivery in Lagos",
    "30-day return, no questions"
  ],

  /* ---------- 6. HERO ---------- */
  hero: {
    eyebrow: "Chapter Nine · The Considered Hour",
    headline: ["Time, worn", "with intent."],
    italicWord: "intent.",
    sub: "Mechanical watches built one at a time, for people who measure a day by what they finish rather than what they start.",
    ctaPrimary: { label: "View the collection", href: "collection.html" },
    ctaSecondary: { label: "Speak to a specialist", href: "wa" },
    image: "assets/img/hero.webp",
    caption: "Ref. 04 · Calibre M-712 · Steel on steel"
  },

  /* ---------- 7. FEATURED ---------- */
  featured: {
    index: "01",
    label: "The Collection",
    title: "Eight references. No filler.",
    sub: "Every piece in the range earns its place. We would rather make one watch properly than nine of them quickly.",
    linkLabel: "All references",
    linkHref: "collection.html",
    ids: ["m-01", "m-03", "m-04", "m-07"]
  },

  /* ---------- 8. EDITORIAL — MOVEMENT ---------- */
  movement: {
    index: "02",
    label: "The Calibre",
    title: "Two hundred and sixteen parts, and not one of them decorative.",
    body: "Our in-house calibre is assembled by hand in a room of eleven people. It is regulated in five positions over fourteen days before it is allowed to leave. That is slower than it needs to be, and we have made peace with it.",
    image: "assets/img/editorial-movement.webp",
    imageAlt: "Macro view of an open-worked mechanical watch movement",
    stats: [
      { value: 216, suffix: "",  label: "Components per calibre" },
      { value: 72,  suffix: "h", label: "Power reserve" },
      { value: 14,  suffix: " days", label: "Regulated before release" },
      { value: 5,   suffix: " yr", label: "International warranty" }
    ]
  },

  /* ---------- 9. PINNED HORIZONTAL STORY ---------- */
  story: {
    index: "03",
    label: "Anatomy",
    title: "Four decisions behind every dial.",
    panels: [
      { n: "I",   title: "The case", body: "316L steel, milled from solid bar, then brushed and polished by hand in seven passes. Nothing is cast.", image: "assets/img/editorial-detail.webp" },
      { n: "II",  title: "The dial",  body: "Sunburst finishing applied under lamp light so the grain reads the same at arm's length as it does at the bench.", image: "assets/img/product-08.webp" },
      { n: "III", title: "The movement", body: "Assembled, disassembled, cleaned, assembled again. The second build is the one that ships.", image: "assets/img/editorial-movement.webp" },
      { n: "IV",  title: "The hand", body: "One watchmaker signs off each reference. If it comes back, it comes back to them.", image: "assets/img/editorial-atelier.webp" }
    ]
  },

  /* ---------- 10. GIFT / PROMO BANNER ---------- */
  promo: {
    kicker: "The Presentation Set",
    title: "Two pieces, one box, one story.",
    body: "A paired set in a hand-stitched leather case. Made in a run of two hundred, then not again.",
    cta: { label: "See the set", href: "collection.html?c=Sets" },
    image: "assets/img/gift-set.webp"
  },

  /* ---------- 11. VALUE PROPS ---------- */
  valueProps: {
    index: "04",
    label: "Ownership",
    title: "What you get after the box is opened.",
    image: "assets/img/lifestyle-wrist.webp",
    items: [
      { title: "Serviced for life", body: "Bring it back at any point. We will open it, clean it, and regulate it. You pay for parts only." },
      { title: "Delivered in 48 hours", body: "Lagos same day where we can. Everywhere else in Nigeria inside two working days, insured." },
      { title: "Try it for 30 days", body: "Wear it properly. If it is not the one, send it back unworn-condition and we refund in full." },
      { title: "A real person", body: "One number, one inbox, answered by someone who has handled the watch you are asking about." }
    ]
  },

  /* ---------- 12. ATELIER ---------- */
  atelier: {
    index: "05",
    label: "The Atelier",
    title: "Eleven people. Forty-eight watches a month.",
    body: [
      "We are not trying to grow into a factory. The bench count is capped on purpose, because the moment you add a twelfth pair of hands you start writing procedures instead of building watches.",
      "Everything is done in one room: casing, regulation, final inspection. The person who signs the certificate is the person who closed the caseback."
    ],
    image: "assets/img/editorial-atelier.webp",
    signature: "Adaeze O. · Head of Atelier"
  },

  /* ---------- 13. REVIEWS ---------- */
  reviews: {
    index: "06",
    label: "Owners",
    title: "What people say once it is on the wrist.",
    items: [
      { rating: 5, text: "I have owned two watches at four times this price and neither of them felt this considered. The finishing on the lugs is absurd for the money.", name: "Tunde A.", place: "Lagos, Nigeria", product: "m-01" },
      { rating: 5, text: "Ordered on a Tuesday, wore it to a wedding on Thursday. Packaging alone made it feel like a proper occasion.", name: "Amara N.", place: "Abuja, Nigeria", product: "m-08" },
      { rating: 5, text: "The strap broke in about a week and looks better now than the day it arrived. That never happens.", name: "Ibrahim K.", place: "Kano, Nigeria", product: "m-02" },
      { rating: 5, text: "Bought it as a gift and quietly regretted giving it away. Ended up buying the black one for myself.", name: "Chisom E.", place: "Port Harcourt, Nigeria", product: "m-07" },
      { rating: 5, text: "Support answered on WhatsApp in four minutes on a Sunday. Sized the bracelet free when I collected it.", name: "Halima S.", place: "Kaduna, Nigeria", product: "m-03" }
    ]
  },

  /* ---------- 14. FAQ ---------- */
  faq: {
    index: "07",
    label: "Questions",
    title: "Before you order.",
    items: [
      { q: "How long does delivery take?", a: "Orders leave the atelier within 24 hours. Lagos is usually same day or next morning. Everywhere else in Nigeria lands inside two working days. International is three to six, fully insured and tracked." },
      { q: "Are these mechanical or quartz?", a: "Six of the eight references are automatic mechanical, running our in-house M-712 calibre. Two are high-accuracy quartz, and we say so plainly on the product page rather than hiding it in the specification table." },
      { q: "Can I return it?", a: "Thirty days. Wear it, sleep in it, take it out. If you send it back in unworn condition with the box and papers we refund in full, including what you paid for delivery." },
      { q: "What does the warranty actually cover?", a: "Five years on the movement and case against manufacturing fault. It does not cover water damage from a crown left unscrewed or a drop onto tile, but bring it in anyway and we will quote you honestly." },
      { q: "Do you service watches you did not make?", a: "Yes, for mechanical pieces. Send a photo of the caseback on WhatsApp and we will tell you whether it is worth doing before you pay anything." },
      { q: "How do I pay?", a: "Card, bank transfer, or pay on delivery within Lagos. Split payment over three months is available on anything above ₦150,000." }
    ]
  },

  /* ---------- 15. NEWSLETTER + FOOTER ---------- */
  newsletter: {
    title: "One letter a month.",
    body: "New references, restock notices, and the occasional note from the bench. No campaigns, no countdown timers.",
    placeholder: "Your email address",
    cta: "Subscribe"
  },
  footer: {
    columns: [
      { title: "Shop", links: [
        { label: "All references", href: "collection.html" },
        { label: "Chronographs", href: "collection.html?c=Chronograph" },
        { label: "Dress", href: "collection.html?c=Dress" },
        { label: "Tool watches", href: "collection.html?c=Tool" },
        { label: "Presentation sets", href: "collection.html?c=Sets" }
      ]},
      { title: "Care", links: [
        { label: "Delivery", href: "index.html#faq" },
        { label: "Returns", href: "index.html#faq" },
        { label: "Warranty", href: "index.html#faq" },
        { label: "Servicing", href: "index.html#faq" },
        { label: "Sizing guide", href: "index.html#faq" }
      ]},
      { title: "House", links: [
        { label: "The atelier", href: "index.html#atelier" },
        { label: "The calibre", href: "index.html#calibre" },
        { label: "Owners", href: "index.html#reviews" },
        { label: "Contact", href: "index.html#faq" }
      ]}
    ],
    legal: "All rights reserved.",
    payments: ["VISA", "Mastercard", "Verve", "Transfer", "Pay on delivery"]
  },

  /* ---------- 16. PRODUCTS ---------- */
  categories: ["All", "Chronograph", "Dress", "Tool", "Sets"],

  products: [
    {
      id: "m-01", name: "Meridian Chronograph 41", ref: "Ref. M-041",
      category: "Chronograph", badge: "Signature",
      price: 268000, compareAt: 310000,
      image: "assets/img/product-01.webp",
      gallery: ["assets/img/product-01.webp", "assets/img/editorial-detail.webp", "assets/img/lifestyle-wrist.webp", "assets/img/editorial-movement.webp"],
      short: "Steel on steel, black sunburst dial, three registers.",
      blurb: "The reference the house is known for. A 41mm chronograph with a black sunburst dial that reads flat matte in shade and opens up completely in daylight. Three registers, no date window, nothing on the dial that is not doing a job.",
      rating: 4.9, reviewCount: 128, stock: 6,
      variants: { label: "Bracelet", options: ["Steel bracelet", "Black leather", "Navy rubber"] },
      specs: [
        ["Movement", "M-712 automatic chronograph"],
        ["Case", "41mm · 316L steel · sapphire"],
        ["Dial", "Black sunburst, applied indices"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "100m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-02", name: "Meridian Classique 38", ref: "Ref. M-038",
      category: "Dress", badge: "",
      price: 189000, compareAt: 0,
      image: "assets/img/product-02.webp",
      gallery: ["assets/img/product-02.webp", "assets/img/editorial-movement.webp", "assets/img/editorial-detail.webp"],
      short: "Gold case, ivory dial, alligator strap.",
      blurb: "A dress watch that stays under a cuff. 38mm, gold case, ivory lacquer dial, blued hands. It does one thing well and disappears the rest of the time.",
      rating: 4.8, reviewCount: 74, stock: 4,
      variants: { label: "Strap", options: ["Chocolate alligator", "Black alligator", "Cognac calf"] },
      specs: [
        ["Movement", "M-712 automatic"],
        ["Case", "38mm · gold-plated steel"],
        ["Dial", "Ivory lacquer, blued hands"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "30m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-03", name: "Meridian Sub 300", ref: "Ref. M-300",
      category: "Tool", badge: "Low stock",
      price: 245000, compareAt: 279000,
      image: "assets/img/product-03.webp",
      gallery: ["assets/img/product-03.webp", "assets/img/editorial-detail.webp", "assets/img/lifestyle-wrist.webp"],
      short: "Ceramic bezel, midnight dial, 300m.",
      blurb: "Built for water and treated badly on purpose during testing. Ceramic bezel with a lume pip that still reads at 3am, midnight blue sunburst dial, screw-down crown.",
      rating: 4.9, reviewCount: 96, stock: 3,
      variants: { label: "Bracelet", options: ["Steel bracelet", "Navy rubber", "Grey NATO"] },
      specs: [
        ["Movement", "M-712 automatic"],
        ["Case", "40mm · 316L steel · ceramic bezel"],
        ["Dial", "Midnight blue sunburst"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "300m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-04", name: "Meridian Skeleton Or", ref: "Ref. M-901",
      category: "Dress", badge: "Atelier piece",
      price: 420000, compareAt: 0,
      image: "assets/img/product-04.webp",
      gallery: ["assets/img/product-04.webp", "assets/img/editorial-movement.webp", "assets/img/editorial-atelier.webp"],
      short: "Rose gold, open-worked dial, hand-finished bridges.",
      blurb: "The one we make forty of a year. The dial is removed entirely so the calibre becomes the face, which means every bridge has to be finished as if it were the front. It is.",
      rating: 5.0, reviewCount: 31, stock: 2,
      variants: { label: "Strap", options: ["Black alligator", "Brown alligator"] },
      specs: [
        ["Movement", "M-712 SK open-worked automatic"],
        ["Case", "40mm · rose gold PVD"],
        ["Dial", "Fully skeletonised"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "30m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-05", name: "Meridian Field 39", ref: "Ref. M-039",
      category: "Tool", badge: "",
      price: 142000, compareAt: 165000,
      image: "assets/img/product-05.webp",
      gallery: ["assets/img/product-05.webp", "assets/img/lifestyle-wrist.webp", "assets/img/editorial-detail.webp"],
      short: "Matte black case, canvas strap, full lume.",
      blurb: "The watch we hand to people who say they are hard on watches. Matte black case that will not show a scratch, cream numerals with full lume, canvas strap you can rinse in a sink.",
      rating: 4.7, reviewCount: 58, stock: 12,
      variants: { label: "Strap", options: ["Olive canvas", "Black canvas", "Sand canvas"] },
      specs: [
        ["Movement", "M-712 automatic"],
        ["Case", "39mm · PVD-coated steel"],
        ["Dial", "Matte black, full lume"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "100m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-06", name: "Meridian Minute 36", ref: "Ref. M-036",
      category: "Dress", badge: "New",
      price: 98000, compareAt: 0,
      image: "assets/img/product-06.webp",
      gallery: ["assets/img/product-06.webp", "assets/img/editorial-detail.webp"],
      short: "Milanese mesh, blank white dial, 6.9mm thin.",
      blurb: "Our quietest reference and the one people buy second. No numerals, no date, no branding on the dial beyond the mark at twelve. Quartz, deliberately, so it is 6.9mm thin.",
      rating: 4.6, reviewCount: 41, stock: 18,
      variants: { label: "Strap", options: ["Silver mesh", "Black mesh", "Tan leather"] },
      specs: [
        ["Movement", "High-accuracy quartz"],
        ["Case", "36mm · brushed steel"],
        ["Dial", "Matte white, unmarked"],
        ["Battery life", "4 years"],
        ["Water resistance", "50m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-07", name: "Meridian Noir Chrono", ref: "Ref. M-041N",
      category: "Chronograph", badge: "Best seller",
      price: 289000, compareAt: 0,
      image: "assets/img/product-07.webp",
      gallery: ["assets/img/product-07.webp", "assets/img/editorial-detail.webp", "assets/img/lifestyle-wrist.webp"],
      short: "Black ceramic throughout, single copper seconds hand.",
      blurb: "Black ceramic case, black bracelet, black dial, and one copper seconds hand so you can still tell it is running. Ceramic will not scratch, will not warm up, and will not go out of style.",
      rating: 4.9, reviewCount: 112, stock: 5,
      variants: { label: "Bracelet", options: ["Ceramic bracelet", "Black rubber"] },
      specs: [
        ["Movement", "M-712 automatic chronograph"],
        ["Case", "41mm · black ceramic"],
        ["Dial", "Black, copper seconds"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "100m"],
        ["Warranty", "5 years international"]
      ]
    },
    {
      id: "m-08", name: "Meridian Bicolore 39", ref: "Ref. M-039B",
      category: "Chronograph", badge: "",
      price: 315000, compareAt: 358000,
      image: "assets/img/product-08.webp",
      gallery: ["assets/img/product-08.webp", "assets/img/editorial-detail.webp", "assets/img/gift-set.webp"],
      short: "Steel and gold, champagne dial, date at three.",
      blurb: "Two-tone done without apology. Steel case, gold centre links, champagne sunburst dial that shifts from cream to bronze depending on where you are standing.",
      rating: 4.8, reviewCount: 63, stock: 7,
      variants: { label: "Bracelet", options: ["Two-tone bracelet", "Brown leather"] },
      specs: [
        ["Movement", "M-712 automatic"],
        ["Case", "39mm · steel and gold"],
        ["Dial", "Champagne sunburst, date"],
        ["Power reserve", "72 hours"],
        ["Water resistance", "50m"],
        ["Warranty", "5 years international"]
      ]
    }
  ]
};
