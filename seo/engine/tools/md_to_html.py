#!/usr/bin/env python3
"""Convert a run's article.md into Shopify article body HTML (+ FAQPage JSON-LD).

Handles the subset the drafting prompt produces: front matter, ## / ### headings, paragraphs,
- and 1. lists, pipe tables, **bold**, [links](url). The H1 is dropped (Shopify renders the title).
The '## FAQ' section's ### questions + following paragraphs become FAQPage JSON-LD.

Usage: python3 seo/engine/tools/md_to_html.py <run dir>   -> writes <run>/body.html, prints front matter as JSON
"""
import html
import json
import re
import sys
from pathlib import Path


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)

    def link(m):
        text, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{html.escape(url)}"{attrs}>{text}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)


def strip_md(t):
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t).replace("**", "")


def convert(md):
    fm = {}
    if md.startswith("---"):
        _, front, md = md.split("---", 2)
        for line in front.strip().splitlines():
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    lines = md.strip().splitlines()
    out, faq, i, in_faq, cur_q = [], [], 0, False, None
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            fm.setdefault("h1", line[2:].strip())
            i += 1
            continue
        if line.startswith("## "):
            text = line[3:].strip()
            in_faq = text.lower() in ("faq", "faqs", "frequently asked questions")
            out.append(f"<h2>{inline('Frequently asked questions' if in_faq else text)}</h2>")
            i += 1
            continue
        if line.startswith("### "):
            text = line[4:].strip()
            out.append(f"<h3>{inline(text)}</h3>")
            if in_faq:
                cur_q = {"q": strip_md(text), "a": ""}
                faq.append(cur_q)
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            head, body = rows[0], rows[1:]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table>")
            continue
        m = re.match(r"(\d+)\.\s|[-*]\s", line)
        if m:
            tag = "ol" if line[0].isdigit() else "ul"
            items = []
            while i < len(lines) and re.match(r"(\d+)\.\s|[-*]\s", lines[i]):
                items.append(re.sub(r"^(\d+\.|[-*])\s+", "", lines[i]).strip())
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"#|\||(\d+)\.\s|[-*]\s", lines[i]):
            para.append(lines[i].strip())
            i += 1
        text = " ".join(para)
        out.append(f"<p>{inline(text)}</p>")
        if in_faq and cur_q is not None:
            cur_q["a"] = (cur_q["a"] + " " + strip_md(text)).strip()
    if faq:
        ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": f["q"],
                              "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}
        out.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    return "\n".join(out) + "\n", fm


def main():
    run = Path(sys.argv[1])
    body, fm = convert((run / "article.md").read_text())
    (run / "body.html").write_text(body)
    print(json.dumps(fm, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
