#!/bin/bash
# ~/.claude と Espanso 設定を iCloud Drive に保存するスクリプト
# Mac mini（メイン機）で実行してください

ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeCode_Sync"
CLAUDE="$HOME/.claude"
ESPANSO="$HOME/Library/Application Support/espanso"

echo "========================================"
echo " iCloud Drive へ同期開始"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# --- Claude Code 設定 ---
echo ""
echo "【Claude Code 設定】"
cp "$CLAUDE/CLAUDE.md" "$ICLOUD/CLAUDE.md" 2>/dev/null && echo "✓ CLAUDE.md"
cp "$CLAUDE/settings.json" "$ICLOUD/settings.json" 2>/dev/null && echo "✓ settings.json"
cp "$CLAUDE/kuro_screenshot.py" "$ICLOUD/kuro_screenshot.py" 2>/dev/null && echo "✓ kuro_screenshot.py"
cp "$CLAUDE/libecity-seen-articles.json" "$ICLOUD/libecity-seen-articles.json" 2>/dev/null && echo "✓ libecity-seen-articles.json"

# plugins
rsync -av --delete "$CLAUDE/plugins/" "$ICLOUD/plugins/" 2>/dev/null && echo "✓ plugins/"

# scheduled-tasks（新規追加）
mkdir -p "$ICLOUD/scheduled-tasks"
rsync -av --delete "$CLAUDE/scheduled-tasks/" "$ICLOUD/scheduled-tasks/" 2>/dev/null && echo "✓ scheduled-tasks/"

# --- Espanso 設定 ---
echo ""
echo "【Espanso 設定】"
mkdir -p "$ICLOUD/espanso/match" "$ICLOUD/espanso/config"
rsync -av "$ESPANSO/match/" "$ICLOUD/espanso/match/" 2>/dev/null && echo "✓ espanso/match/"
rsync -av "$ESPANSO/config/" "$ICLOUD/espanso/config/" 2>/dev/null && echo "✓ espanso/config/"

# --- 同期スクリプト・シェル設定 ---
echo ""
echo "【同期スクリプト・シェル設定】"
mkdir -p "$ICLOUD/scripts"
cp "$HOME/sync_menu.sh" "$ICLOUD/scripts/sync_menu.sh" 2>/dev/null && echo "✓ sync_menu.sh"
cp "$HOME/sync_claude.sh" "$ICLOUD/scripts/sync_claude.sh" 2>/dev/null && echo "✓ sync_claude.sh"
cp "$HOME/sync_claude_upload.sh" "$ICLOUD/scripts/sync_claude_upload.sh" 2>/dev/null && echo "✓ sync_claude_upload.sh"
cp "$HOME/.zshrc" "$ICLOUD/scripts/.zshrc" 2>/dev/null && echo "✓ .zshrc"

# --- LaunchAgents ---
echo ""
echo "【LaunchAgents】"
mkdir -p "$ICLOUD/LaunchAgents"
for plist in com.shigesan.restore_claude_settings com.shigesan.sync_claude com.shigesan.sync_claude_upload com.shigesan.sync_log_notify; do
    cp "$HOME/Library/LaunchAgents/${plist}.plist" "$ICLOUD/LaunchAgents/${plist}.plist" 2>/dev/null && echo "✓ ${plist}.plist"
done

echo ""
echo "✅ iCloud への同期完了！"
echo "========================================"
