#!/bin/bash
# 本店⇔支店 同期差分チェックスクリプト（フェーズ1）
# 使い方: bash ~/.claude/sync_diff_check.sh

ICLOUD_PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeCode_Sync"
LOCAL_PATH="$HOME/.claude"

if [ ! -d "$ICLOUD_PATH" ]; then
    echo "⚠️ iCloud Sync フォルダが見つかりません: $ICLOUD_PATH"
    exit 1
fi

# チェック対象ファイル
FILES=(
    "CLAUDE.md"
    "settings.json"
    "kuro_screenshot.py"
    "relay_notes.md"
    "discussion_board.md"
    "statusboard.md"
    "rollback.sh"
    "master_schedule.json"
)

DIFF_COUNT=0
DIFF_DETAILS=""

echo "🔍 本店⇔iCloud 差分チェック開始..."
echo ""

for FILE in "${FILES[@]}"; do
    LOCAL_FILE="$LOCAL_PATH/$FILE"
    ICLOUD_FILE="$ICLOUD_PATH/$FILE"

    # 両方存在
    if [ -f "$LOCAL_FILE" ] && [ -f "$ICLOUD_FILE" ]; then
        if ! diff -q "$LOCAL_FILE" "$ICLOUD_FILE" > /dev/null 2>&1; then
            LOCAL_TIME=$(stat -f "%m" "$LOCAL_FILE" 2>/dev/null)
            ICLOUD_TIME=$(stat -f "%m" "$ICLOUD_FILE" 2>/dev/null)
            
            if [ "$LOCAL_TIME" -gt "$ICLOUD_TIME" ]; then
                NEWER="🖥️ 本店が新しい"
            elif [ "$ICLOUD_TIME" -gt "$LOCAL_TIME" ]; then
                NEWER="☁️ iCloud(支店)が新しい"
            else
                NEWER="同時刻だが内容が違う"
            fi
            
            DIFF_DETAILS="${DIFF_DETAILS}  ❌ $FILE - $NEWER\n"
            DIFF_COUNT=$((DIFF_COUNT + 1))
        fi
    elif [ -f "$LOCAL_FILE" ] && [ ! -f "$ICLOUD_FILE" ]; then
        DIFF_DETAILS="${DIFF_DETAILS}  ⚠️ $FILE - iCloudに存在しない（本店のみ）\n"
        DIFF_COUNT=$((DIFF_COUNT + 1))
    elif [ ! -f "$LOCAL_FILE" ] && [ -f "$ICLOUD_FILE" ]; then
        DIFF_DETAILS="${DIFF_DETAILS}  ⚠️ $FILE - 本店に存在しない（iCloudのみ）\n"
        DIFF_COUNT=$((DIFF_COUNT + 1))
    fi
done

if [ "$DIFF_COUNT" -eq 0 ]; then
    echo "✅ 本店とiCloudは同期済みです"
    exit 0
else
    echo "⚠️ $DIFF_COUNT 箇所の違いがあります："
    echo ""
    echo -e "$DIFF_DETAILS"
    echo ""
    echo "💡 対応するには："
    echo "   - iCloud(支店)が新しい → 「本店から支店」を実行"
    echo "   - 本店が新しい → 「支店から本店」を実行"
    exit $DIFF_COUNT
fi
