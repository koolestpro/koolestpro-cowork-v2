# Design tool integration: Lovable, Claude Design, and the rest (2026-09-13)

> **2026-09-18 update:** approved by Ridwan. CRO Fix rebuilds and redesigns (not templates) are built here and the rulebook now allows it (`CLAUDE.md` → AI Workflow Architecture). **Rebuilds stay private:** no public `deploy_project` / share link for a real brand's page; capture from the private preview. Lovable, v0 and Figma are connected as MCPs in Cowork sessions, so Claude can drive the whole chain.

Operator assumption: **Claude Code (or Codex) runs the operation.** Everything here is meant to be
drivable from that agent, not clicked by hand. Prices checked 2026-09-13; they change, so re-check
before committing.

## The headline: yes, Lovable connects to Claude, officially

Lovable runs a **Model Context Protocol (MCP) server** at `https://mcp.lovable.dev`. It is the
reverse of Lovable's "chat connectors": it lets an external agent (Claude, Claude Code, ChatGPT,
Cursor, VS Code) drive Lovable programmatically. OAuth only, no API key, available on **all plans**.

### Claude Code setup (one line)

```bash
claude mcp add --transport http lovable "https://mcp.lovable.dev"
# or, with slash commands for common tasks:
/plugin install lovable@claude-plugins-official
```

### Claude Desktop / claude.ai setup

`+` -> **Connectors** -> **Browse Connectors** -> search **Lovable** -> Connect, then sign in.

### What the agent can then do

| Tool | What it does |
|---|---|
| `create_project` | Start a project with an `initial_message` (the build prompt) |
| `send_message` | Iterate on a project (supports plan mode, file attachments) |
| `deploy_project` | Publish and return the live URL |
| `get_project` | Project details incl. preview URL and a screenshot |
| `list_design_systems` | Design systems available in the workspace |
| `set_workspace_knowledge` / `set_project_knowledge` | Push our rules into Lovable as persistent instructions |
| `create_workspace_skill` | Package our playbook as a Lovable skill |
| `get_diff` / `read_file` / `list_files` | Inspect the generated code |
| `import-claude-design-from-url` | **Claude clients only.** Import a Claude Design into a new Lovable project |

`create_project` and `send_message` consume Lovable credits. The rest are free.

## Claude Design, and why it matters here

**Claude Design** is an Anthropic beta product (`claude.ai/design`), included in **Claude Pro, Max,
Team, and Enterprise**. It creates on-brand visual work (designs, prototypes, decks), and its
"connectors" include **Lovable**, Replit, Vercel, Wix, Canva, Adobe, Gamma, Miro.

Two facts make it the missing link for this project:

1. It **imports a design system** from a GitHub repo, design files, or the local codebase, and
   checks its output against it. So a build can come out looking like the brand, not a template.
2. It **hands off directly to Lovable** (and Replit/Vercel/Wix), which turns the design into
   production code.

It also syncs with Claude Code via `/design-sync` (pull the design system in) and `/design` (work
inside Claude Code). Usage shares the same pool as chat, Claude Cowork, and Claude Code.

## The end-to-end automated chain (Claude Code as operator)

```
0. (optional) Claude Design: /design with the brand design system -> on-brand design
   -> Lovable MCP import-claude-design-from-url -> new Lovable project
1. Brief:      build_page_brief.py            -> <slug>_build-brief.md      [this repo]
2. Build:      Lovable MCP create_project(initial_message = brief)
               -> send_message to iterate -> set_project_visibility(private)
               -> capture from the authenticated preview (NO public deploy for real brands)
3. Capture:    capture_page.py --url <live URL> -> mobile / full / desktop PNGs  [this repo]
4. Compose:    build_device_still.py / carousel / recap -> post graphics   [this repo]
5. Publish:    caption per x-caption-playbook -> content system (#cowork-sync-data)
```

One-time, push our standards into Lovable so every build starts from them:
`set_workspace_knowledge(...)` with the redesign standard, `create_workspace_skill(...)` with the
page-build playbook.

That is genuinely "in one go": a brief in, a published page and post assets out, no manual step.

## Price comparison

### Page builders

| Tool | Entry price | Free tier | API / MCP | Strengths | Weaknesses |
|---|---|---|---|---|---|
| **Lovable** | **$25/mo** Pro (100 credits); $250/yr annual ($21/mo). Business from $50/mo | Free (5 build credits/day, 30/mo) | **Official MCP** (all plans) + Build-with-URL | Best finished-page quality of the group; official Claude MCP; Claude Design import; Git sync; deploy + hosting | Credits burn on iteration; no repo import; generation API is MCP only |
| **Figma Make** | **$16/mo** Professional (full seat, 3,000 AI credits/mo) | Free (150 AI credits/day, 500/mo) | Figma MCP (200 tool calls/day on Pro) | Best if you already live in Figma; design-system styling; publish a URL; mobile | Make is bundled in the seat, credits shared across Figma AI; not an agent-first API |
| **v0** (Vercel) | Paid usage (Vercel/v0 credits) | Limited | **Official REST API v2** + MCP + SDK (`npm install v0`) | The most API-first option; clean SDK; deploy to Vercel | Cost scales with use; another account to manage |
| **Bolt.new** | **$25/mo** Pro (10M tokens) | Free (300K tokens/day, 1M/mo, Bolt branding) | No public generation API | Good quality, full-stack, hosting + databases included | No official API/MCP for automation; branding on free |
| **bolt.diy** | **$0** + model tokens | Self-hosted | Local/Docker, BYO LLM (OpenRouter, Ollama) | Cheapest possible; any model; fully local | WebContainers need a commercial license for for-profit production; you maintain it |
| **Onlook** | **$0** self-hosted | Open source | Self-host | Visual React/Tailwind editing; "Cursor for designers" | Not a generator; editing layer, not a builder |
| **Replit** | Paid usage | Limited | MCP + Claude Design connector | Also in the Claude Design connector list; full-stack + hosting | Own pricing model |

