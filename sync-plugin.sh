#!/bin/sh
# Copy the plugin skills into the Claude plugin and the Hermes plugin.
# Claude: keeps the plugin's narrowed allowed-tools lines and ${CLAUDE_SKILL_DIR} paths.
# Hermes: drops allowed-tools (Claude syntax) and uses ${HERMES_SKILL_DIR}.
# Run after editing bo-catalog/, verify-blindoracle-receipt/ or prove-a-delegation/ at the repository root.
set -e
cd "$(dirname "$0")"
for s in bo-catalog verify-blindoracle-receipt prove-a-delegation; do
  keep=$(grep '^allowed-tools:' "claude-plugin/skills/$s/SKILL.md")
  rm -rf "claude-plugin/skills/$s" && cp -r "$s" "claude-plugin/skills/$s"
  sed -i "s|^allowed-tools:.*|$keep|" "claude-plugin/skills/$s/SKILL.md"

  rm -rf "hermes-plugin/skills/$s" && cp -r "$s" "hermes-plugin/skills/$s"
  sed -i '/^allowed-tools:/d' "hermes-plugin/skills/$s/SKILL.md"
done
sed -i 's|python3 verify.py|python3 ${CLAUDE_SKILL_DIR}/verify.py|g' claude-plugin/skills/verify-blindoracle-receipt/SKILL.md
sed -i 's|python3 verify.py|python3 ${HERMES_SKILL_DIR}/verify.py|g' hermes-plugin/skills/verify-blindoracle-receipt/SKILL.md
echo "synced; now run: claude plugin validate ./claude-plugin && hermes plugins validate ./hermes-plugin"
