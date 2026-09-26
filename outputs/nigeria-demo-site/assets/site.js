// Lumora Skin — demo store data + shared logic
// Built by Koolestpro. This is the D2a reference demo / D3 base template.

const WA_NUMBER = "2348012345678"; // demo placeholder number, international format no "+"
const STORE_NAME = "Lumora Skin";

const PRODUCTS = [
  {
    id: "gentle-foaming-cleanser",
    name: "Gentle Foaming Cleanser",
    category: "Cleansers",
    price: 9500,
    oldPrice: null,
    rating: 4.8,
    reviews: 132,
    badge: "Best Seller",
    img: "assets/products/cleanser.png",
    blurb: "A soft, sulphate-free daily cleanser that lifts dirt and sunscreen without stripping your skin, built for Lagos humidity.",
    variants: ["Standard 150ml", "Travel 50ml"],
  },
  {
    id: "vitamin-c-brightening-serum",
    name: "Vitamin C Brightening Serum",
    category: "Serums",
    price: 18000,
    oldPrice: 21000,
    rating: 4.9,
    reviews: 208,
    badge: "Best Seller",
    img: "assets/products/serum.png",
    blurb: "10% stabilised vitamin C plus vitamin E to fade dark spots and even out tone. Lightweight, fast-absorbing, no white cast.",
    variants: ["Standard 30ml", "Travel 10ml"],
  },
  {
    id: "shea-ceramide-moisturizer",
    name: "Shea & Ceramide Moisturizer",
    category: "Moisturizers",
    price: 14500,
    oldPrice: 17000,
    rating: 4.7,
    reviews: 96,
    badge: "Sale",
    img: "assets/products/moisturizer.png",
    blurb: "Locally sourced shea butter with ceramides to lock in moisture all day, without feeling heavy under makeup or sunscreen.",
    variants: ["Standard 50ml", "Jumbo 100ml"],
  },
  {
    id: "rosewater-balancing-toner",
    name: "Rosewater Balancing Toner",
    category: "Toners",
    price: 11000,
    oldPrice: null,
    rating: 4.6,
    reviews: 74,
    badge: null,
    img: "assets/products/toner.png",
    blurb: "Alcohol-free rosewater mist that rebalances your skin after cleansing and preps it to absorb serum better.",
    variants: ["Standard 100ml"],
  },
  {
    id: "purifying-clay-mask",
    name: "Purifying Clay Mask",
    category: "Masks",
    price: 13000,
    oldPrice: null,
    rating: 4.8,
    reviews: 61,
    badge: "Hot",
    img: "assets/products/mask.png",
    blurb: "Black clay and charcoal draw out excess oil and congestion, twice a week, without leaving skin tight or dry.",
    variants: ["Standard 60g"],
  },
  {
    id: "daily-defence-spf-50",
    name: "Daily Defence SPF 50",
    category: "Sunscreen",
    price: 16500,
    oldPrice: null,
    rating: 4.9,
    reviews: 154,
    badge: "Best Seller",
    img: "assets/products/sunscreen.png",
    blurb: "A weightless, no white-cast SPF 50 built for melanin-rich skin and Lagos sun, reapplies clean over makeup.",
    variants: ["Standard 50ml"],
  },
  {
    id: "whipped-shea-body-butter",
    name: "Whipped Shea Body Butter",
    category: "Body",
    price: 15000,
    oldPrice: null,
    rating: 4.8,
    reviews: 88,
    badge: null,
    img: "assets/products/body-butter.png",
    blurb: "Deeply hydrating whipped shea for elbows, knees and everywhere the AC dries out. Sinks in fast, no greasy film.",
    variants: ["Standard 200g", "Jumbo 400g"],
  },
  {
    id: "charcoal-detox-bar",
    name: "Charcoal Detox Bar",
    category: "Body",
    price: 6500,
    oldPrice: null,
    rating: 4.5,
    reviews: 47,
    badge: null,
    img: "assets/products/soap.png",
    blurb: "A gentle, handmade charcoal bar for body and back, made to clear congestion without over-drying skin.",
    variants: ["Standard 120g"],
  },
  {
    id: "renewing-eye-cream",
    name: "Renewing Eye Cream",
    category: "Moisturizers",
    price: 17500,
    oldPrice: 20500,
    rating: 4.7,
    reviews: 52,
    badge: "New",
    img: "assets/products/eye-cream.png",
    blurb: "A light peptide eye cream for tired mornings and long AC-lit days, softens fine lines without tugging delicate skin.",
    variants: ["Standard 15ml"],
  },
  {
    id: "shea-tinted-lip-balm",
    name: "Shea Tinted Lip Balm",
    category: "Body",
    price: 5500,
    oldPrice: null,
    rating: 4.6,
    reviews: 39,
    badge: "New",
    img: "assets/products/lip-balm.png",
    blurb: "A sheer terracotta tint with shea and vitamin E, keeps lips soft through harmattan without feeling waxy.",
    variants: ["Standard 4g"],
  },
  {
    id: "brown-sugar-body-scrub",
    name: "Brown Sugar Body Scrub",
    category: "Body",
    price: 12500,
    oldPrice: null,
    rating: 4.7,
    reviews: 58,
    badge: "Hot",
    img: "assets/products/scrub.png",
    blurb: "Coarse brown sugar in a shea-oil base, buffs away dry patches in the shower without stripping your skin barrier.",
    variants: ["Standard 200g"],
  },
  {
    id: "lumora-essentials-gift-set",
    name: "Lumora Essentials Gift Set",
    category: "Gift Sets",
    price: 32000,
    oldPrice: 38500,
    rating: 4.9,
    reviews: 44,
    badge: "Sale",
    img: "assets/products/gift-set.png",
    blurb: "Cleanser, moisturizer and a detox bar in a ribboned box, our most-gifted set for birthdays and owambe favours.",
    variants: ["Standard Set"],
  },
];

