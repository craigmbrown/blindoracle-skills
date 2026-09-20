---
name: bo-orchestrator
description: Route a BlindOracle task to the right interface — plain HTTP with x402, the MCP server, or a Virtuals ACP job — and run it end to end. Use this first when an agent wants something from BlindOracle but does not know whether to call HTTP, connect an MCP server, or post an on-chain job. Keywords: BlindOracle, orchestrator, routing, x402, MCP, ACP, agent commerce, which interface, how do I call.
allowed-tools: Bash, WebFetch, Read
---

# BlindOracle orchestrator

One catalog, three ways in. Pick by what the caller already has, not by novelty.

| If the caller… | Use | Why |
|---|---|---|
| is a script, or any HTTP client with a funded Base wallet | **HTTP + x402** | fewest moving parts; the payment *is* the auth |
| is an MCP-capable agent (Claude Code, Codex, an MCP host) | **MCP** | SKUs arrive as typed tools with schemas; no bespoke client |
| already trades on Virtuals ACP | **ACP job** | settlement and escrow are handled by the protocol |
| is a human deciding whether to buy | **the docs** | `https://craigmbrown.com/llms.txt` |

Read the catalog first either way — see the `bo-catalog` skill. No key, no signup:
a funded EVM wallet on Base is the only credential, and the wallet that signs the
payment is the identity.

## Route A — HTTP + x402

```bash
curl -s https://api.craigmbrown.com/v1/services                  # catalog, free
curl -si -X POST https://api.craigmbrown.com/v1/services/<sku_id> # -> HTTP 402
```

The 402 carries a base64 x402 challenge in the `payment-required` header. Sign an
EIP-3009 `TransferWithAuthorization` for USDC on Base (`eip155:8453`, scheme
`exact`) and retry with the `PAYMENT-SIGNATURE` header. The facilitator settles
gaslessly. The standard `@x402/fetch` client does all of this for you — and the
`pay-blindoracle-via-x402` skill in this repo walks it step by step.

## Route B — MCP

Streamable HTTP, JSON-RPC over POST:

```
https://api.craigmbrown.com/v1/mcp
```

```bash
claude mcp add --transport http blindoracle https://api.craigmbrown.com/v1/mcp
```

Each paid SKU appears as a tool whose name is the `sku_id` with `.` replaced by
`_` (`agent.prehire-check` → `agent_prehire-check`). Calling one without payment
returns a tool result carrying the same 402 challenge; pay by putting the x402
payload in the call's `_meta`. `get_result` polls a background job by `job_id`
and is **free**. Read the server's `skill.md` resource before your first call.

## Route C — Virtuals ACP

The same services are sold by the ACP provider agent **BlindOracle Research &
Trust** (`0xfb67673a0316626c8310348015eed036be728ca6`). Post a job through ACP
and settlement follows the protocol rather than a raw 402.

## After the call

1. Check what you got — `verify-blindoracle-receipt` (key-free).
2. A background SKU returns a `job_id`, not a deliverable. Poll it; do not re-buy.
3. Read the AI-provenance field honestly: absent means *not recorded*, which is
   not the same as *not AI-generated*.

## Do not

- Do not pay before reading the catalog price — never hardcode a price.
- Do not send a private key anywhere. You sign locally; BlindOracle never holds keys.
- Do not treat a 402 as an error. It is the price quote.
