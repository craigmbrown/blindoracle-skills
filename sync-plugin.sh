#!/bin/sh
# Copy the two money-free skills into the Claude plugin, keeping the plugin's
# narrowed allowed-tools lines and ${CLAUDE_SKILL_DIR} paths. Run after editing
# bo-catalog/ or verify-blindoracle-receipt/ at the repository root.
set -e
cd "$(dirname "$0")"
for s in bo-catalog verify-blindoracle-receipt; do
  keep=$(grep '^allowed-tools:' "claude-plugin/skills/$s/SKILL.md")
  rm -rf "claude-plugin/skills/$s" && cp -r "$s" "claude-plugin/skills/$s"
  sed -i "s|^allowed-tools:.*|$keep|" "claude-plugin/skills/$s/SKILL.md"
done
sed -i 's|python3 verify.py|python3 ${CLAUDE_SKILL_DIR}/verify.py|g' claude-plugin/skills/verify-blindoracle-receipt/SKILL.md
echo "synced; now run: claude plugin validate ./claude-plugin"