const TESTIMONIALS = [
  { name: "Bisola A.", city: "Lekki, Lagos", quote: "My skin has never held up this well through harmattan. The eye cream is now non-negotiable.", product: "Renewing Eye Cream" },
  { name: "Chiamaka O.", city: "Enugu", quote: "Ordered on WhatsApp on a Tuesday, had it Thursday morning. The serum genuinely faded my dark spots in 3 weeks.", product: "Vitamin C Brightening Serum" },
  { name: "Tunde K.", city: "Abuja", quote: "Got the gift set for my sister's birthday and she has reordered twice since. Packaging alone is worth it.", product: "Lumora Essentials Gift Set" },
  { name: "Ifeoma N.", city: "Port Harcourt", quote: "Finally a sunscreen that doesn't leave a white cast on my skin tone. I've told everyone in my office group chat.", product: "Daily Defence SPF 50" },
];

const FEATURES = [
  { icon: "🌿", title: "Made for Lagos skin", text: "Formulated and tested in real heat, humidity and harmattan, not imported from somewhere cold." },
  { icon: "💬", title: "Order on WhatsApp", text: "No app, no card details online. Chat, confirm, pay on delivery in Lagos." },
  { icon: "🚚", title: "Fast, tracked delivery", text: "Same-day within Lagos, 2-4 working days nationwide, every order confirmed before it ships." },
  { icon: "↩️", title: "7-day exchange", text: "Wrong size or a WhatsApp mix-up? Unopened items can be swapped within a week." },
];

const FAQS = [
  { q: "How long does delivery take?", a: "Orders confirmed before 2pm ship same-day within Lagos. Nationwide delivery is 2-4 working days via courier, tracked and confirmed in your WhatsApp chat." },
  { q: "Do you offer returns or exchanges?", a: "Unopened items can be swapped within 7 days if a WhatsApp order was misconfirmed on size or scent. Message us with your order details to start it." },
  { q: "What payment methods do you accept?", a: "Pay on delivery within Lagos, or bank transfer confirmed in chat before nationwide dispatch. No card details are ever collected on this site." },
  { q: "Is Lumora suitable for sensitive or oily skin?", a: "Yes. Every formula is fragrance-light and dermatologist-reviewed. Full ingredient lists are shared on request before you order." },
];

