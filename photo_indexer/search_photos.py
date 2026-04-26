#!/usr/bin/env python3
"""
写真DB検索スクリプト
使い方: python3 search_photos.py <キーワード>
複数キーワードAND検索: python3 search_photos.py 富士山 夕暮れ
"""
import sys
import json
import re
from pathlib import Path

DB_PATH = Path.home() / ".claude" / "photo_indexer" / "photo_db.json"

def search(keywords):
    if not DB_PATH.exists():
        print("DBがまだありません。先に index_photos.py を実行してください。")
        return
    
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    results = []
    for entry in db:
        # 検索対象テキスト
        text = ' '.join([
            entry.get('folder', ''),
            ' '.join(entry.get('folder_tags', [])),
            entry.get('filename', ''),
            str(entry.get('exif', {})),
        ])
        
        # 全キーワード含む？
        if all(kw in text for kw in keywords):
            results.append(entry)
    
    return results

def main():
    if len(sys.argv) < 2:
        print("使い方: python3 search_photos.py <キーワード1> [キーワード2] ...")
        return
    
    keywords = sys.argv[1:]
    results = search(keywords)
    
    print(f"\n=== 検索結果: {' AND '.join(keywords)} ===")
    print(f"ヒット: {len(results)}件\n")
    
    # フォルダごとにグループ化
    by_folder = {}
    for r in results:
        f = r['folder']
        if f not in by_folder:
            by_folder[f] = []
        by_folder[f].append(r)
    
    for folder in sorted(by_folder.keys()):
        items = by_folder[folder]
        print(f"📁 {folder} ({len(items)}枚)")
        for item in items[:3]:
            print(f"   - {item['filename']}")
        if len(items) > 3:
            print(f"   ... 他 {len(items)-3}枚")
        print()

if __name__ == "__main__":
    main()
