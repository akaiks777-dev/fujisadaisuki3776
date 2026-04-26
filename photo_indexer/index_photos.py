#!/usr/bin/env python3
"""
マスターの写真ライブラリ AIタグ付けインデックス
Phase 1: フォルダ名 + EXIF データ抽出
"""
import os
import json
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import time
from datetime import datetime

PHOTO_ROOT = Path.home() / "Pictures" / "Googleフォト整理"
DB_PATH = Path.home() / ".claude" / "photo_indexer" / "photo_db.json"
PROGRESS_PATH = Path.home() / ".claude" / "photo_indexer" / "progress.json"

def get_exif_data(image_path):
    """EXIFデータ抽出"""
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
            if not exif:
                return {}
            
            data = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "DateTimeOriginal":
                    data["datetime"] = str(value)
                elif tag == "Make":
                    data["camera_make"] = str(value)
                elif tag == "Model":
                    data["camera_model"] = str(value)
                elif tag == "GPSInfo":
                    gps = {}
                    for gps_id, gps_val in value.items():
                        gps_tag = GPSTAGS.get(gps_id, gps_id)
                        gps[gps_tag] = gps_val
                    data["gps"] = str(gps)[:200]  # GPS情報抜粋
            return data
    except Exception as e:
        return {}

def index_photos():
    db = []
    start = time.time()
    photo_count = 0
    
    # フォルダ巡回
    for folder in sorted(PHOTO_ROOT.iterdir()):
        if not folder.is_dir():
            continue
        
        folder_name = folder.name
        # フォルダ名からタグ抽出（例: "2025年11月_富士山" → ["2025年11月", "富士山"]）
        parts = folder_name.replace('_', ' ').split()
        folder_tags = parts
        
        # 写真ファイル列挙
        for ext in ['jpg', 'jpeg', 'png', 'heic', 'JPG', 'JPEG', 'PNG', 'HEIC']:
            for photo in folder.rglob(f"*.{ext}"):
                photo_count += 1
                
                # 基本情報
                stat = photo.stat()
                entry = {
                    "id": photo_count,
                    "path": str(photo),
                    "folder": folder_name,
                    "folder_tags": folder_tags,
                    "filename": photo.name,
                    "size_mb": round(stat.st_size / 1024 / 1024, 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
                
                # EXIF取得
                exif = get_exif_data(photo)
                entry["exif"] = exif
                
                db.append(entry)
                
                if photo_count % 500 == 0:
                    elapsed = time.time() - start
                    print(f"  処理 {photo_count}枚 / 経過 {elapsed:.0f}秒", flush=True)
    
    # データベース保存
    DB_PATH.parent.mkdir(exist_ok=True, parents=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=1)
    
    elapsed = time.time() - start
    print(f"\n=== Phase 1+2 完了 ===")
    print(f"処理枚数: {photo_count}枚")
    print(f"処理時間: {elapsed:.1f}秒")
    print(f"保存先: {DB_PATH}")
    print(f"DBサイズ: {DB_PATH.stat().st_size / 1024:.0f} KB")

if __name__ == "__main__":
    index_photos()
