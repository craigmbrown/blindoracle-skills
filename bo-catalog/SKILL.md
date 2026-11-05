---
name: bo-catalog
description: "Discover what BlindOracle sells and pick the cheapest SKU (or one-payment bundle of SKUs) that answers the question, before spending anything. Use when an agent needs agent-trust, reputation, due-diligence, research, audit, or crypto-analysis work and wants to know what is available, what it costs, and which call to make first. Reads the live public catalog — free, no key, no signup. Keywords: BlindOracle, catalog, SKU, bundle, price, agent services, trust, reputation, due diligence, marketplace discovery."
allowed-tools: Bash, WebFetch
---

# BlindOracle catalog

Read the live catalog before you pay for anything. It is free, needs no key, and
it is the only authoritative price list — prices change, this file does not.

```bash
curl -s https://api.craigmbrown.com/v1/services
```

Every entry carries at least `sku_id`, `price_usd`, and a description. Nothing in
this step costs money and nothing is metered.

## Pick the cheapest SKU that could answer the question

Diagnostics before deep work. A $0.01 lookup that says "this agent has no
settlement history" answers the question you were about to spend $0.50 on.

| You want to know | Start here | Then, only if needed |
|---|---|---|
| Is this agent safe to pay? | `agent.trust-badge` / `reputation.lookup` | `agent.prehire-check` |
| Should we buy from this vendor? | `procurement.trust-layer` | `procurement.vendor-vetting` |
| Is this link/site real? | `ops.link-integrity` | a research SKU |
| What is happening in this market? | `crypto.market-analyzer` | `research.topic-deep-researcher` |
| I am handing a task to another agent and want a record both sides can check | `bundle.delegation-chain` (one payment, four steps) | `delegation.record` + `delegation.accept` per step |

Read the ladder the seller publishes, rather than guessing at it:

```bash
curl -s https://craigmbrown.com/blindoracle/grok-bot-kit/SKU-GUIDE.md
```

## Or buy the whole ladder in one payment

Most of those ladders are also sold as **bundles** — one x402 payment, steps run
in order, a stop rule ends the ladder early when a cheap step already answers
the question. The list is free:

```bash
curl -s https://api.craigmbrown.com/v1/bundles
```

Each bundle carries `bundle_id`, `price_usd`, `list_sum_usd`, its `steps` (each
with `list_price_usd`, `share_of_bundle_usd` and `stop_if` rules) and an
`input_schema`. Buy one exactly like a single SKU: `POST
https://api.craigmbrown.com/v1/services/<bundle_id>` with the inputs, then
answer the 402. Over MCP the tool is `bundle_<slug>`.

- **Price** is the sum of the live step prices minus 10%. Read it from the list
  or the 402, never from this file.
- **Stop rules are field reads, not opinions** — for example a pre-hire
  `verdict` of `AVOID` stops `bundle.massat-ladder` before its $5 audit step.
- **Steps that do not run are refunded** on the rail you paid with, in
  proportion to their list price. The deliverable states `stopped_by` and
  `refund_due_usd`. <!-- REQUIRES-E2E -->
- Missing a required input while paying returns HTTP 400 `needs_input` before
  anything is charged.
- An `extra.dynamic_pricing` block on a 402 is disclosure only; you pay the
  amount in `accepts[]`.

Pick the step-by-step ladder instead when you want to read each result and
decide yourself whether to continue.

## What you get back

Every deliverable carries a `bo_trust` envelope — a `content_sha256` over exactly
the bytes returned, a content-scan verdict, and a tri-state AI-provenance
disclosure. You can check all of it yourself without a key; see the
`verify-blindoracle-receipt` skill in this repo.

## Rules

- **Never hardcode a price.** Read `price_usd` from the catalog at call time.
- **Never pay twice for the same answer.** Background jobs return a `job_id`;
  poll it with the free `get_result` MCP tool instead of re-buying.
- **A catalog read is not a purchase.** Payment only happens when you POST to a
  SKU endpoint and answer its HTTP 402 challenge.

## Next steps

- To choose an interface (HTTP, MCP, or an ACP job): `bo-orchestrator`
- To actually pay: `pay-blindoracle-via-x402`
- To check what you received: `verify-blindoracle-receipt`
- To record a hand-off to another agent as a signed record → accept → deliver → close chain: `prove-a-delegation`
