---
name: verify-blindoracle-receipt
description: Verify a BlindOracle deliverable yourself, with no API key and no account — recompute the SHA-256 over the bytes you received and compare it to the trust envelope, read the AI-provenance disclosure honestly, and confirm the payment transaction on Base through the public RPC. Use after buying any BlindOracle SKU, or when an agent is handed a BlindOracle deliverable by a third party and wants to check it was not altered. Keywords: verify, receipt, integrity, sha256, tamper, provenance, AI disclosure, settlement, Base, x402, trust envelope, key-free.
allowed-tools: Bash, Read
---

# Verify a BlindOracle receipt

Every BlindOracle deliverable carries a `bo_trust` envelope. You do not have to
trust it — you can recompute it. Nothing here needs a credential, and none of it
calls a BlindOracle endpoint, so a third party holding the deliverable can run
the same check and reach the same answer.

```bash
python3 verify.py --deliverable result.json
python3 verify.py --deliverable result.json --tx 0x<payment-tx-hash>
python3 verify.py --deliverable result.json --json
```

Exit code 0 means every requested check passed; 1 means one failed.

## What is checked

| Check | How | What a failure means |
|---|---|---|
| **Integrity** | SHA-256 over the delivered content vs `bo_trust.content_sha256` | the bytes you hold are not the bytes that were stamped — someone edited the deliverable after delivery |
| **Provenance** | reads `ai_generated` / `ai_model` / `scan_verdict` | reported, never inferred (see below) |
| **Settlement** | `eth_getTransactionReceipt` against `https://mainnet.base.org` | the payment you were shown did not confirm on Base |

The Base check uses the public RPC endpoint: no key, no plan, no account.

## Provenance is tri-state — read it literally

`ai_generated` has three states and they are not interchangeable:

- `true` → a model produced this content; the model name should accompany it.
- `false` → retrieved or computed deterministically.
- **absent** → **not recorded.** This is *not* a claim that no model was involved.
  Treat it as possibly model-generated.

The verifier prints "not recorded" for the absent case on purpose. Do not report
it to a human as "no AI involved".

## If the content field is somewhere else

The hash covers the SKU's returned content string. The verifier looks for
`output`, `content`, `text`, `result`, `deliverable`, then `body`, including one
level of nesting. If your SKU nests it differently, say so explicitly:

```bash
python3 verify.py --deliverable result.json --content-field my_field
python3 verify.py --content-file body.md --expect-sha256 <hex>
```

A mismatch caused by hashing the wrong field is a *reading* error, not a tamper
finding. Confirm you hashed the right bytes before accusing anyone.

## Limits — what this does NOT prove

- It does not prove the content is **correct**, only that it is **unaltered**.
  A digest establishes consistency with the stamp, not truth of the claim.
- It does not verify the internal proof rail (HMAC-signed proof records, Merkle
  roots). Those are checked seller-side; this skill deliberately covers only what
  a stranger can check alone.
- A confirmed transaction proves *a* payment settled, not that it was yours.
  Match the amount and recipient yourself if that matters.

## Related

- `bo-catalog` — what is for sale, and the cheapest call that answers the question
- `bo-orchestrator` — HTTP vs MCP vs ACP
- `pay-blindoracle-via-x402` — making the purchase
