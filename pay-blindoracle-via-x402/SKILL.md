---
name: pay-blindoracle-via-x402
description: "Pay any BlindOracle SKU over the x402 HTTP payment protocol (EIP-3009 USDC on Base). Use when a buyer agent needs to autonomously purchase a BlindOracle service (research, crypto analysis, audits, deep research) — it handles the 402 challenge, signs a gasless USDC TransferWithAuthorization, resubmits with the X-PAYMENT header, and returns the deliverable + on-chain settlement proof. Keywords: x402, pay, buy, BlindOracle, USDC, Base, agent commerce, machine-to-machine payment."
allowed-tools: Bash, Read, WebFetch
---

# Pay BlindOracle via x402

A reusable **buyer skill**: lets any agent with a funded EVM wallet autonomously
purchase a BlindOracle SKU using Coinbase's [x402](https://x402.org) HTTP payment
protocol. Machine-to-machine, gasless (facilitator submits the tx), self-custodial.

## When to use

- A buyer agent wants a BlindOracle deliverable (deep research, crypto/market
  analysis, sentiment, agent audit, verified introduction) and is willing to pay
  per call in USDC.
- You have an EVM private key with USDC on **Base mainnet**.

## The endpoint & catalog

- **x402 payment endpoint:** `https://api.craigmbrown.com/v1/reputation/blindoracle`
- **Live SKUs** (per-call, USDC on Base) — full list in the ecosystem directory
  `https://craigmbrown.com/.well-known/agent-services.json` (`services[]`):

| SKU (`capability`) | Price | Output |
|---|---|---|
| `research.topic-deep-researcher` | $0.05 | multi-source research report + HTML |
| `research.topic-news-scanner` | $0.02 | recent-news scan |
| `research.topic-sentiment-analyzer` | $0.03 | sentiment sample |
| `crypto.market-analyzer` | $0.02 | real-time market read |
| … | … | see directory `services[]` |

## How it works (x402 flow)

1. **GET** the SKU endpoint with no payment → server replies **HTTP 402** with a
   challenge (`accepts[]`, `resource`, `extensions`).
2. **Sign** an EIP-3009 `TransferWithAuthorization` for the quoted USDC amount to
   the BlindOracle treasury (self-custodial signature; no funds move until settled).
3. **Resubmit** the request with the base64 signed authorization in the
   `X-PAYMENT` header.
4. The BlindOracle gateway forwards to the Coinbase CDP **facilitator** (verify +
   settle on Base, gasless for you), runs the SKU, and returns the **deliverable**
   plus a settlement record. A bad signature is simply rejected by the
   facilitator — **no fund risk**.

## Install

```bash
npx skills add pay-blindoracle-via-x402
pip install eth-account
```

## Invocation

```bash
# print the HTTP 402 challenge only — no key needed, nothing is sent
python3 pay.py --url https://api.craigmbrown.com/v1/reputation/blindoracle --dry-run

# sign + submit + settle on Base, return the deliverable + tx
BUYER_PRIVATE_KEY=0x... python3 pay.py \
  --url https://api.craigmbrown.com/v1/reputation/blindoracle
```

Wallet key is read from `BUYER_PRIVATE_KEY` only. **Never** hardcode a key; the
skill reads it from the environment only, and never writes it to disk or logs.

## What you get back

- The SKU deliverable (JSON / HTML per the SKU).
- A **trust envelope**: `content_sha256`, `content_scanned`, `powered_by: BlindOracle`.
- The on-chain settlement reference (Base USDC tx) — publicly verifiable.

## Safety notes

- **Self-custodial**: you sign; you never share the key. The facilitator settles.
- **Gasless**: the facilitator submits the tx; you pay only the USDC amount.
- **No fund risk on failure**: an invalid signature or a failed SKU = no settlement.
- x402 is mandatory for machine-to-machine BlindOracle calls. Human buyers should
  use the standard checkout link in the ecosystem directory instead.

## Related

- Ecosystem / SKU directory: `https://craigmbrown.com/.well-known/agent-services.json`
- Discover the catalog live: `https://api.craigmbrown.com/v1/services`
- x402 protocol docs: `https://x402.org`
