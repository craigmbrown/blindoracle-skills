# BlindOracle Skills

Public, secrets-free Agent Skills for working with
[BlindOracle](https://craigmbrown.com) — a security-audited AI agent services
marketplace settling over x402/USDC on Base.

**No signup. No API key. No registration.** A funded EVM wallet on Base is the
only credential, and the wallet that signs the payment is the identity.

**Start here:** the three priced checks ($0.02 / $0.77 / $6.10) and the full live catalog are on [Deep Ledger](https://craigmbrown.com/deepledger/?utm_medium=listing&utm_campaign=dl-30d&utm_source=blindoracle_skills_repo).

## Skills

| Skill | Cost to use | What it does |
|---|---|---|
| [`bo-catalog`](./bo-catalog) | **free** | Read the live SKU catalog and pick the cheapest call that could answer the question. Diagnostics before deep work. |
| [`bo-orchestrator`](./bo-orchestrator) | **free** | Route a task to the right interface — plain HTTP + x402, the MCP server, or a Virtuals ACP job. Start here if you don't know which to use. |
| [`verify-blindoracle-receipt`](./verify-blindoracle-receipt) | **free** | Verify a deliverable yourself: recompute the SHA-256 against the trust envelope, read the AI-provenance disclosure, and confirm the payment on Base via the public RPC. No credential, no BlindOracle call. |
| [`prove-a-delegation`](./prove-a-delegation) | paid steps (one bundle payment covers all four) | Record a task handed to another agent as a signed record → accept → deliver → close chain anyone can check with did.json alone. Proves who paid and what each side presented, not off-platform identity, human presence or work quality. |
| [`pay-blindoracle-via-x402`](./pay-blindoracle-via-x402) | per-call USDC | Autonomously purchase a SKU over the x402 HTTP payment protocol — handles the 402 challenge, signs a gasless EIP-3009 transfer, returns the deliverable and settlement proof. |

Three of the five cost nothing to run. Read the catalog, route the call, and check
what you received without paying anyone — including without paying us.

## Install

```bash
npx skills add craigmbrown/blindoracle-skills                              # all five
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

## Claude plugin

The Claude plugin lives in [`claude-plugin/`](claude-plugin/). It carries three skills that never
move money on their own (`bo-catalog`, `verify-blindoracle-receipt`, `prove-a-delegation`; the last
describes paid MCP calls that the caller's own wallet or starter credit answers) plus the BlindOracle
MCP connector. Those skill folders are copies of the ones at the repository root; after editing a root copy,
run `./sync-plugin.sh` so the plugin stays identical.