### Agent / model layer (the operator)

| Tool | Price | Notes |
|---|---|---|
| **Claude Pro** | **$17/mo** annual, $20 monthly | Includes Claude Code, Claude Cowork, **Claude Design**, Claude Science. One usage pool. |
| Claude Max | from $100/mo | 5x or 20x Pro usage |
| Claude Team | $20/seat annual ($25 monthly); Premium seat $100/seat | SSO, central billing |
| Claude API (self-hosting) | Sonnet 5 $2/$10 per MTok; Opus 5 $5/$25; Haiku 4.5 $1/$5 | Only if you drive a self-hosted builder |

## What this means for cost

For a few page builds a week, **Lovable Pro ($25/mo, 100 credits)** is enough: a landing page with
generated images costs about 1.7 credits, and a full page plus a few iterations lands in the low
single digits per build. Add **Claude Pro ($20/mo)** if not already subscribed, and the whole chain
(MCP drive + Claude Design + Claude Code) is covered. Realistic all-in: **about $45/mo**, plus
Figma's $16/mo only if you want Figma Make too.

The genuinely free path (bolt.diy + Ollama) exists, but you trade away the finished-page quality and
take on maintenance plus the WebContainers licensing question. Given that build quality is the
priority, it is not the right default.

## Is there anything better than Lovable and Figma Make?

For **this** goal (on-brand page design, production output, driven by an agent) the strongest fit is
**Claude Design + Lovable**, for one reason: Claude Design imports a real design system and outputs
on-brand design, and Lovable is the only one of the pair with an official MCP plus a Claude-only
import path. Replit is the closest alternative (also a Claude Design connector, also MCP-capable).
v0 is better if you want a pure API rather than an MCP. Figma Make stays the better choice when the
work is design-led and you are already in Figma.

Nothing free beats Lovable or Figma Make on finished page quality today.

## Three common questions

### Can Claude Design replace Lovable entirely?

**Partly.** For this project's actual deliverable, a designed mobile page captured as a screenshot,
Claude Design can plausibly carry it: it builds on-brand pages, imports a design system from a repo
or codebase, and **exports HTML**. Our rebuilds are already standalone HTML, so that output fits the
pipeline. What it does **not** replace is Lovable as an app platform: React/Next structure, routing,
a backend, Shopify/checkout, hosting, and one-click deploy are not its job. It is also a **beta**,
and its usage shares one pool with Claude Code, Cowork, and chat. Verdict: worth a head-to-head test
on Caraway, but do not assume it matches the GetFit bar.

### Is v0 more accurate, on pay-as-you-go?

Accuracy comes from the **model and the brief**, not the platform, so "more accurate" is not
guaranteed. v0's real edge is control: an official REST API and SDK (`npm install v0`) let you send
the exact brief, design tokens, and constraints programmatically, which makes output more consistent
than re-typing prompts by hand. PAYG also suits one build a week. I could not confirm v0's current
rates from its pricing page (it did not render), so check v0 settings before committing. Verdict: a
strong API-first alternative. Settle it with a bake-off, not with assumptions.

### Does Lovable Free cover one build a week?

**Not reliably.** Free gives 5 build credits/day capped at **30 build credits per month**, and the
cap is front-loaded: you get the grant for roughly the first 6 days of the month, then nothing until
the 1st. A landing page with generated images is about 1.7 credits, and a real build plus iteration
is several messages, so 30 credits spread across four builds is tight. Free also has **no custom
domain, keeps the "Edit with Lovable" badge, no code download, and no design systems**, all of which
matter for professional output. The MCP server does work on Free. Verdict: fine for testing the
connection, not for shipping.

### What I would actually do

1. **Test on Free first:** connect the Lovable MCP, run the Caraway brief, confirm the chain works
   end to end.
2. **Upgrade to Lovable Pro** (annual, about $21/mo) for shipping. 100 credits covers several builds
   a month with headroom, and it removes the badge and unlocks design systems and code download.
3. **Before paying anything,** run the same Caraway brief through Claude Design (already in a Claude
   plan) and v0 PAYG. Whichever lands closest to the GetFit bar wins. That is a one-afternoon test
   that answers the whole question with evidence.

## Recommendation

1. **Primary:** Lovable Pro + Claude Pro, wired through the Lovable MCP. Push the redesign standard
   into Lovable once via `set_workspace_knowledge` and the playbook via `create_workspace_skill`.
2. **Design front-end (optional):** Claude Design, when the page needs an on-brand design pass
   before Lovable builds it.
3. **Alternative:** Figma Make if the work is design-led, v0 if you want a pure API.
4. **Free fallback:** bolt.diy + Ollama for experiments only.
