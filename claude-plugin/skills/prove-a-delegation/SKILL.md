---
name: prove-a-delegation
description: Record a task handed from one AI agent to another as a four-step BlindOracle proof-of-delegation chain (record, accept, deliver, close) that anyone can check, and explain what the chain does and does not prove.
allowed-tools: Bash(curl -s https://api.craigmbrown.com/v1/delegations/*), WebFetch(domain:api.craigmbrown.com), WebFetch(domain:craigmbrown.com)
---

Use this skill when the user hands a task to another agent (or pays an outside API for one) and wants a record, which both sides and any third party can check, of who asked for what, who took it on, what was handed back, and whether the delivery matched.

## What the chain is

Four signed credentials, one per step: record → accept → deliver → close. Each credential is signed by `did:web:craigmbrown.com` and carries the hash of the step before it. Anyone can check the chain with only https://craigmbrown.com/.well-known/did.json.

It proves who paid and what each side presented. It does **not** prove either party's off-platform identity, that a human was present, or that the work is good. Say this to the user before they rely on a chain.

## Where it runs

The chain tools are paid. They run on the BlindOracle MCP endpoint `https://api.craigmbrown.com/v1/mcp` (the same server the BlindOracle plugin connects to; listing its tools needs no payment), or over plain HTTP at `POST https://api.craigmbrown.com/v1/services/<sku_id>` (`delegation.record`, `delegation.accept`, `bundle.delegation-chain`, `attestation.single-use-seal`, `trust.receipt-verify`). Read `price_usd` from `https://api.craigmbrown.com/v1/services` or the 402 challenge at call time; never quote a price from memory. The bundle is one payment for all four steps and costs less than buying them one by one. Calling a paid tool returns a payment-required result; this skill never moves funds on its own.

The caller pays with its own funds, in one of two ways:

- **x402**: answer the 402 payment request with a signed USDC payment on Base, from the caller's own wallet.
- **Starter credit**: register an agent (`POST https://api.craigmbrown.com/v1/agents/register` with `{"name": "<agent-name>", "capabilities": ["delegation"], "terms_accepted": true}`; keep the `api_key`, shown once), then `POST https://api.craigmbrown.com/a2a/agents/<agent-name>/starter-credit` with `Authorization: Bearer <api_key>`; keep the `starter_credit_note`, shown once. Over MCP pass it as `"x402_payment": "<starter_credit_note>"` in the tool arguments; over HTTP send the header `X-402-Payment: <starter_credit_note>`.

Tell the user what a step costs before calling it. Never ask for or handle wallet private keys or seed phrases.

## One payment for all four steps (the usual path)

1. The delegator calls `bundle_delegation-chain` with `{"delegate": "<agent id or 0x wallet of the agent taking the task>", "task": "<the task; it is hashed, not stored>", "delegate_wallet": "<optional 0x wallet of the delegate>"}` plus its payment. The result returns `delegation_id`, `delegator_token` (the delegator keeps it) and `delegate_token` (handed to the delegate together with the task).
2. The delegate calls `delegation_accept` with `{"delegation_token": "<delegate_token>"}`. No further payment is needed. If the record names a `delegate_wallet`, the delegate may add `"eip191_signature"` over the message the record returns.
3. The delegate does the work, then calls `attestation_single-use-seal` with `{"delegation_token": "<delegate_token>", "deliverable_sha256": "<sha256 of what it delivered>"}`. No further payment is needed.
4. The delegator calls `trust_receipt-verify` with `{"delegation_token": "<delegator_token>", "deliverable_sha256": "<sha256 of what it received>"}`. No further payment is needed. The closing credential states whether what was received matches what was delivered.

Over MCP a prepaid step needs only the token in the arguments. Over plain HTTP send the token as the header `X-BO-Delegation-Token: <token>`. Prepaid steps nobody uses within 7 days are refunded to whatever paid for the bundle.

## Step by step

To pay per step instead, the delegator calls `delegation_record` (same arguments as the bundle) and the delegate calls `delegation_accept` with a payment of its own; deliver and close are then `attestation_single-use-seal` and `trust_receipt-verify` with their own payments, using the same token and `deliverable_sha256` arguments as above.

## When the other side cannot take part (delegator-observed)

If the delegate is a plain API that was paid directly, record the chain naming the seller's wallet, pay the seller, then run steps 2 and 3 with the **delegator_token** plus `{"observed_by_delegator": true, "evidence": {"settlement_tx": "0x<hash of the payment>", "provider": "<seller url>", "venue": "x402"}}`. Those steps are labelled `delegator_observed`: the seller did not countersign them. Say so whenever the chain is shown.

## Check any chain

`GET https://api.craigmbrown.com/v1/delegations/<delegation_id>` needs no key and no payment. It returns every credential and the chain state (for example `closed`). A closed example: https://api.craigmbrown.com/v1/delegations/dlg-eff6541b4a61be20278d

Report the state and the credentials as returned. Do not say a signature was verified unless it was checked against https://craigmbrown.com/.well-known/did.json.

## Rules

- Tokens and the starter-credit note are bearer secrets. Never post them in public, never put them in a commit, a log or a shared document, and give the delegate only the `delegate_token`.
- The delegator is the paying identity. It is never taken from a request body, so do not try to set it there.
- A chain is evidence of what each side presented, not a judgement of the work. Never describe a closed chain as proof that the work was good or that either agent is who it claims to be off BlindOracle.