function nairaFmt(n) {
  return "₦" + n.toLocaleString("en-NG");
}

function getProduct(id) {
  return PRODUCTS.find((p) => p.id === id);
}

function stars(rating) {
  const full = Math.round(rating);
  return "★".repeat(full) + "☆".repeat(5 - full);
}

const BADGE_CLASS = { "Best Seller": "badge-seller", "New": "badge-new", "Hot": "badge-hot", "Sale": "badge-sale" };

// Shared product card markup, used on the homepage and the collection grid.
function productCardHtml(p) {
  const badge = p.badge ? `<span class="p-badge ${BADGE_CLASS[p.badge] || ""}">${p.badge}</span>` : "";
  const oldPrice = p.oldPrice ? `<span class="old">${nairaFmt(p.oldPrice)}</span>` : "";
  return `
    <a class="card" href="product.html?id=${p.id}">
      <div class="thumb">${badge}<img src="${p.img}" alt="${p.name}" loading="lazy"></div>
      <div class="info">
        <div class="cat">${p.category}</div>
        <h3>${p.name}</h3>
        <div class="card-rating">${stars(p.rating)} <span>(${p.reviews})</span></div>
        <div class="price">${nairaFmt(p.price)} ${oldPrice}</div>
      </div>
    </a>`;
}

function waLink(message) {
  return `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(message)}`;
}

// Renders the persistent sticky WhatsApp bar. Pass a product to prefill
// a message about that specific item; omit it for a generic store greeting.
function renderWaBar(product) {
  const el = document.getElementById("wa-bar");
  if (!el) return;
  const message = product
    ? `Hi ${STORE_NAME}! I'm interested in the ${product.name} (${nairaFmt(product.price)}). Is it available?`
    : `Hi ${STORE_NAME}! I'd like to ask about your products.`;
  el.innerHTML = `<a href="${waLink(message)}" target="_blank" rel="noopener">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-5.5 0-9.96 4.46-9.96 9.96 0 1.76.46 3.48 1.34 5L2 22l5.2-1.36a9.9 9.9 0 0 0 4.84 1.23h.01c5.5 0 9.96-4.46 9.96-9.96S17.54 2 12.04 2zm0 18.2c-1.5 0-2.97-.4-4.26-1.16l-.3-.18-3.08.8.82-3-.2-.31a8.18 8.18 0 0 1-1.26-4.4c0-4.53 3.69-8.22 8.23-8.22 4.53 0 8.22 3.69 8.22 8.22 0 4.53-3.69 8.25-8.17 8.25zm4.52-6.16c-.25-.12-1.47-.72-1.7-.81-.23-.08-.4-.12-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.04-.38-1.98-1.22-.73-.65-1.22-1.46-1.37-1.7-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.25.25-.4.08-.17.04-.31-.02-.44-.06-.12-.56-1.35-.77-1.85-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.87.85-.87 2.08 0 1.22.89 2.4 1.02 2.57.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.11-.23-.17-.48-.29z"/></svg>
    Message on WhatsApp</a>`;
}

// Quick-add-to-cart intent that also lands on WhatsApp, since this demo has
// no real cart/checkout by design (D3: frontend only, WhatsApp handoff).
function messageAboutProduct(product, variant, qty) {
  const v = variant ? ` (${variant})` : "";
  const q = qty && qty > 1 ? ` x${qty}` : "";
  const msg = `Hi ${STORE_NAME}! I'd like to order the ${product.name}${v}${q} — ${nairaFmt(product.price)}. Please confirm availability and delivery to my area.`;
  window.open(waLink(msg), "_blank", "noopener");
}

document.addEventListener("DOMContentLoaded", () => {
  renderWaBar(window.__pdpProduct || null);
});
