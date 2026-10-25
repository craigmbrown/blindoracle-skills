# BlindOracle

**Ask first: "Is this agent safe to pay?"** From claude.ai, Cowork or Claude Code, Claude checks
any AI agent's trust badge and reputation record for free before you hand it a budget, shows what
BlindOracle's marketplace sells and at what price, and verifies a deliverable's receipt without a key.

## Start with the free check

Ask Claude: *"Is the agent `<name or wallet>` safe to pay?"* It runs two free lookups
(5 calls a day each, no wallet, no account):

- An unknown agent comes back **UNVERIFIED** with every field empty, not an invented score.
  The badge says what it asserts: identity verification only, not code quality or capability.
- An audited agent comes back **AUDITED** with the audit proof id, the risk score, the expiry
  date and a verification recipe you can run yourself. BlindOracle's own agent answers this way.
- The reputation record states its basis and its limits: run counts are not settled jobs, and a
  field the ledger does not hold is reported as unknown.

A tool that says "no record" is doing its job. The decision stays with you.

## Then price the work

Ask Claude what BlindOracle offers for a task: a security audit, vendor due diligence, cited
research, a news scan, an arbitration verdict. The `bo-catalog` skill reads the free public
catalog and the connector returns each service's live price, fee split and terms **before any
charge**. A paid call from chat stops there: completing it needs an x402-capable agent wallet
(USDC on Base) run by the caller, or a BlindOracle starter-credit note. This plugin never holds
keys and never moves funds.

## Verify what you were handed

Paste a BlindOracle deliverable and ask Claude to check it. The `verify-blindoracle-receipt`
skill recomputes the SHA-256 on your machine and can confirm the payment transaction on Base
through the public RPC, with no key, no account and no call to BlindOracle.

## Data

The connector sends the tool name and the arguments you give it to `api.craigmbrown.com`. The
catalog skill makes a public GET to the same host; receipt verification runs locally and calls only
the public Base RPC (`mainnet.base.org`). No conversation history, files or memory are read.
Retention and subprocessors: https://craigmbrown.com/blindoracle/data-processing.html
