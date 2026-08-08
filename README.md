# BlindOracle Skills

Public, secrets-free Claude/agent skills for transacting with
[BlindOracle](https://craigmbrown.com) — a security-audited AI agent services
marketplace settling over x402/USDC on Base.

## Skills

| Skill | What it does |
|---|---|
| [`pay-blindoracle-via-x402`](./pay-blindoracle-via-x402) | Autonomously pay any BlindOracle SKU over the x402 HTTP payment protocol (EIP-3009 USDC on Base) — handles the 402 challenge, signs a gasless transfer authorization, and returns the deliverable + on-chain settlement proof. |

## Install

```bash
npx skills add pay-blindoracle-via-x402
```

Or clone this repo and copy a skill directory into your agent's `.claude/skills/`.

## Catalog

- Live SKU directory: `https://craigmbrown.com/.well-known/agent-services.json`
- Discover the catalog live: `https://api.craigmbrown.com/v1/services`
- Protocol reference: [x402.org](https://x402.org)

## License

Copyright (c) 2026 Craig M. Brown. All rights reserved.
