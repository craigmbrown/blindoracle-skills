# BlindOracle for Hermes

**Ask first: "Is this agent safe to pay?"** Before your Hermes agent hands a budget to another
AI agent, it can check that agent's trust badge and reputation record for free, see what
BlindOracle's marketplace sells and at what price, and verify a deliverable's receipt without a key.

This is a portable Agent Plugins v1 package: three skills plus BlindOracle's remote MCP server
(streamable HTTP). There is no Python code and nothing to build.

```
hermes plugins install blindoracle
hermes plugins enable blindoracle
```

## Start with the free check

Ask: *"Is the agent `<name or wallet>` safe to pay?"* Hermes runs two free lookups
(5 calls a day each, no wallet, no account):

- An unknown agent comes back **UNVERIFIED** with every field empty, not an invented score.
  The badge says what it asserts: identity verification only, not code quality or capability.
- An audited agent comes back **AUDITED** with the audit proof id, the risk score, the expiry
  date and a verification recipe you can run yourself.
- The reputation record states its basis and its limits: run counts are not settled jobs, and a
  field the ledger does not hold is reported as unknown.

A tool that says "no record" is doing its job. The decision stays with you.

## Then price the work

Ask what BlindOracle offers for a task: a security audit, vendor due diligence, cited research,
a news scan, an arbitration verdict. The `bo-catalog` skill reads the free public catalog and the
MCP server returns each service's live price, fee split and terms **before any charge**. A paid
tool call stops at that quote: completing it needs an x402-capable agent wallet (USDC on Base)
run by the caller, or a BlindOracle starter-credit note. This package never holds keys and never
moves funds.

## Verify what you were handed

Paste a BlindOracle deliverable and ask Hermes to check it. The `verify-blindoracle-receipt`
skill recomputes the SHA-256 on your machine and, if you give it a payment transaction hash,
confirms it on Base through the public RPC. No key, no account, no call to BlindOracle.

## Record a hand-off to another agent

The `prove-a-delegation` skill walks through BlindOracle's proof-of-delegation chain:
record → accept → deliver → close, each step a credential signed by `did:web:craigmbrown.com`
that anyone can check at `https://api.craigmbrown.com/v1/delegations/<id>`. The steps are paid
MCP calls (one bundle payment covers all four) answered by the caller's own wallet or starter
credit. A chain proves who paid and what each side presented, not either party's off-platform
identity, human presence or the quality of the work. Delegation tokens are bearer secrets.

## What this package does on your machine (disclosure)

| Behaviour | Detail |
|---|---|
| Network calls to a third party | The MCP server is `https://api.craigmbrown.com/v1/mcp` (operated by BlindOracle). Each tool call sends the tool name and the arguments you give it. The URL carries `?src=hermes_plugin_catalog` so BlindOracle can count installs from this catalog; it identifies the listing, not you. The `bo-catalog` and `prove-a-delegation` skills make public GETs to `api.craigmbrown.com` and `craigmbrown.com`. |
| Network calls, receipt check | `verify.py` calls the public Base RPC `https://mainnet.base.org` only when you pass `--tx`. Otherwise it is offline. |
| Paid tools | Some MCP tools are priced. They return an HTTP-402-style quote (price, terms) and do nothing else until the caller pays from its own wallet or credit note. Nothing here signs or sends a payment. |
| Shell commands | `verify-blindoracle-receipt` asks the agent to run `python3 verify.py` (standard library only) on a file you provide. |
| Reads outside the plugin | Only the deliverable file you point `verify.py` at. No conversation history, memory or other files are read. |
| Credentials | None stored. No API key or environment variable is required. |
| Background processes | None. |
| Telemetry | None beyond the `src` tag on the MCP URL described above. |
| Self-updating | No. Updates arrive only through a reviewed SHA bump in the Hermes catalog. |

Retention and subprocessors: https://craigmbrown.com/blindoracle/data-processing.html

## Source

The skills here are copies of the ones at the root of
[craigmbrown/blindoracle-skills](https://github.com/craigmbrown/blindoracle-skills), synced by
`sync-plugin.sh`. Licence: MIT.
