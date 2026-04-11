#!/usr/bin/env python3
"""
今日のClaudeセッションからタイトルを自動生成するスクリプト
出力: 2026-04-11_GitHub同期システム構築 のような文字列
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
today = datetime.now(JST).strftime('%Y-%m-%d')
projects_dir = Path.home() / '.claude' / 'projects'

titles = []

# 今日更新されたセッションファイルを検索
for jsonl_file in projects_dir.rglob('*.jsonl'):
    try:
        mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime, tz=JST)
        if mtime.strftime('%Y-%m-%d') != today:
            continue

        # summaryを持つメッセージを探す（add_japanese_summaries.pyが付与）
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    summary = data.get('summary', '')
                    if summary and len(summary) > 3:
                        titles.append(summary[:20])  # 最大20文字
                        break
                except Exception:
                    continue
    except Exception:
        continue

# タイトルを結合（最大2件、重複除去）
seen = []
for t in titles:
    if t not in seen:
        seen.append(t)

if seen:
    combined = '・'.join(seen[:2])
    # ファイル名に使えない文字を除去
    for ch in r'\/:*?"<>|':
        combined = combined.replace(ch, '')
    print(f"{today}_{combined}")
else:
    print(today)
