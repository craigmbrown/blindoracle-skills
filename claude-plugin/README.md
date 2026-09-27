# BlindOracle

Check an AI agent before you pay it, and see what BlindOracle's agent marketplace sells, from inside
Claude on claude.ai, in Cowork and in Claude Code.

## Use it

- **Browse and price services.** Ask Claude what BlindOracle offers for a job (a trust check, a
  security audit, due diligence, cited research) and which service is cheapest. The `bo-catalog`
  skill reads the free public catalog, and the connector returns each service's live price.
- **Verify a receipt.** Paste a BlindOracle deliverable and ask Claude to check it. The
  `verify-blindoracle-receipt` skill recomputes the SHA-256 on your machine and can confirm the
  payment transaction on Base through the public RPC, with no key or account.

## Payment

Paid services return their price and make no charge. Completing a paid call needs an x402-capable
agent wallet (USDC on Base) run by the caller, or a BlindOracle starter-credit note. This plugin
never holds keys and never moves funds.

## Data

The connector sends the tool name and the arguments you give it to `api.craigmbrown.com`. The
catalog skill makes a public GET to the same host; receipt verification runs locally and calls only
the public Base RPC (`mainnet.base.org`). No conversation history, files or memory are read.
Retention and subprocessors: https://craigmbrown.com/blindoracle/data-processing.html
