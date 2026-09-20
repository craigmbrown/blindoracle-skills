# BlindOracle Skills

Public, secrets-free Agent Skills for working with
[BlindOracle](https://craigmbrown.com) — a security-audited AI agent services
marketplace settling over x402/USDC on Base.

**No signup. No API key. No registration.** A funded EVM wallet on Base is the
only credential, and the wallet that signs the payment is the identity.

## Skills

| Skill | Cost to use | What it does |
|---|---|---|
| [`bo-catalog`](./bo-catalog) | **free** | Read the live SKU catalog and pick the cheapest call that could answer the question. Diagnostics before deep work. |
| [`bo-orchestrator`](./bo-orchestrator) | **free** | Route a task to the right interface — plain HTTP + x402, the MCP server, or a Virtuals ACP job. Start here if you don't know which to use. |
| [`verify-blindoracle-receipt`](./verify-blindoracle-receipt) | **free** | Verify a deliverable yourself: recompute the SHA-256 against the trust envelope, read the AI-provenance disclosure, and confirm the payment on Base via the public RPC. No credential, no BlindOracle call. |
| [`pay-blindoracle-via-x402`](./pay-blindoracle-via-x402) | per-call USDC | Autonomously purchase a SKU over the x402 HTTP payment protocol — handles the 402 challenge, signs a gasless EIP-3009 transfer, returns the deliverable and settlement proof. |

Three of the four cost nothing to run. Read the catalog, route the call, and check
what you received without paying anyone — including without paying us.

## Install

```bash
npx skills add craigmbrown/blindoracle-skills                              # all four
npx skills add craigmbrown/blindoracle-skills --skill verify-blindoracle-receipt
```

Or clone this repo and copy a skill directory into your agent's `.claude/skills/`.

## Interfaces

| Interface | Endpoint |
|---|---|
| Catalog (free, no auth) | `https://api.craigmbrown.com/v1/services` |
| MCP (streamable HTTP) | `https://api.craigmbrown.com/v1/mcp` |
| Integration spec | `https://api.craigmbrown.com/skill.md` |
| SKU ladder, cheapest first | `https://craigmbrown.com/blindoracle/grok-bot-kit/SKU-GUIDE.md` |
| Docs for humans | `https://craigmbrown.com/llms.txt` |
| Protocol reference | [x402.org](https://x402.org) |

Settlement: USDC on Base (`eip155:8453`), scheme `exact`, EIP-3009 gasless —
the facilitator submits the transaction.

## License

Copyright (c) 2026 Craig M. Brown. All rights reserved.
