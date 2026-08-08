#!/usr/bin/env python3
# Copyright (c) 2026 Craig M. Brown. All rights reserved.
"""pay-blindoracle-via-x402 — public buyer skill for BlindOracle SKUs.

Self-contained x402 v2 "exact" buyer: signs an EIP-3009 TransferWithAuthorization
for USDC on Base and submits it as the X-PAYMENT header to a BlindOracle x402
endpoint. Gasless (the CDP facilitator submits the tx); self-custodial (you sign,
you never share the key; a bad signature is simply rejected — no fund risk).

Usage:
  # print the HTTP 402 challenge only — no key needed, nothing is sent
  python3 pay.py --url https://api.craigmbrown.com/v1/reputation/blindoracle --dry-run

  # sign + submit + settle on Base, return the deliverable + tx
  BUYER_PRIVATE_KEY=0x... python3 pay.py --url https://api.craigmbrown.com/v1/reputation/blindoracle

Requires: pip install eth-account
Wallet key is read from the BUYER_PRIVATE_KEY environment variable ONLY.
Never hardcode a private key in this file or pass it on the command line.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (pay-blindoracle-via-x402 skill)"


def fetch_challenge(url: str) -> dict:
    """GET the endpoint; return the x402 402-challenge JSON (or raise)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {
                "status": r.status,
                "note": "endpoint returned non-402 (no payment required?)",
                "body": r.read(2000).decode("utf-8", "replace"),
            }
    except urllib.error.HTTPError as e:
        if e.code == 402:
            try:
                return {"status": 402, "challenge": json.loads(e.read())}
            except Exception:
                return {"status": 402, "challenge_raw": "unparseable 402 body"}
        return {"status": e.code, "error": e.reason}


def build_payment(acct, challenge: dict) -> dict:
    """Sign an EIP-3009 TransferWithAuthorization for the quoted USDC amount."""
    from eth_account.messages import encode_typed_data

    accepts = challenge["accepts"][0]
    chain_id = int(accepts["network"].split(":")[1])  # eip155:8453 -> 8453
    usdc = accepts["asset"]
    now = int(time.time())
    auth = {
        "from": acct.address,
        "to": accepts["payTo"],
        "value": int(accepts["amount"]),
        "validAfter": 0,
        # generous window so the facilitator has time to submit
        "validBefore": now + max(int(accepts.get("maxTimeoutSeconds", 60)), 300),
        "nonce": "0x" + secrets.token_bytes(32).hex(),
    }
    typed = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
            ],
        },
        "domain": {
            "name": accepts["extra"]["name"],
            "version": accepts["extra"]["version"],
            "chainId": chain_id,
            "verifyingContract": usdc,
        },
        "primaryType": "TransferWithAuthorization",
        "message": auth,
    }
    signed = acct.sign_message(encode_typed_data(full_message=typed))
    sig = signed.signature.hex()
    if not sig.startswith("0x"):
        sig = "0x" + sig
    # canonical x402 v2 PaymentPayload: {x402Version, payload, accepted, resource, extensions}
    accepted = {
        k: accepts[k]
        for k in ("scheme", "network", "asset", "amount", "payTo", "maxTimeoutSeconds", "extra")
        if k in accepts
    }
    extensions = accepts.get("extensions") or challenge.get("extensions")
    payment = {
        "x402Version": 2,
        "payload": {
            "signature": sig,
            "authorization": {
                "from": auth["from"],
                "to": auth["to"],
                "value": str(auth["value"]),
                "validAfter": str(auth["validAfter"]),
                "validBefore": str(auth["validBefore"]),
                "nonce": auth["nonce"],
            },
        },
        "accepted": accepted,
    }
    if challenge.get("resource"):
        payment["resource"] = challenge["resource"]
    if extensions:
        payment["extensions"] = extensions
    return payment


def main() -> int:
    ap = argparse.ArgumentParser(description="Pay a BlindOracle SKU via x402.")
    ap.add_argument("--url", required=True, help="BlindOracle x402 endpoint")
    ap.add_argument("--dry-run", action="store_true", help="fetch + print the 402 challenge only")
    args = ap.parse_args()

    if args.dry_run:
        print(json.dumps(fetch_challenge(args.url), indent=2)[:4000])
        return 0

    key = os.environ.get("BUYER_PRIVATE_KEY")
    if not key:
        print("ERROR: set BUYER_PRIVATE_KEY (never hardcode a key in this file).", file=sys.stderr)
        return 2

    try:
        from eth_account import Account
    except ImportError:
        print("ERROR: pip install eth-account", file=sys.stderr)
        return 2

    acct = Account.from_key(key)
    challenge_resp = fetch_challenge(args.url)
    challenge = challenge_resp.get("challenge")
    if not challenge:
        print(f"ERROR: endpoint did not return a 402 challenge: {challenge_resp}", file=sys.stderr)
        return 2

    a = challenge["accepts"][0]
    print(f"[pay] {args.url}")
    print(
        f"[pay] from={acct.address} -> payTo={a['payTo']} "
        f"amount={int(a['amount']) / 1e6:.4f} USDC net={a['network']}"
    )
    payload = build_payment(acct, challenge)
    header = base64.b64encode(json.dumps(payload).encode()).decode()
    print(f"[pay] X-PAYMENT built ({len(header)} b64 chars)")

    req = urllib.request.Request(
        args.url, headers={"User-Agent": UA, "X-PAYMENT": header, "X-402-Payment": header}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        body = resp.read().decode()
        print(f"[pay] HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[pay] HTTP {e.code}")
    print("[pay] response:", body[:1200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
