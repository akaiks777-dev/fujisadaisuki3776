#!/usr/bin/env python3
"""
Phase 3: AIによる画像キャプション生成
SmolVLM-256M を使って各写真の内容を英語キャプション化
日本語キーワード対応のため、簡易翻訳辞書も併用
"""
import warnings
warnings.filterwarnings('ignore')

import os
import json
import sys
import time
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claude" / "photo_indexer" / "photo_db.json"
CAPTION_DB_PATH = Path.home() / ".claude" / "photo_indexer" / "captions.json"
PROGRESS_PATH = Path.home() / ".claude" / "photo_indexer" / "caption_progress.json"
LOG_PATH = Path.home() / ".claude" / "photo_indexer" / "caption_log.txt"

# 進捗保存間隔（N枚ごと）
SAVE_INTERVAL = 50

# 日英キーワード辞書（検索用）
JP_EN_KEYWORDS = {
    # 動物
    "猫": ["cat", "kitten", "feline"],
    "犬": ["dog", "puppy", "canine"],
    "コーギー": ["corgi", "dog"],
    "鳥": ["bird"],
    "魚": ["fish"],
    # 自然
    "山": ["mountain"],
    "富士山": ["mountain", "fuji"],  # 富士山特有の説明は出ないかも
    "海": ["sea", "ocean", "beach"],
    "湖": ["lake"],
    "川": ["river"],
    "空": ["sky"],
    "雲": ["cloud"],
    "雪": ["snow"],
    "桜": ["cherry blossom", "sakura"],
    "梅": ["plum"],
    "紅葉": ["autumn", "fall foliage", "red leaves"],
    "花": ["flower", "blossom"],
    "木": ["tree"],
    # 乗り物
    "電車": ["train"],
    "新幹線": ["bullet train", "shinkansen", "train"],
    "車": ["car", "vehicle"],
    "バイク": ["motorcycle", "bike"],
    "自転車": ["bicycle", "bike"],
    "船": ["boat", "ship"],
    "飛行機": ["airplane", "plane"],
    # 食べ物
    "ご飯": ["rice", "meal", "food"],
    "ラーメン": ["ramen", "noodle"],
    "寿司": ["sushi"],
    "ケーキ": ["cake"],
    "果物": ["fruit"],
    # 建物
    "家": ["house", "home"],
    "建物": ["building"],
    "お寺": ["temple"],
    "神社": ["shrine"],
    "ビル": ["building", "skyscraper"],
    # 時間
    "夕暮れ": ["sunset", "dusk", "evening"],
    "朝": ["morning", "sunrise"],
    "夜": ["night"],
    # シーン
    "風景": ["landscape", "scenery"],
    "ポートレート": ["portrait", "person"],
    "人": ["person", "people", "man", "woman"],
    "テレビ": ["television", "tv"],
}

def log(msg):
    """ログ書き込み"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

def load_progress():
    if PROGRESS_PATH.exists():
        return json.load(open(PROGRESS_PATH))
    return {"processed_ids": [], "last_id": 0}

def save_progress(progress):
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False)

def load_captions():
    if CAPTION_DB_PATH.exists():
        return json.load(open(CAPTION_DB_PATH))
    return {}

def save_captions(captions):
    with open(CAPTION_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(captions, f, ensure_ascii=False, indent=1)

def main():
    log("=== Phase 3: AI画像キャプション開始 ===")
    
    # 写真DB読み込み
    db = json.load(open(DB_PATH))
    log(f"対象画像: {len(db)}枚")
    
    # 進捗復元
    progress = load_progress()
    captions = load_captions()
    log(f"既処理: {len(progress['processed_ids'])}枚")
    
    # モデルロード
    log("MLXモデルロード中...")
    from mlx_vlm import load, generate
    from mlx_vlm.prompt_utils import apply_chat_template
    
    MODEL = "mlx-community/SmolVLM-256M-Instruct-bf16"
    model, processor = load(MODEL)
    config = model.config
    log("モデルロード完了")
    
    # 残処理対象
    remaining = [x for x in db if x['id'] not in progress['processed_ids']]
    log(f"処理対象: {len(remaining)}枚")
    
    # 推定時間
    est_seconds = len(remaining) * 2.0
    est_hours = est_seconds / 3600
    log(f"推定時間: {est_hours:.1f}時間")
    
    start = time.time()
    processed_count = 0
    error_count = 0
    
    messages = [
        {"role": "user", "content": "Describe what is in this image in 1 sentence."}
    ]
    formatted_prompt = apply_chat_template(processor, config, messages, num_images=1)
    
    for entry in remaining:
        try:
            img_path = entry['path']
            if not Path(img_path).exists():
                error_count += 1
                continue
            
            # キャプション生成
            output = generate(
                model, processor, formatted_prompt, 
                image=img_path, max_tokens=60, verbose=False
            )
            
            # 結果整形
            caption = str(output).strip()
            # <end_of_utterance>等の除去
            caption = caption.replace('<end_of_utterance>', '').strip()
            
            captions[str(entry['id'])] = {
                "caption_en": caption,
                "path": img_path,
                "folder": entry['folder'],
                "filename": entry['filename'],
            }
            
            progress['processed_ids'].append(entry['id'])
            processed_count += 1
            
            # 定期保存
            if processed_count % SAVE_INTERVAL == 0:
                save_progress(progress)
                save_captions(captions)
                elapsed = time.time() - start
                rate = processed_count / elapsed if elapsed > 0 else 0
                remaining_count = len(remaining) - processed_count
                eta_min = (remaining_count / rate / 60) if rate > 0 else 0
                log(f"進捗 {processed_count}/{len(remaining)} ({rate:.1f}枚/秒) ETA: {eta_min:.1f}分")
        
        except Exception as e:
            error_count += 1
            log(f"エラー (id={entry.get('id')}): {str(e)[:100]}")
    
    # 最終保存
    save_progress(progress)
    save_captions(captions)
    
    elapsed = time.time() - start
    log(f"\n=== 完了 ===")
    log(f"処理: {processed_count}枚")
    log(f"エラー: {error_count}枚")
    log(f"所要時間: {elapsed/60:.1f}分")
    log(f"DB保存: {CAPTION_DB_PATH}")

if __name__ == "__main__":
    main()
