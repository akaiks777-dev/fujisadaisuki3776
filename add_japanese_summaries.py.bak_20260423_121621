#!/usr/bin/env python3
"""
Claude Codeのセッションファイルに日本語サマリーを追加するスクリプト
- summaryが未設定のセッションに、最初のユーザーメッセージから日本語タイトルを生成
"""
import json
import glob
import os

PROJECT_DIR = os.path.expanduser('~/.claude/projects/-Users-shigesan/')
files = glob.glob(os.path.join(PROJECT_DIR, '*.jsonl'))

added = 0
skipped = 0

for f in files:
    has_summary = False
    first_user_text = None

    with open(f, encoding='utf-8') as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)

                # すでにsummaryがある場合はスキップ
                if data.get('type') == 'summary':
                    has_summary = True
                    break

                # queue-operationのenqueueからユーザーのテキストを取得
                if (data.get('type') == 'queue-operation'
                        and data.get('operation') == 'enqueue'
                        and first_user_text is None):
                    content = data.get('content', '')
                    if content and isinstance(content, str):
                        text = content.strip().replace('\n', ' ')
                        first_user_text = text

                # userタイプのメッセージからも取得を試みる
                if data.get('type') == 'user' and first_user_text is None:
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

    if has_summary:
        skipped += 1
        continue

    if first_user_text:
        # タイトルを25文字以内に切り詰める
        title = first_user_text[:25]
        if len(first_user_text) > 25:
            title += '…'

        summary_entry = json.dumps(
            {'type': 'summary', 'summary': title},
            ensure_ascii=False
        )

        with open(f, 'a', encoding='utf-8') as fp:
            fp.write(summary_entry + '\n')

        print(f'✓ {os.path.basename(f)[:20]} → {title}')
        added += 1

print(f'\n完了: {added}件追加 / {skipped}件スキップ（既存サマリーあり）')
