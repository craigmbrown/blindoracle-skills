#!/usr/bin/env python3
"""Verify a BlindOracle deliverable without any credential.

Two independent checks, both key-free:

  1. INTEGRITY — recompute SHA-256 over the delivered content and compare it to
     the `content_sha256` in the deliverable's `bo_trust` envelope. A mismatch
     means the bytes you are holding are not the bytes that were stamped.
  2. SETTLEMENT (optional) — if you have the payment transaction hash, confirm it
     on Base through the public JSON-RPC endpoint. No API key, no account.

Provenance is reported, never inferred: `ai_generated` is tri-state, and an
absent value is reported as "not recorded", which is NOT a claim that no model
was involved.

Usage:
    python3 verify.py --deliverable result.json
    python3 verify.py --deliverable result.json --content-field output
    python3 verify.py --deliverable result.json --tx 0x<payment-tx-hash>
    python3 verify.py --content-file body.md --expect-sha256 <hex>

Exit code 0 = every requested check passed, 1 = a check failed, 2 = bad input.
Stdlib only. Copyright (c) 2026 Craig M. Brown. All rights reserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

BASE_RPC = "https://mainnet.base.org"
CONTENT_FIELDS = ("output", "content", "text", "result", "deliverable", "body")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_envelope(obj: Any) -> Optional[Dict[str, Any]]:
    """Locate the bo_trust envelope anywhere in the payload."""
    if isinstance(obj, dict):
        if isinstance(obj.get("bo_trust"), dict):
            return obj["bo_trust"]
        if "content_sha256" in obj:
            return obj
        for value in obj.values():
            found = find_envelope(value)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_envelope(item)
            if found:
                return found
    return None


def find_content(obj: Any, field: Optional[str]) -> Tuple[Optional[str], str]:
    """Return (content, where-it-came-from)."""
    if field:
        if isinstance(obj, dict) and field in obj:
            return str(obj[field]), field
        return None, f"{field} (absent)"
    if isinstance(obj, dict):
        for name in CONTENT_FIELDS:
            if isinstance(obj.get(name), str):
                return obj[name], name
        for key, value in obj.items():
            if isinstance(value, dict):
                content, where = find_content(value, None)
                if content is not None:
                    return content, f"{key}.{where}"
    return None, "not found"


def check_tx(tx_hash: str, timeout: int = 15) -> Dict[str, Any]:
    """Confirm a transaction on Base via the public RPC. Keyless."""
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "eth_getTransactionReceipt", "params": [tx_hash],
    }).encode("utf-8")
    request = urllib.request.Request(
        BASE_RPC, data=payload,
        headers={"Content-Type": "application/json",
                 "User-Agent": "blindoracle-receipt-verifier/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"ok": False, "reason": f"RPC unreachable: {exc}"}
    receipt = body.get("result")
    if not receipt:
        return {"ok": False, "reason": "no receipt — unknown or unconfirmed tx"}
    status = receipt.get("status")
    return {
        "ok": status == "0x1",
        "status": status,
        "block": receipt.get("blockNumber"),
        "to": receipt.get("to"),
        "reason": "reverted" if status != "0x1" else "confirmed",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Key-free verification of a BlindOracle deliverable.")
    parser.add_argument("--deliverable", help="JSON file as returned by the SKU")
    parser.add_argument("--content-file", help="raw content bytes, if delivered separately")
    parser.add_argument("--content-field", help="which JSON field holds the hashed content")
    parser.add_argument("--expect-sha256", help="compare against this digest instead of the envelope's")
    parser.add_argument("--tx", help="payment transaction hash to confirm on Base")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if not args.deliverable and not args.content_file:
        parser.error("give --deliverable and/or --content-file")

    report: Dict[str, Any] = {"checks": {}}
    failed = False

    content: Optional[str] = None
    source = "none"
    envelope: Dict[str, Any] = {}

    if args.deliverable:
        try:
            with open(args.deliverable, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, ValueError) as exc:
            print(f"cannot read --deliverable: {exc}", file=sys.stderr)
            return 2
        envelope = find_envelope(payload) or {}
        content, source = find_content(payload, args.content_field)

    if args.content_file:
        try:
            with open(args.content_file, "r", encoding="utf-8") as handle:
                content = handle.read()
            source = args.content_file
        except OSError as exc:
            print(f"cannot read --content-file: {exc}", file=sys.stderr)
            return 2

    expected = args.expect_sha256 or envelope.get("content_sha256")

    if content is None:
        report["checks"]["integrity"] = {"ok": False, "reason": f"content not located ({source})"}
        failed = True
    elif not expected:
        report["checks"]["integrity"] = {"ok": False, "reason": "no content_sha256 to compare against"}
        failed = True
    else:
        actual = sha256_hex(content)
        ok = actual.lower() == str(expected).lower()
        report["checks"]["integrity"] = {
            "ok": ok, "content_from": source,
            "reason": "sha256 matches" if ok else "sha256 mismatch — these are not the stamped bytes",
            "expected": expected, "actual": actual,
            "bytes": len(content.encode("utf-8")),
        }
        failed = failed or not ok

    if envelope:
        generated = envelope.get("ai_generated")
        report["provenance"] = {
            "ai_generated": ("yes" if generated is True
                             else "no" if generated is False else "not recorded"),
            "ai_model": envelope.get("ai_model"),
            "scanner": envelope.get("scanner"),
            "scan_verdict": envelope.get("scan_verdict"),
            "content_scanned": envelope.get("content_scanned"),
            "source": envelope.get("source"),
            "retrieved_at": envelope.get("retrieved_at"),
            "powered_by": envelope.get("powered_by"),
        }
    else:
        report["provenance"] = {"ai_generated": "not recorded", "note": "no bo_trust envelope found"}

    if args.tx:
        result = check_tx(args.tx)
        report["checks"]["settlement"] = result
        failed = failed or not result.get("ok")

    if args.json:
        print(json.dumps(report, indent=2))
        return 1 if failed else 0

    integrity = report["checks"]["integrity"]
    if integrity.get("ok"):
        print(f"INTEGRITY  PASS  sha256 matches ({integrity['bytes']} bytes from '{integrity['content_from']}')")
    else:
        print(f"INTEGRITY  FAIL  {integrity.get('reason', '')}")
        if integrity.get("actual"):
            print(f"           expected {integrity['expected']}")
            print(f"           actual   {integrity['actual']}")
    provenance = report["provenance"]
    model_note = (f" ({provenance.get('ai_model')})"
                  if provenance["ai_generated"] == "yes" and provenance.get("ai_model") else "")
    print(f"PROVENANCE       AI-generated: {provenance['ai_generated']}{model_note}")
    if provenance.get("scan_verdict") is not None:
        print(f"                 scan: {provenance.get('scan_verdict')} by {provenance.get('scanner')}")
    if "settlement" in report["checks"]:
        settlement = report["checks"]["settlement"]
        verdict = "PASS" if settlement.get("ok") else "FAIL"
        print(f"SETTLEMENT {verdict}  {settlement.get('reason')}"
              + (f" in block {settlement.get('block')}" if settlement.get("block") else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
