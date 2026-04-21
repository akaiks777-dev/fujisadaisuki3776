#!/bin/bash
# ロールバック（復元）システム
# 用途: Claude Code 設定ファイルのスナップショット取得・一覧表示・復元
# 保存先: ~/.claude/backups/snapshots/YYYY-MM-DD_HHMMSS/
# 保存期間: 永久保持（自動削除なし）
# 保存条件: 前回と内容が異なる場合のみ保存

CLAUDE="$HOME/.claude"
BACKUP_DIR="$CLAUDE/backups/snapshots"
# 永久保持（自動削除なし）

# バックアップ対象ファイル（個別）
BACKUP_FILES=(
    "CLAUDE.md"
    "settings.json"
    "kuro_screenshot.py"
    "add_japanese_summaries.py"
    "get_today_title.py"
    "mercari_photo.py"
    "libecity-seen-articles.json"
)

# バックアップ対象ディレクトリ
BACKUP_DIRS=(
    "org"
    "scheduled-tasks"
    "plugins"
)

# ========================================
# snapshot: スナップショット取得
# ========================================
do_snapshot() {
    local timestamp=$(date +"%Y-%m-%d_%H%M%S")
    local snap_dir="$BACKUP_DIR/$timestamp"

    mkdir -p "$snap_dir"

    # 個別ファイルをコピー
    for f in "${BACKUP_FILES[@]}"; do
        if [ -f "$CLAUDE/$f" ]; then
            cp "$CLAUDE/$f" "$snap_dir/"
        fi
    done

    # ディレクトリをコピー
    for d in "${BACKUP_DIRS[@]}"; do
        if [ -d "$CLAUDE/$d" ]; then
            mkdir -p "$snap_dir/$d"
            rsync -a "$CLAUDE/$d/" "$snap_dir/$d/"
        fi
    done

    # 前回スナップショットと比較
    local latest=$(ls -d "$BACKUP_DIR"/????-??-??_?????? 2>/dev/null | sort | tail -2 | head -1)

    if [ -n "$latest" ] && [ "$latest" != "$snap_dir" ]; then
        # diff で比較（差分がなければ削除）
        local has_diff=false
        if ! diff -rq "$latest" "$snap_dir" > /dev/null 2>&1; then
            has_diff=true
        fi

        if [ "$has_diff" = false ]; then
            rm -rf "$snap_dir"
            echo "📋 前回と差分なし — スナップショットをスキップしました"
            return 0
        fi
    fi

    # 自動削除なし（永久保持）

    echo "✅ スナップショット保存完了: $timestamp"
}

# ========================================
# list: バックアップ一覧表示
# ========================================
do_list() {
    local snapshots=($(ls -d "$BACKUP_DIR"/????-??-??_?????? 2>/dev/null | sort -r))

    if [ ${#snapshots[@]} -eq 0 ]; then
        echo "📭 バックアップがありません"
        return 0
    fi

    echo "========================================"
    echo "📦 バックアップ一覧（新しい順）"
    echo "========================================"
    echo ""

    local i=1
    for snap in "${snapshots[@]}"; do
        local name=$(basename "$snap")
        # YYYY-MM-DD_HHMMSS → 読みやすい形式に変換
        local date_part="${name:0:10}"
        local time_part="${name:11:2}:${name:13:2}:${name:15:2}"
        local size=$(du -sh "$snap" 2>/dev/null | cut -f1)

        echo "  [$i] $date_part $time_part ($size)"

        # 変更ファイルの概要を表示（前のスナップショットとの差分）
        if [ $i -lt ${#snapshots[@]} ]; then
            local prev="${snapshots[$i]}"
            local changed=$(diff -rq "$prev" "$snap" 2>/dev/null | grep -c "differ")
            local added=$(diff -rq "$prev" "$snap" 2>/dev/null | grep -c "Only in $snap")
            if [ "$changed" -gt 0 ] || [ "$added" -gt 0 ]; then
                echo "      変更: ${changed}ファイル / 追加: ${added}ファイル"
            fi
        else
            echo "      （初回スナップショット）"
        fi
        echo ""
        i=$((i + 1))
    done

    echo "========================================"
    echo "復元するには: bash ~/.claude/rollback.sh restore <番号>"
    echo "例: bash ~/.claude/rollback.sh restore 1"
    echo "========================================"
}

# ========================================
# restore: 指定バックアップから復元
# ========================================
do_restore() {
    local target="$1"
    local snapshots=($(ls -d "$BACKUP_DIR"/????-??-??_?????? 2>/dev/null | sort -r))

    if [ ${#snapshots[@]} -eq 0 ]; then
        echo "📭 バックアップがありません"
        return 1
    fi

    # 番号指定の場合
    if [[ "$target" =~ ^[0-9]+$ ]]; then
        local idx=$((target - 1))
        if [ $idx -lt 0 ] || [ $idx -ge ${#snapshots[@]} ]; then
            echo "❌ 無効な番号です（1〜${#snapshots[@]}）"
            return 1
        fi
        target=$(basename "${snapshots[$idx]}")
    fi

    local snap_dir="$BACKUP_DIR/$target"

    if [ ! -d "$snap_dir" ]; then
        echo "❌ スナップショットが見つかりません: $target"
        return 1
    fi

    # 復元前に現在の状態を保存（安全策）
    echo "🔒 復元前に現在の状態をバックアップしています..."
    do_snapshot

    echo ""
    echo "🔄 復元開始: $target"

    # 個別ファイルを復元
    for f in "${BACKUP_FILES[@]}"; do
        if [ -f "$snap_dir/$f" ]; then
            cp "$snap_dir/$f" "$CLAUDE/$f"
            echo "  ✅ $f"
        fi
    done

    # ディレクトリを復元
    for d in "${BACKUP_DIRS[@]}"; do
        if [ -d "$snap_dir/$d" ]; then
            rsync -a --delete "$snap_dir/$d/" "$CLAUDE/$d/"
            echo "  ✅ $d/"
        fi
    done

    echo ""
    echo "✅ 復元完了: $target"
    echo "⚠️  復元前の状態もバックアップ済みです"
}

# ========================================
# メイン
# ========================================
case "${1:-}" in
    snapshot)
        do_snapshot
        ;;
    list)
        do_list
        ;;
    restore)
        if [ -z "${2:-}" ]; then
            echo "❌ 復元先を指定してください"
            echo "使い方: bash ~/.claude/rollback.sh restore <番号>"
            echo "一覧を見るには: bash ~/.claude/rollback.sh list"
            exit 1
        fi
        do_restore "$2"
        ;;
    *)
        echo "使い方:"
        echo "  bash ~/.claude/rollback.sh snapshot   # スナップショット取得"
        echo "  bash ~/.claude/rollback.sh list       # バックアップ一覧"
        echo "  bash ~/.claude/rollback.sh restore <番号>  # 復元"
        ;;
esac
