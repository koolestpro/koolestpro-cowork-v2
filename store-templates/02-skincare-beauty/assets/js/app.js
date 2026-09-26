/* ============================================================
   Store template runtime (v2)
   Renders every page from site.config.js, then wires the motion.
   You should not need to edit this file to reskin the store.

   v2 changes over the Template 01 engine, all backwards compatible:
   - every user-facing string comes from config.labels, with the
     Template 01 wording as the default
   - section anchor ids come from config, so nav links can read
     #formula instead of #calibre in a non-watch vertical
   - theme injects light-mode-safe tokens (onAccent, line, ink2,
     scrim, shadow, radiusLg) instead of hard-coding dark values
   ============================================================ */
(function () {
  "use strict";

  var S = window.SITE;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------
     LABELS — every string the engine renders on its own
  --------------------------------------------------------- */
  var DEFAULT_LABELS = {
    itemSingular: "piece",
    itemPlural: "pieces",
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
    taxNote: "Delivery calculated at checkout.",
    inStock: "In stock, ships within 24 hours",
    lowStock: "Only {n} left",
    assurances: [],
    footerBlurb: "",
    faqAside: "Still unsure? Message us and a person will answer.",
    faqCta: "Ask on WhatsApp",
    subtotal: "Subtotal",
    delivery: "Delivery",
    deliveryNote: "Calculated at checkout",
    total: "Total"
  };
  var L = Object.assign({}, DEFAULT_LABELS, S.labels || {});

  function anchorOf(section, fallback) {
    return (S[section] && S[section].anchor) || fallback;
  }

  /* ---------------------------------------------------------
     THEME
  --------------------------------------------------------- */
  function injectTheme() {
    var t = S.theme, r = document.documentElement.style;
    var map = {
      "--bg": t.bg,
      "--bg2": t.bg2,
      "--surface": t.surface,
      "--ink": t.ink,
      "--accent": t.accent,
      "--accent-dim": t.accentDim,
      "--on-accent": t.onAccent || "#0A0A0B",
      "--line": t.line || "rgba(32,27,22,.16)",
      "--line-soft": t.lineSoft || "rgba(32,27,22,.09)",
      "--ink-2": t.ink2 || "rgba(32,27,22,.68)",
      "--ink-3": t.ink3 || "rgba(32,27,22,.46)",
      "--scrim": t.scrim || "251,246,239",
      "--shadow": t.shadow || "0 18px 50px -28px rgba(70,44,26,.42)",
      "--radius": t.radius,
      "--radius-lg": t.radiusLg || t.radius,
      "--font-display": t.fontDisplay,
      "--font-body": t.fontBody
    };
    Object.keys(map).forEach(function (k) { if (map[k]) r.setProperty(k, map[k]); });

    var pre = document.createElement("link");
    pre.rel = "preconnect"; pre.href = "https://fonts.gstatic.com"; pre.crossOrigin = "";
    document.head.appendChild(pre);
    var f = document.createElement("link");
    f.rel = "stylesheet";
    f.href = "https://fonts.googleapis.com/css2?" + t.googleFonts + "&display=swap";
    document.head.appendChild(f);

    var m = document.createElement("meta");
    m.name = "theme-color"; m.content = t.bg;
    document.head.appendChild(m);
  }

  /* ---------------------------------------------------------
     HELPERS
  --------------------------------------------------------- */
  function money(n) {
    return S.currency.symbol + Number(n).toLocaleString(S.currency.locale, {
      minimumFractionDigits: S.currency.decimals, maximumFractionDigits: S.currency.decimals
    });
  }
  function pctOff(p, c) { return c && c > p ? Math.round((1 - p / c) * 100) : 0; }
  function byId(id) { return S.products.filter(function (p) { return p.id === id; })[0]; }
  function stars(n) {
    var out = "", full = Math.round(n);
    for (var i = 0; i < 5; i++) out += i < full ? "★" : "☆";
    return out;
  }
  function waLink() {
    return "https://wa.me/" + S.brand.whatsapp + "?text=" + encodeURIComponent(S.brand.whatsappMessage);
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function qs(name) { return new URLSearchParams(window.location.search).get(name); }

  var ICON = {
    arrow: '<svg width="13" height="9" viewBox="0 0 13 9" fill="none"><path d="M8.5 1L12 4.5L8.5 8M12 4.5H0" stroke="currentColor" stroke-width="1.2"/></svg>',
    bag: '<svg width="17" height="18" viewBox="0 0 17 18" fill="none"><path d="M1 5.5h15L15 17H2L1 5.5Z" stroke="currentColor" stroke-width="1.2"/><path d="M5.5 7.5V4a3 3 0 0 1 6 0v3.5" stroke="currentColor" stroke-width="1.2"/></svg>',
    search: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5.4" stroke="currentColor" stroke-width="1.2"/><path d="M11 11l4 4" stroke="currentColor" stroke-width="1.2"/></svg>',
    close: '<svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M1 1l13 13M14 1L1 14" stroke="currentColor" stroke-width="1.2"/></svg>',
    check: '<svg width="16" height="12" viewBox="0 0 16 12" fill="none"><path d="M1 6l4.5 4.5L15 1" stroke="currentColor" stroke-width="1.4"/></svg>',
    leaf: '<svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M14 2C6 2 2 5.5 2 10.5c0 1.4.4 2.4.4 2.4S5 8 10 6c0 0-4 2.6-6.2 7.6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>',
    wa: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2c-5.5 0-9.96 4.46-9.96 9.96 0 1.76.46 3.48 1.34 5L2 22l5.2-1.36a9.9 9.9 0 0 0 4.84 1.23c5.5 0 9.96-4.46 9.96-9.96S17.54 2 12.04 2zm5.8 14.06c-.24.68-1.4 1.3-1.94 1.34-.5.04-.98.22-3.3-.7-2.78-1.1-4.54-3.94-4.68-4.12-.14-.18-1.12-1.5-1.12-2.86s.7-2.02.96-2.3c.24-.26.54-.32.72-.32h.52c.16 0 .4-.06.62.48.24.58.8 2 .88 2.14.06.14.1.3.02.48-.36.72-.74 1.08-.5 1.5.9 1.54 1.8 2.08 3.16 2.76.22.1.36.08.5-.06.14-.16.58-.68.74-.92.16-.24.3-.2.5-.12.22.08 1.36.64 1.6.76.24.12.4.18.46.28.06.1.06.58-.14 1.14z"/></svg>',
    ext: '<svg width="9" height="9" viewBox="0 0 10 10" fill="none" style="margin-left:5px"><path d="M2 8L8 2M8 2H3.4M8 2v4.6" stroke="currentColor" stroke-width="1.2"/></svg>'
  };

  /* ---------------------------------------------------------
     SHARED CHROME
  --------------------------------------------------------- */
  function chromeTop() {
    var h = '<div id="topbar">';

    var bb = S.builtBy;
    if (S.brand.conceptNotice || bb) {
      h += '<div class="concept-ribbon">' +
        (S.brand.conceptNotice ? '<span><b>◆</b> ' + esc(S.brand.conceptNotice) + "</span>" : "") +
        (bb ? '<a class="ribbon-credit" href="' + bb.url + '" target="_blank" rel="noopener">' +
              esc(bb.ribbonCredit) + " <b>" + esc(bb.domain) + "</b>" + ICON.ext + "</a>" : "") +
        "</div>";
    }

    var t = S.ticker.concat(S.ticker).map(function (x) { return "<span>" + esc(x) + "</span>"; }).join("");
    h += '<div class="ticker"><div class="ticker-track">' + t + "</div></div>";

    h += '<header class="hdr" id="hdr"><div class="wrap hdr-in">' +
      '<a href="index.html" class="logo">' + esc(S.brand.wordmark) + "<small>" + esc(S.brand.established) + "</small></a>" +
      '<nav class="hdr-nav">' + S.nav.map(function (n) {
        return '<a href="' + n.href + '">' + esc(n.label) + "</a>";
      }).join("") + "</nav>" +
      '<div class="hdr-act">' +
        '<a class="icon-btn" href="collection.html" aria-label="Search">' + ICON.search + "</a>" +
        '<button class="icon-btn" id="cart-open" aria-label="Open bag">' + ICON.bag +
          '<i class="cart-count num" id="cart-count">0</i></button>' +
        '<button class="burger" id="burger" aria-label="Menu"><i></i></button>' +
      "</div></div></header></div>";

    h += '<div class="mnav" id="mnav"><div>' +
      S.nav.map(function (n) { return '<a class="m-link" href="' + n.href + '">' + esc(n.label) + "</a>"; }).join("") +
      "</div><div class='m-foot'><a href='" + waLink() + "' target='_blank' rel='noopener'>WhatsApp</a><a href='mailto:" +
      S.brand.email + "'>Email</a></div></div>";

    return h;
  }

  function chromeBottom() {
    var nl = S.newsletter;
    var h = '<section class="section wrap" id="newsletter"><div class="nl">' +
      '<div><h2 class="display" data-split>' + esc(nl.title) + "</h2></div>" +
      '<div><p class="lede" data-reveal>' + esc(nl.body) + "</p>" +
      '<form class="nl-form" data-reveal onsubmit="return false;">' +
        '<input type="email" placeholder="' + esc(nl.placeholder) + '" aria-label="Email">' +
        "<button type='submit'>" + esc(nl.cta) + "</button></form>" +
      '<p class="nl-note">No spam. Unsubscribe in one click.</p></div></div></section>';

    h += '<footer class="ftr wrap"><div class="ftr-grid">' +
      "<div><div class='logo' style='font-size:22px'>" + esc(S.brand.wordmark) +
      "<small>" + esc(S.brand.established) + "</small></div>" +
      "<p class='lede' style='margin-top:20px;font-size:14px;max-width:34ch'>" +
      esc(L.footerBlurb || S.brand.tagline + ".") + "</p>" +
      "<div style='margin-top:24px'><a class='link-u' href='" + waLink() + "' target='_blank' rel='noopener'>WhatsApp us " + ICON.arrow + "</a></div></div>" +
      S.footer.columns.map(function (c) {
        return "<div><h4>" + esc(c.title) + "</h4><ul>" + c.links.map(function (l) {
          return '<li><a href="' + l.href + '">' + esc(l.label) + "</a></li>";
        }).join("") + "</ul></div>";
      }).join("") + "</div>" +
      '<div class="ftr-word" aria-hidden="true">' + esc(S.brand.wordmark) + "</div>" +
      '<div class="ftr-bot"><span>© ' + S.brand.year + " " + esc(S.brand.name) + ". " + esc(S.footer.legal) + "</span>" +
      '<div class="pay">' + S.footer.payments.map(function (p) { return "<span>" + esc(p) + "</span>"; }).join("") + "</div></div>" +
      (S.builtBy ? '<div class="ftr-credit">' + esc(S.builtBy.footerCredit) +
        ' <a href="' + S.builtBy.url + '" target="_blank" rel="noopener">' + esc(S.builtBy.domain) + ICON.ext + "</a>" +
        (S.brand.conceptNotice ? '<span class="ftr-disclaim">' + esc(S.brand.conceptNotice) + "</span>" : "") +
        "</div>" : "") +
      "</footer>";

    /* bag drawer + toast + wa float */
    h += '<div class="drawer-bd" id="drawer-bd"></div>' +
      '<aside class="drawer" id="drawer" aria-label="Bag">' +
        '<div class="drawer-hd"><h3>' + esc(L.cartTitle) + '</h3><button class="icon-btn" id="cart-close" aria-label="Close">' + ICON.close + "</button></div>" +
        '<div class="drawer-body" id="drawer-body"></div>' +
        '<div class="drawer-ft"><div class="row"><span>' + esc(L.subtotal) + '</span><span id="cart-sub">' + money(0) + "</span></div>" +
        '<div class="row"><span>' + esc(L.delivery) + "</span><span>" + esc(L.deliveryNote) + "</span></div>" +
        '<div class="row total"><span>' + esc(L.total) + '</span><span id="cart-total">' + money(0) + "</span></div>" +
        '<a class="btn btn-solid btn-block" href="' + waLink() + '" target="_blank" rel="noopener">' + esc(L.checkout) + "</a>" +
        '<button class="btn btn-ghost btn-block btn-sm" id="cart-close-2">' + esc(L.keepLooking) + "</button></div></aside>";

    h += '<div id="toast"></div>';
    h += '<a class="wa-float" href="' + waLink() + '" target="_blank" rel="noopener" aria-label="WhatsApp">' + ICON.wa + "</a>";
    if (S.builtBy) {
      h += '<a class="built-mark" href="' + S.builtBy.url + '" target="_blank" rel="noopener">' +
        '<span class="bm-dot"></span><span class="bm-txt">' + esc(S.builtBy.watermark) + "</span>" + ICON.ext + "</a>";
    }
    h += '<div id="curtain"></div>';
    return h;
  }

  /* ---------------------------------------------------------
     CARDS
  --------------------------------------------------------- */
  function cardHTML(p, i) {
    var alt = p.gallery && p.gallery[1] ? p.gallery[1] : p.image;
    var off = pctOff(p.price, p.compareAt);
    return '<article class="card" data-reveal data-i="' + (i || 0) + '">' +
      '<a class="card-media" href="product.html?id=' + p.id + '">' +
        (p.badge ? '<span class="card-badge">' + esc(p.badge) + "</span>" : "") +
        '<img class="main" src="' + p.image + '" alt="' + esc(p.name) + '" loading="lazy" decoding="async">' +
        '<img class="alt" src="' + alt + '" alt="" aria-hidden="true" loading="lazy" decoding="async">' +
        '<div class="card-quick"><button class="btn btn-sm js-add" data-id="' + p.id + '">' + esc(L.addToCart) + "</button></div>" +
      "</a>" +
      '<div class="card-body"><a href="product.html?id=' + p.id + '">' +
        '<div class="card-ref">' + esc(p.ref) + " · " + esc(p.category) + "</div>" +
        '<h3 class="card-name">' + esc(p.name) + "</h3>" +
        '<p class="card-short">' + esc(p.short) + "</p>" +
        '<div class="card-price num"><span>' + money(p.price) + "</span>" +
          (off ? "<s>" + money(p.compareAt) + '</s><span class="off">−' + off + "%</span>" : "") +
        "</div>" +
        '<div style="margin-top:6px"><span class="stars">' + stars(p.rating) + '</span> <span class="small num">' +
          p.rating.toFixed(1) + " · " + p.reviewCount + " " + esc(L.buyerNoun) + "</span></div>" +
      "</a></div></article>";
  }

  /* ---------------------------------------------------------
     HOME
  --------------------------------------------------------- */
  function renderHome(root) {
    var H = S.hero, h = "";

    /* hero */
    h += '<section class="hero" id="' + anchorOf("hero", "top") + '">' +
      '<div class="hero-bg" data-parallax="0.16"><img src="' + H.image + '" alt="" fetchpriority="high"></div>' +
      '<div class="hero-scrim"></div>' +
      '<div class="hero-in wrap">' +
        '<p class="eyebrow" data-hero-el>' + esc(H.eyebrow) + "</p>" +
        '<h1 class="display">' + H.headline.map(function (l) {
          var txt = esc(l);
          if (H.italicWord && l.indexOf(H.italicWord) > -1) {
            txt = txt.replace(esc(H.italicWord), "<em>" + esc(H.italicWord) + "</em>");
          }
          return '<span class="r-line"><span>' + txt + "</span></span>";
        }).join("") + "</h1>" +
        '<p class="lede" data-hero-el>' + esc(H.sub) + "</p>" +
        '<div class="hero-cta" data-hero-el>' +
          '<a class="btn btn-solid" href="' + H.ctaPrimary.href + '">' + esc(H.ctaPrimary.label) + "</a>" +
          '<a class="btn btn-ghost" href="' + (H.ctaSecondary.href === "wa" ? waLink() : H.ctaSecondary.href) + '" target="_blank" rel="noopener">' + esc(H.ctaSecondary.label) + "</a>" +
        "</div>" +
        '<div class="hero-meta" data-hero-el><span>' + esc(H.caption) + "</span>" +
          '<span class="scroll-cue"><i></i>Scroll</span></div>' +
      "</div></section>";

    /* featured */
    var F = S.featured;
    h += '<section class="section wrap" id="' + anchorOf("featured", "range") + '"><div class="sec-head">' +
      '<div class="left"><div class="sec-index">' + F.index + " / " + esc(F.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(F.title) + "</h2>" +
      '<p class="lede" data-reveal>' + esc(F.sub) + "</p></div>" +
      '<a class="link-u" href="' + F.linkHref + '" data-reveal>' + esc(F.linkLabel) + " " + ICON.arrow + "</a></div>" +
      '<div class="grid grid-4">' + F.ids.map(function (id, i) {
        var p = byId(id); return p ? cardHTML(p, i) : "";
      }).join("") + "</div></section>";

    /* formula editorial */
    var M = S.movement;
    h += '<section class="section wrap band" id="' + anchorOf("movement", "formula") + '"><div class="split">' +
      '<div class="split-media sq" data-parallax="0.09"><img src="' + M.image + '" alt="' + esc(M.imageAlt) + '" loading="lazy"></div>' +
      "<div><div class='sec-index'>" + M.index + " / " + esc(M.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(M.title) + "</h2>" +
      '<p class="lede" data-reveal style="margin-top:22px">' + esc(M.body) + "</p>" +
      '<div class="stat-row" style="margin-top:44px">' + M.stats.map(function (s) {
        return '<div class="stat" data-reveal><div class="v num" data-count="' + s.value + '" data-suffix="' + esc(s.suffix) + '">0</div><div class="l">' + esc(s.label) + "</div></div>";
      }).join("") + "</div></div></div></section>";

    /* pinned routine */
    var T = S.story;
    h += '<section class="story section" id="' + anchorOf("story", "routine") + '"><div class="wrap"><div class="sec-head"><div class="left">' +
      '<div class="sec-index">' + T.index + " / " + esc(T.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(T.title) + "</h2></div></div></div>" +
      '<div class="story-viewport"><div class="story-track" id="story-track">' +
        T.panels.map(function (p) {
          return '<article class="story-panel"><div class="sp-media"><img src="' + p.image + '" alt="' + esc(p.title) + '" loading="lazy"></div>' +
            '<div class="sp-body"><div class="sp-n">' + esc(p.n) + "</div><h3 class='display'>" + esc(p.title) + "</h3><p>" + esc(p.body) + "</p></div></article>";
        }).join("") +
      "</div></div>" +
      '<div class="story-hint"><span>Drag or scroll</span><span class="story-prog"><i id="story-prog"></i></span></div></section>';

    /* promo */
    var P = S.promo;
    h += '<section class="promo" id="' + anchorOf("promo", "sets") + '"><div class="promo-bg" data-parallax="0.12"><img src="' + P.image + '" alt="" loading="lazy"></div>' +
      '<div class="promo-in wrap"><div class="promo-card">' +
      '<p class="eyebrow" data-reveal>' + esc(P.kicker) + "</p>" +
      '<h2 class="display" data-split>' + esc(P.title) + "</h2>" +
      '<p class="lede" data-reveal>' + esc(P.body) + "</p>" +
      '<div style="margin-top:32px" data-reveal><a class="btn btn-solid" href="' + P.cta.href + '">' + esc(P.cta.label) + "</a></div>" +
      "</div></div></section>";

    /* value props */
    var V = S.valueProps;
    h += '<section class="section wrap" id="' + anchorOf("valueProps", "care") + '"><div class="split flip">' +
      '<div class="split-media tall" data-parallax="0.08"><img src="' + V.image + '" alt="" loading="lazy"></div>' +
      "<div><div class='sec-index'>" + V.index + " / " + esc(V.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(V.title) + "</h2>" +
      '<div class="vp-list" style="margin-top:34px">' + V.items.map(function (it, i) {
        return '<div class="vp" data-reveal><div class="n">0' + (i + 1) + '</div><div><h3>' + esc(it.title) + "</h3><p>" + esc(it.body) + "</p></div></div>";
      }).join("") + "</div></div></div></section>";

    /* the kitchen */
    var A = S.atelier;
    h += '<section class="section wrap band" id="' + anchorOf("atelier", "kitchen") + '"><div class="split">' +
      '<div class="split-media tall" data-parallax="0.1"><img src="' + A.image + '" alt="" loading="lazy"></div>' +
      "<div><div class='sec-index'>" + A.index + " / " + esc(A.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(A.title) + "</h2>" +
      A.body.map(function (b) { return '<p class="lede" data-reveal style="margin-top:22px">' + esc(b) + "</p>"; }).join("") +
      '<p class="small" data-reveal style="margin-top:30px;letter-spacing:.2em;text-transform:uppercase">' + esc(A.signature) + "</p>" +
      "</div></div></section>";

    /* reviews */
    var R = S.reviews;
    var revCards = R.items.concat(R.items).map(function (r) {
      var p = byId(r.product) || S.products[0];
      return '<article class="review"><div class="stars">' + stars(r.rating) + "</div>" +
        "<p>" + esc(r.text) + "</p>" +
        /* NOT lazy: the rail sits off-screen horizontally, so lazy thumbs only
           fetch once the marquee carries them in and pop in blank. Ten 44px
           images is cheaper than that. */
        '<div class="rev-foot"><img src="' + p.image + '" alt="' + esc(p.name) + '" decoding="async">' +
        "<div><div class='who'>" + esc(r.name) + ' <span class="verified">✓ Verified</span></div>' +
        "<div class='where'>" + esc(r.place) + " · " + esc(p.name) + "</div></div></div></article>";
    }).join("");
    h += '<section class="section" id="' + anchorOf("reviews", "reviews") + '"><div class="wrap"><div class="sec-head"><div class="left">' +
      '<div class="sec-index">' + R.index + " / " + esc(R.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(R.title) + "</h2></div></div></div>" +
      '<div class="rev-mask"><div class="rev-rail">' + revCards + "</div></div></section>";

    /* faq */
    h += '<section class="section wrap" id="' + anchorOf("faq", "faq") + '"><div class="split" style="align-items:start">' +
      "<div><div class='sec-index'>" + S.faq.index + " / " + esc(S.faq.label) + "</div>" +
      '<h2 class="display" data-split>' + esc(S.faq.title) + "</h2>" +
      '<p class="lede" data-reveal style="margin-top:20px">' + esc(L.faqAside) + "</p>" +
      '<div style="margin-top:26px" data-reveal><a class="btn btn-ghost btn-sm" href="' + waLink() + '" target="_blank" rel="noopener">' + esc(L.faqCta) + "</a></div></div>" +
      '<div class="faq-list">' + S.faq.items.map(function (f) {
        return '<div class="faq-i"><button class="faq-q">' + esc(f.q) + '<span class="pm"></span></button>' +
          '<div class="faq-a"><p>' + esc(f.a) + "</p></div></div>";
      }).join("") + "</div></div></section>";

    root.innerHTML = h;
  }

  /* ---------------------------------------------------------
     COLLECTION
  --------------------------------------------------------- */
  function renderCollection(root) {
    var active = qs("c") || "All";
    if (S.categories.indexOf(active) === -1) active = "All";

    var h = '<section class="page-head wrap">' +
      '<div class="crumbs"><a href="index.html">Home</a> / ' + esc(L.collectionCrumb) + "</div>" +
      '<h1 class="display" data-split>' + esc(L.collectionTitle) + "</h1>" +
      '<p class="lede" data-reveal style="margin-top:20px">' + esc(S.featured.sub) + "</p></section>";

    h += '<div class="wrap"><div class="filters">' +
      '<div class="chips">' + S.categories.map(function (c) {
        return '<button class="chip' + (c === active ? " on" : "") + '" data-cat="' + esc(c) + '">' + esc(c) + "</button>";
      }).join("") + "</div>" +
      '<div class="sort"><span id="count-lbl" class="num"></span><label for="sort">Sort</label>' +
      '<select id="sort"><option value="featured">Featured</option><option value="low">Price, low to high</option>' +
      '<option value="high">Price, high to low</option><option value="rating">Best rated</option></select></div>' +
      "</div>";

    h += '<section class="section" style="padding-top:clamp(32px,4vw,56px)"><div class="grid grid-3" id="grid"></div></section></div>';

    root.innerHTML = h;

    function paint() {
      var cat = $(".chip.on").dataset.cat;
      var sort = $("#sort").value;
      var list = S.products.filter(function (p) {
        return cat === "All" || p.category === cat;
      });
      if (sort === "low") list.sort(function (a, b) { return a.price - b.price; });
      if (sort === "high") list.sort(function (a, b) { return b.price - a.price; });
      if (sort === "rating") list.sort(function (a, b) { return b.rating - a.rating; });
      $("#grid").innerHTML = list.length
        ? list.map(cardHTML).join("")
        : '<p class="lede">Nothing in this category yet. <a class="link-u" href="collection.html">See everything</a></p>';
      $("#count-lbl").textContent = list.length + " " + (list.length === 1 ? L.itemSingular : L.itemPlural);
      bindAdd();
      revealNow($$("#grid .card"));
    }

    $$(".chip").forEach(function (c) {
      c.addEventListener("click", function () {
        $$(".chip").forEach(function (x) { x.classList.remove("on"); });
        c.classList.add("on");
        history.replaceState(null, "", c.dataset.cat === "All" ? "collection.html" : "collection.html?c=" + encodeURIComponent(c.dataset.cat));
        paint();
      });
    });
    $("#sort").addEventListener("change", paint);
    paint();
  }

  /* ---------------------------------------------------------
     PRODUCT
  --------------------------------------------------------- */
  function renderProduct(root) {
    var p = byId(qs("id")) || S.products[0];
    document.title = p.name + " · " + S.brand.name;
    var off = pctOff(p.price, p.compareAt);
    var gal = p.gallery && p.gallery.length ? p.gallery : [p.image];

    var h = '<section class="pdp wrap"><div class="crumbs"><a href="index.html">Home</a> / <a href="collection.html">' +
      esc(L.collectionCrumb) + "</a> / " + esc(p.name) + "</div>";

    h += '<div class="pdp-grid" style="margin-top:26px">' +
      '<div class="pdp-gal"><div class="pdp-main" id="pdp-main"><img src="' + gal[0] + '" alt="' + esc(p.name) + '" id="pdp-img"></div>' +
      '<div class="pdp-thumbs">' + gal.map(function (g, i) {
        return '<button class="' + (i === 0 ? "on" : "") + '" data-src="' + g + '" aria-label="View image ' + (i + 1) + '"><img src="' + g + '" alt="" loading="lazy"></button>';
      }).join("") + "</div></div>";

    h += '<div class="pdp-info">' +
      '<div class="card-ref">' + esc(p.ref) + " · " + esc(p.category) + "</div>" +
      "<h1>" + esc(p.name) + "</h1>" +
      '<div class="pdp-rate"><span class="stars">' + stars(p.rating) + '</span><span class="num">' + p.rating.toFixed(1) +
        "</span><span>·</span><span class='num'>" + p.reviewCount + " " + esc(L.buyerNoun) + "</span></div>" +
      '<div class="pdp-price num"><span class="now">' + money(p.price) + "</span>" +
        (off ? "<s>" + money(p.compareAt) + '</s><span class="off">Save ' + off + "%</span>" : "") + "</div>" +
      '<div class="pdp-tax">' + esc(L.taxNote) + "</div>" +
      '<p class="pdp-blurb">' + esc(p.blurb) + "</p>";

    if (p.variants && p.variants.options.length) {
      h += '<div class="opt-group"><div class="opt-lbl">' + esc(p.variants.label) + '</div><div class="opts" id="opts">' +
        p.variants.options.map(function (o, i) {
          return '<button class="opt' + (i === 0 ? " on" : "") + '">' + esc(o) + "</button>";
        }).join("") + "</div></div>";
    }

    h += '<div class="pdp-buy"><div class="qty-pick"><button id="qty-dec" aria-label="Fewer">−</button><span class="num" id="qty-val">1</span><button id="qty-inc" aria-label="More">+</button></div>' +
      '<button class="btn btn-solid" style="flex:1" id="pdp-add">' + esc(L.addToCart) + ' · <span class="num" id="pdp-total">' + money(p.price) + "</span></button></div>" +
      '<div class="pdp-stock"><span class="dot"></span>' +
        (p.stock <= 10 ? esc(L.lowStock).replace("{n}", p.stock) : esc(L.inStock)) + "</div>";

    if (L.assurances.length) {
      h += '<div class="pdp-assure">' + L.assurances.map(function (t) {
        return "<div>" + ICON.check + "<span>" + esc(t) + "</span></div>";
      }).join("") + "</div>";
    }

    h += '<div style="margin-top:40px"><div class="opt-lbl">' + esc(L.specTitle) + '</div><table class="spec-table">' +
      p.specs.map(function (s) { return "<tr><td>" + esc(s[0]) + "</td><td>" + esc(s[1]) + "</td></tr>"; }).join("") +
      "</table></div>";

    h += "</div></div></section>";

    /* related */
    var rel = S.products.filter(function (x) { return x.id !== p.id; }).slice(0, 4);
    h += '<section class="section wrap"><div class="sec-head"><div class="left">' +
      '<div class="sec-index">' + esc(L.relatedIndex) + '</div><h2 class="display" data-split>' + esc(L.relatedTitle) + "</h2></div>" +
      '<a class="link-u" href="collection.html" data-reveal>' + esc(L.relatedLink) + " " + ICON.arrow + "</a></div>" +
      '<div class="grid grid-4">' + rel.map(cardHTML).join("") + "</div></section>";

    root.innerHTML = h;

    /* gallery */
    $$(".pdp-thumbs button").forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".pdp-thumbs button").forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on");
        var img = $("#pdp-img");
        img.style.opacity = "0";
        setTimeout(function () { img.src = b.dataset.src; img.style.opacity = "1"; }, 180);
      });
    });
    var mainBox = $("#pdp-main");
    mainBox.addEventListener("click", function () { mainBox.classList.toggle("zoom"); });
    mainBox.addEventListener("mousemove", function (e) {
      if (!mainBox.classList.contains("zoom")) return;
      var r = mainBox.getBoundingClientRect();
      $("#pdp-img").style.transformOrigin =
        ((e.clientX - r.left) / r.width * 100) + "% " + ((e.clientY - r.top) / r.height * 100) + "%";
    });

    /* options */
    $$("#opts .opt").forEach(function (o) {
      o.addEventListener("click", function () {
        $$("#opts .opt").forEach(function (x) { x.classList.remove("on"); });
        o.classList.add("on");
      });
    });

    /* qty */
    var qty = 1;
    function syncQty() {
      $("#qty-val").textContent = qty;
      $("#pdp-total").textContent = money(p.price * qty);
    }
    $("#qty-inc").addEventListener("click", function () { qty = Math.min(qty + 1, Math.max(1, p.stock)); syncQty(); });
    $("#qty-dec").addEventListener("click", function () { qty = Math.max(1, qty - 1); syncQty(); });
    $("#pdp-add").addEventListener("click", function () {
      var v = $("#opts .opt.on");
      addToCart(p.id, qty, v ? v.textContent : "");
    });
  }

  /* ---------------------------------------------------------
     BAG (in-memory for the demo)
  --------------------------------------------------------- */
  var cart = [];
  function addToCart(id, qty, variant) {
    var p = byId(id); if (!p) return;
    var key = id + "|" + (variant || "");
    var found = cart.filter(function (c) { return c.key === key; })[0];
    if (found) found.qty += qty || 1;
    else cart.push({ key: key, id: id, qty: qty || 1, variant: variant || (p.variants ? p.variants.options[0] : "") });
    paintCart();
    toast(p.name + " added");
    openCart();
  }
  function paintCart() {
    var n = cart.reduce(function (a, c) { return a + c.qty; }, 0);
    var cc = $("#cart-count");
    cc.textContent = n;
    cc.classList.toggle("on", n > 0);
    var sub = cart.reduce(function (a, c) { return a + byId(c.id).price * c.qty; }, 0);
    $("#cart-sub").textContent = money(sub);
    $("#cart-total").textContent = money(sub);
    $("#drawer-body").innerHTML = cart.length ? cart.map(function (c, i) {
      var p = byId(c.id);
      return '<div class="ci"><img src="' + p.image + '" alt=""><div><div class="nm">' + esc(p.name) + "</div>" +
        '<div class="vr">' + esc(c.variant) + "</div>" +
        '<div class="qty"><button data-d="-1" data-i="' + i + '" aria-label="Fewer">−</button><span class="num">' + c.qty + '</span><button data-d="1" data-i="' + i + '" aria-label="More">+</button></div></div>' +
        '<div class="pr num">' + money(p.price * c.qty) + "</div></div>";
    }).join("") : '<div class="drawer-empty">' + esc(L.cartEmpty) +
      '<br><a class="link-u" href="collection.html" style="margin-top:14px">' + esc(L.cartEmptyLink) + "</a></div>";

    $$("#drawer-body .qty button").forEach(function (b) {
      b.addEventListener("click", function () {
        var i = +b.dataset.i, d = +b.dataset.d;
        cart[i].qty += d;
        if (cart[i].qty < 1) cart.splice(i, 1);
        paintCart();
      });
    });
  }
  function openCart() { $("#drawer").classList.add("on"); $("#drawer-bd").classList.add("on"); }
  function closeCart() { $("#drawer").classList.remove("on"); $("#drawer-bd").classList.remove("on"); }
  function bindAdd() {
    $$(".js-add").forEach(function (b) {
      if (b.dataset.bound) return;
      b.dataset.bound = "1";
      b.addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation();
        addToCart(b.dataset.id, 1);
      });
    });
  }
  var toastT;
  function toast(msg) {
    var t = $("#toast");
    t.textContent = msg;
    t.classList.add("on");
    clearTimeout(toastT);
    toastT = setTimeout(function () { t.classList.remove("on"); }, 2400);
  }

  /* ---------------------------------------------------------
     MOTION
  --------------------------------------------------------- */
  function splitLines(el) {
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w) {
      return '<span class="w" style="display:inline-block;overflow:hidden;vertical-align:top"><span style="display:inline-block;will-change:transform">' + esc(w) + "</span></span>";
    }).join(" ");
    return $$(".w > span", el);
  }

  function revealNow(els) {
    if (!window.gsap || REDUCED) { els.forEach(function (e) { e.style.opacity = 1; }); return; }
    window.gsap.fromTo(els, { opacity: 0, y: 26 }, {
      opacity: 1, y: 0, duration: 1, ease: "power3.out", stagger: 0.07, overwrite: true
    });
  }

  function initMotion() {
    var g = window.gsap;
    if (!g) { $$("[data-reveal]").forEach(function (e) { e.style.opacity = 1; }); return; }
    g.registerPlugin(window.ScrollTrigger);
    var ST = window.ScrollTrigger;

    if (REDUCED) {
      $$("[data-reveal]").forEach(function (e) { e.style.opacity = 1; });
      return;
    }

    var tl = g.timeline({ delay: 0.05 });
    if ($(".hero")) {
      tl.from(".hero .r-line > span", { yPercent: 118, duration: 1.25, ease: "expo.out", stagger: 0.09 }, 0)
        .from("[data-hero-el]", { opacity: 0, y: 22, duration: 1, ease: "power3.out", stagger: 0.1 }, 0.25)
        .from(".hero-bg img", { scale: 1.14, duration: 2.2, ease: "expo.out" }, 0);
    }
    tl.from(".hdr, .ticker, .concept-ribbon", { opacity: 0, duration: 1, ease: "power2.out" }, 0.15);

    $$("[data-split]").forEach(function (el) {
      var parts = splitLines(el);
      g.from(parts, {
        yPercent: 115, duration: 1.05, ease: "expo.out", stagger: 0.022,
        scrollTrigger: { trigger: el, start: "top 88%" }
      });
    });

    $$("[data-reveal]").forEach(function (el) {
      g.fromTo(el, { opacity: 0, y: 30 }, {
        opacity: 1, y: 0, duration: 1.05, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 92%" }
      });
    });

    $$("[data-parallax]").forEach(function (el) {
      var amt = parseFloat(el.dataset.parallax) || 0.1;
      var target = el.querySelector("img") || el;
      g.fromTo(target, { yPercent: -amt * 100 * 0.5 }, {
        yPercent: amt * 100 * 0.5, ease: "none",
        scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true }
      });
    });

    $$("[data-count]").forEach(function (el) {
      var end = parseFloat(el.dataset.count), suf = el.dataset.suffix || "";
      var o = { v: 0 };
      g.to(o, {
        v: end, duration: 1.8, ease: "power2.out",
        scrollTrigger: { trigger: el, start: "top 90%" },
        onUpdate: function () { el.textContent = Math.round(o.v) + suf; }
      });
    });

    var track = $("#story-track");
    if (track && window.innerWidth > 860) {
      var story = $(".story");
      var dist = function () { return track.scrollWidth - window.innerWidth + 80; };
      g.to(track, {
        x: function () { return -dist(); },
        ease: "none",
        scrollTrigger: {
          trigger: story, start: "top top", end: function () { return "+=" + dist(); },
          pin: true, scrub: 0.6, invalidateOnRefresh: true,
          onUpdate: function (self) {
            var bar = $("#story-prog");
            if (bar) bar.style.transform = "scaleX(" + self.progress + ")";
          }
        }
      });
    } else if (track) {
      track.parentElement.style.overflowX = "auto";
      track.parentElement.style.scrollSnapType = "x mandatory";
      $$(".story-panel", track).forEach(function (p) { p.style.scrollSnapAlign = "center"; });
    }

    ST.refresh();
    window.addEventListener("load", function () { ST.refresh(); });
  }

  function initSmooth() {
    if (REDUCED || !window.Lenis || !window.gsap || !window.ScrollTrigger) return;
    var lenis = new window.Lenis({ duration: 1.1, smoothWheel: true, wheelMultiplier: 0.9, touchMultiplier: 1.6 });
    lenis.on("scroll", window.ScrollTrigger.update);
    window.gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    window.gsap.ticker.lagSmoothing(0);
    window.__lenis = lenis;
  }

  function initHeader() {
    var hdr = $("#hdr"), bar = $("#topbar"), last = 0;

    function measure() {
      document.documentElement.style.setProperty("--topbar-h", bar.offsetHeight + "px");
      syncSticky();
    }
    /* Sticky elements sit under the topbar, but the topbar retracts on scroll
       down. --sticky-top follows it so nothing is left floating mid-screen. */
    function syncSticky() {
      var hidden = bar.classList.contains("hide");
      document.documentElement.style.setProperty("--sticky-top", hidden ? "0px" : bar.offsetHeight + "px");
    }
    measure();
    window.addEventListener("resize", measure);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

    function onScroll() {
      var y = window.scrollY || document.documentElement.scrollTop;
      hdr.classList.toggle("solid", y > 40);
      bar.classList.toggle("hide", y > 340 && y > last && !document.body.classList.contains("menu-open"));
      syncSticky();
      last = y;
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    $("#burger").addEventListener("click", function () {
      document.body.classList.toggle("menu-open");
      document.body.classList.toggle("is-locked", document.body.classList.contains("menu-open"));
      if (window.gsap && document.body.classList.contains("menu-open")) {
        window.gsap.fromTo(".mnav .m-link", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .8, ease: "expo.out", stagger: .06, delay: .18 });
      }
    });
    $$(".mnav a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-open", "is-locked");
      });
    });
  }

  function initFaq() {
    $$(".faq-i").forEach(function (item) {
      var q = $(".faq-q", item), a = $(".faq-a", item);
      q.addEventListener("click", function () {
        var open = item.classList.contains("open");
        $$(".faq-i.open").forEach(function (o) {
          o.classList.remove("open");
          $(".faq-a", o).style.height = "0px";
        });
        if (!open) {
          item.classList.add("open");
          a.style.height = a.scrollHeight + "px";
        }
      });
    });
  }

  function initMagnetic() {
    if (REDUCED || !window.gsap || window.matchMedia("(hover:none)").matches) return;
    $$(".btn").forEach(function (b) {
      b.addEventListener("mousemove", function (e) {
        var r = b.getBoundingClientRect();
        window.gsap.to(b, {
          x: (e.clientX - r.left - r.width / 2) * 0.18,
          y: (e.clientY - r.top - r.height / 2) * 0.28,
          duration: .5, ease: "power3.out"
        });
      });
      b.addEventListener("mouseleave", function () {
        window.gsap.to(b, { x: 0, y: 0, duration: .7, ease: "elastic.out(1,0.4)" });
      });
    });
  }

  function initTransitions() {
    var c = $("#curtain");
    if (!c || !window.gsap || REDUCED) return;
    document.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest("a") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (!href || href.charAt(0) === "#" || a.target === "_blank" || href.indexOf("http") === 0 || href.indexOf("mailto") === 0) return;
      e.preventDefault();
      window.gsap.timeline()
        .set(c, { transformOrigin: "50% 100%" })
        .to(c, { y: "0%", duration: .62, ease: "power4.inOut" })
        .add(function () { window.location.href = href; });
    });
    window.gsap.set(c, { y: "0%" });
    window.gsap.to(c, { y: "-100%", duration: .8, ease: "power4.inOut", delay: .05 });
  }

  function initPreloader(done) {
    var pl = $("#preloader");
    if (!pl) { done(); return; }
    if (REDUCED || !window.gsap) { pl.remove(); done(); return; }
    var o = { v: 0 };
    window.gsap.timeline()
      .to(o, {
        v: 100, duration: 1.0, ease: "power2.inOut",
        onUpdate: function () {
          $("#preloader .pl-pct").textContent = Math.round(o.v) + "%";
          $("#preloader .pl-bar i").style.transform = "scaleX(" + o.v / 100 + ")";
        }
      })
      .to("#preloader .pl-mark, #preloader .pl-bar, #preloader .pl-pct", { opacity: 0, duration: .35, ease: "power2.out" })
      .to(pl, {
        yPercent: -100, duration: .85, ease: "power4.inOut",
        onComplete: function () { pl.remove(); }
      }, "-=0.1")
      .add(done, "-=0.55");
  }

  /* ---------------------------------------------------------
     BOOT
  --------------------------------------------------------- */
  function boot() {
    injectTheme();
    document.title = document.title.replace("{{brand}}", S.brand.name);

    var page = document.body.dataset.page;
    document.body.insertAdjacentHTML("afterbegin",
      '<div id="preloader"><div class="pl-mark">' + esc(S.brand.wordmark) + "</div>" +
      '<div class="pl-bar"><i></i></div><div class="pl-pct num">0%</div></div>' + chromeTop());

    var main = $("#app");
    if (page === "home") renderHome(main);
    else if (page === "collection") renderCollection(main);
    else if (page === "product") renderProduct(main);

    main.insertAdjacentHTML("afterend", chromeBottom());

    initHeader();
    initFaq();
    bindAdd();
    paintCart();

    $("#cart-open").addEventListener("click", openCart);
    $("#cart-close").addEventListener("click", closeCart);
    $("#cart-close-2").addEventListener("click", closeCart);
    $("#drawer-bd").addEventListener("click", closeCart);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { closeCart(); document.body.classList.remove("menu-open", "is-locked"); }
    });

    /* anchor links should not be hijacked by the curtain */
    $$('a[href^="#"], a[href*="index.html#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href").split("#")[1];
        var t = id && document.getElementById(id);
        if (!t) return;
        e.preventDefault(); e.stopPropagation();
        document.body.classList.remove("menu-open", "is-locked");
        if (window.__lenis) window.__lenis.scrollTo(t, { offset: -80 });
        else t.scrollIntoView({ behavior: "smooth", block: "start" });
      }, true);
    });

    /* the corner watermark stands down where the footer already credits us */
    var mark = $(".built-mark"), credit = $(".ftr-credit");
    if (mark && credit && window.IntersectionObserver) {
      new IntersectionObserver(function (rows) {
        mark.classList.toggle("tuck", rows[0].isIntersecting);
      }, { rootMargin: "0px 0px -40px 0px" }).observe(credit);
    }

    initSmooth();
    initTransitions();
    initMagnetic();

    initPreloader(function () { initMotion(); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
