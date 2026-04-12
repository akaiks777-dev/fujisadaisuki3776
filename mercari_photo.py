#!/usr/bin/env python3
"""
メルカリ出品用写真加工スクリプト
- ~/Downloads/ から最新の画像を取得
- 明るさ・コントラスト調整
- 正方形トリミング
- ~/Downloads/mercari_ready/ に保存
"""

import os
import sys
import glob
from datetime import datetime
from PIL import Image, ImageEnhance, ImageOps

DOWNLOADS = os.path.expanduser("~/Downloads")
OUTPUT_DIR = os.path.join(DOWNLOADS, "mercari_ready")

def get_latest_images(n=10):
    """Downloadsから最新n枚の画像を取得"""
    patterns = ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.HEIC"]
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(DOWNLOADS, pat)))
    # mercari_readyフォルダ内は除外
    files = [f for f in files if "mercari_ready" not in f]
    # 更新日時でソート（新しい順）
    files.sort(key=os.path.getmtime, reverse=True)
    return files[:n]

def process_image(input_path, output_path, size=1080):
    """画像をメルカリ向けに最適化（軽微な明るさ補正のみ・過度な加工なし）"""
    img = Image.open(input_path).convert("RGB")

    # 正方形にトリミング（中央）
    w, h = img.size
    min_side = min(w, h)
    left = (w - min_side) // 2
    top = (h - min_side) // 2
    img = img.crop((left, top, left + min_side, top + min_side))

    # リサイズ（1080×1080）
    img = img.resize((size, size), Image.LANCZOS)

    # 明るさ：軽微な補正のみ（実物と大きく変わらない範囲）
    img = ImageEnhance.Brightness(img).enhance(1.1)

    img.save(output_path, "JPEG", quality=95)
    return output_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    images = get_latest_images()
    if not images:
        print("画像が見つかりませんでした。")
        return

    print(f"\n📸 {len(images)}枚の画像を加工します...\n")
    results = []
    for i, path in enumerate(images):
        filename = os.path.basename(path)
        out_name = f"mercari_{i+1:02d}_{filename}"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        process_image(path, out_path)
        results.append(out_path)
        print(f"  ✅ {filename} → {out_name}")

    print(f"\n✨ 加工完了！{OUTPUT_DIR} に保存しました。")
    print(f"合計 {len(results)} 枚")
    return results

if __name__ == "__main__":
    main()
