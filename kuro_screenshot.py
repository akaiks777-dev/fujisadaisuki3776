#!/usr/bin/env python3
import json, sys, subprocess

try:
    data = json.load(sys.stdin)
    prompt = data.get('prompt', '')
    if prompt.strip() == 'はる':
        import os
        path1 = '/tmp/kuro_screenshot_1.png'
        path2 = '/tmp/kuro_screenshot_2.png'
        # 複数ファイル名を渡すと各ディスプレイが別ファイルに保存される
        subprocess.run(['screencapture', '-x', path1, path2], check=True)
        if os.path.exists(path2):
            context = f'ユーザーが「はる」と入力しました。左画面を {path1}、右画面を {path2} に保存しました。必ずReadツールで両方のファイルを読み込んで、左右の画像を表示してください。'
        else:
            context = f'ユーザーが「はる」と入力しました。スクリーンショットを {path1} に保存しました。必ずReadツールで {path1} を読み込んで、画像を表示してください。'
        result = {
            'hookSpecificOutput': {
                'hookEventName': 'UserPromptSubmit',
                'additionalContext': context
            }
        }
        print(json.dumps(result, ensure_ascii=False))
except Exception:
    pass
