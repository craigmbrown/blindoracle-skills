# BlindOracle Skills

Skills your coding agent can use to check an AI agent, a vendor or a delivered
result before you rely on it. Hand this page to your agent and say what you want.

**No signup. No API key. No registration.** Reading prices and verifying a result
are free. Paid checks settle per call in USDC on Base, and the wallet that signs
the payment is the identity.

## What you can ask for

Say it in normal language. Your agent reads the live price list first and tells
you the cost before anything is paid.

| You say | What your agent does | Price on 2026-11-10 |
|---|---|---|
| "Is this agent safe to pay?" | Looks up the agent's track record and trust badge. | $0.01 each, or $0.018 together (`bundle.reputation-badge`) |
| "Should I hire this agent?" | Track record, then a pre-hire check. A $5 security audit runs only if you mark the job high-stakes, and never after an "avoid" verdict. | about $4.73 in one payment (`bundle.prehire-ladder`); steps that do not run are refunded |
| "Is this vendor real?" | Looks the company up in a public registry, pulls its trust record, then runs a $1 due-diligence scan. Stops if the registry does not name the company. | about $1.00 (`bundle.due-diligence`); steps that do not run are refunded |
| "We disagree about a delivery." | Pulls the other side's record as evidence, runs the dispute settlement, and seals the verdict. The verdict comes from BlindOracle's own operator panel, not a neutral third party. | about $4.56 (`bundle.dispute-evidence`) |
| "I'm handing this task to another agent. Keep a record." | Records the handoff as a signed chain: record, accept, deliver, close. Anyone can check it. | about $0.16 for all four steps (`bundle.delegation-chain`) |
| "Was this report altered after it was made?" | Recomputes the hash of what you received and confirms the payment on Base. No BlindOracle call. | free |

Prices change. The [live catalog](https://api.craigmbrown.com/v1/services) is the
only authoritative price list, and it is free to read.

### Paste this into your agent

```text
Install the BlindOracle skills: npx skills add craigmbrown/blindoracle-skills
Read the live price list. Then tell me the cheapest way to check whether
<agent name or wallet> is safe to pay, and what it will cost.
Do not pay for anything until I say yes.
```

Swap the middle sentence for any row in the table above.

## The five skills

| What it is for | Skill | Cost to use |
|---|---|---|
| Find the cheapest check that answers your question, before spending anything | [`bo-catalog`](./bo-catalog) | **free** |
| Get a check running from whatever your agent already has: plain HTTP, an MCP host, or a Virtuals ACP account | [`bo-orchestrator`](./bo-orchestrator) | **free** |
| Check that a result you were handed was not altered: recompute its SHA-256, read the AI-provenance disclosure, confirm the payment on Base. No credential, no BlindOracle call | [`verify-blindoracle-receipt`](./verify-blindoracle-receipt) | **free** |
| Keep a record both sides can check when one agent hands a task to another. It proves who paid and what each side presented, not off-platform identity, human presence or work quality | [`prove-a-delegation`](./prove-a-delegation) | paid steps (one bundle payment covers all four) |
| Let your agent pay for one check on its own over x402: it answers the 402 challenge, signs a gasless USDC transfer, and returns the result with its settlement proof | [`pay-blindoracle-via-x402`](./pay-blindoracle-via-x402) | per-call USDC |

Three of the five cost nothing to run. Read the catalog, route the call, and check
what you received without paying anyone, including without paying us.

The three priced starter checks ($0.02 / $0.77 / $6.10) are on [Deep Ledger](https://craigmbrown.com/deepledger/?utm_medium=listing&utm_campaign=dl-30d&utm_source=blindoracle_skills_repo).

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
