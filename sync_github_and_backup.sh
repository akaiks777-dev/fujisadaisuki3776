#!/bin/bash
# ============================================
# Claude Code 自動同期・バックアップスクリプト
# 毎夜23:00に実行
# ① GitHub に設定ファイルをpush
# ② 外付けHDD(Drive_Rest)にチャット履歴をrsync
# ============================================

LOG="$HOME/.claude/sync_backup.log"
CLAUDE="$HOME/.claude"
HDD_ROOT="/Volumes/KUROKOちゃんバックアップ/claude-backup"
DATE=$(date '+%Y-%m-%d %H:%M:%S')
# 今日の日付＋作業タイトルでフォルダ名を生成
TODAY_TITLE=$(python3 "$CLAUDE/get_today_title.py" 2>/dev/null || date '+%Y-%m-%d')
HDD="$HDD_ROOT/$TODAY_TITLE"

echo "" >> "$LOG"
echo "========================================" >> "$LOG"
echo " $DATE 同期・バックアップ開始" >> "$LOG"
echo "========================================" >> "$LOG"

# ---- ① GitHub push（設定ファイル） ----
echo "【GitHub push】" >> "$LOG"
cd "$CLAUDE" || exit 1

git add -A >> "$LOG" 2>&1
CHANGED=$(git diff --cached --name-only | wc -l | tr -d ' ')

if [ "$CHANGED" -gt "0" ]; then
    git commit -m "Auto sync: $(date '+%Y-%m-%d %H:%M')" >> "$LOG" 2>&1
    git push origin main >> "$LOG" 2>&1
    echo "✓ $CHANGED ファイルをGitHubにpush" >> "$LOG"
else
    echo "✓ 変更なし（push不要）" >> "$LOG"
fi

# ---- ② 外付けHDDバックアップ（チャット履歴） ----
echo "【外付けHDDバックアップ】" >> "$LOG"

if [ -d "/Volumes/KUROKOちゃんバックアップ" ]; then
    echo "バックアップ先: $TODAY_TITLE" >> "$LOG"
    mkdir -p "$HDD/projects"
    rsync -av "$CLAUDE/projects/" "$HDD/projects/" >> "$LOG" 2>&1
    rsync -av "$CLAUDE/history.jsonl" "$HDD/history.jsonl" >> "$LOG" 2>&1
    echo "✓ チャット履歴をKUROKOちゃんバックアップにバックアップ完了" >> "$LOG"
else
    echo "⚠️  Drive_Rest がマウントされていません。スキップ。" >> "$LOG"
fi

echo "✅ 完了: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"
