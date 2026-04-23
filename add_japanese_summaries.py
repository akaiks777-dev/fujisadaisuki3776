#!/usr/bin/env python3
"""
Claude Codeのセッションファイルに日本語サマリーを追加するスクリプト
【2026-04-23 改訂版（ハイブリッド：A+B+C案）】
- B案: サマリー行を先頭に挿入（Claudeアプリが先頭行を読むため）
- 既存サマリーが中間/末尾にある場合は先頭に移動（reposition）
- summaryがないファイルは新規に生成して先頭に挿入
"""
import json
import glob
import os
import tempfile

PROJECT_DIR = os.path.expanduser('~/.claude/projects/-Users-shigesan/')
files = glob.glob(os.path.join(PROJECT_DIR, '*.jsonl'))

added = 0
repositioned = 0
skipped = 0
errors = 0

def atomic_write(filepath, content):
    """一時ファイルに書き込んでからアトミックに置換"""
    dirname = os.path.dirname(filepath)
    tmp_fd, tmp_path = tempfile.mkstemp(dir=dirname, prefix='.summary_tmp_', suffix='.jsonl')
    try:
        with os.fdopen(tmp_fd, 'w', encoding='utf-8') as tmp:
            tmp.write(content)
        os.replace(tmp_path, filepath)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

for f in files:
    try:
        with open(f, encoding='utf-8') as fp:
            lines = fp.readlines()

        if not lines:
            continue

        # 1行目がsummaryなら何もしない
        first_line = lines[0].strip()
        if first_line:
            try:
                first_data = json.loads(first_line)
                if first_data.get('type') == 'summary':
                    skipped += 1
                    continue
            except json.JSONDecodeError:
                pass

        # 既存のsummary行を探す（全行スキャン）
        existing_summary_line = None
        other_lines = []
        first_user_text = None
        for line in lines:
            stripped = line.strip()
            if not stripped:
                other_lines.append(line)
                continue
            try:
                data = json.loads(stripped)
                if data.get('type') == 'summary' and existing_summary_line is None:
                    existing_summary_line = line if line.endswith('\n') else line + '\n'
                    # このsummary行はother_linesに入れない（先頭に移す）
                    continue
                # ユーザーテキスト候補を拾う
                if first_user_text is None:
                    if data.get('type') == 'queue-operation' and data.get('operation') == 'enqueue':
                        content = data.get('content', '')
                        if isinstance(content, str) and content.strip():
                            first_user_text = content.strip().replace('\n', ' ')
                    elif data.get('type') == 'user':
                        msg = data.get('message', {})
                        content = msg.get('content', '')
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and c.get('type') == 'text':
                                    first_user_text = c.get('text', '').strip().replace('\n', ' ')
                                    break
                        elif isinstance(content, str):
                            first_user_text = content.strip().replace('\n', ' ')
            except json.JSONDecodeError:
                pass
            other_lines.append(line)

        if existing_summary_line:
            # 既存summaryを先頭に移動
            new_content = existing_summary_line + ''.join(other_lines)
            atomic_write(f, new_content)
            print(f'↑ {os.path.basename(f)[:20]} → 既存summaryを先頭に移動')
            repositioned += 1
        elif first_user_text:
            # summaryが存在しない場合は新規生成
            title = first_user_text[:25]
            if len(first_user_text) > 25:
                title += '…'
            summary_entry = json.dumps({'type': 'summary', 'summary': title}, ensure_ascii=False) + '\n'
            new_content = summary_entry + ''.join(other_lines)
            atomic_write(f, new_content)
            print(f'✓ {os.path.basename(f)[:20]} → {title}')
            added += 1
        else:
            skipped += 1

    except Exception as e:
        print(f'✗ エラー: {os.path.basename(f)[:20]} - {e}')
        errors += 1

print(f'\n完了: {added}件新規追加 / {repositioned}件先頭に移動 / {skipped}件スキップ / {errors}件エラー')
