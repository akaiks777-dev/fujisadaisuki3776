#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 音声モード ON/OFF トグルスクリプト
# settings.json の UserPromptSubmit フックから呼び出す
# 2026-04-19

import sys
import os
import json

VOICE_ENABLED = os.path.expanduser("~/.claude/voice_enabled")
VOICE_MAIN_MODE = os.path.expanduser("~/.claude/voice_main_mode")

ON_KEYWORDS  = ["音声出して", "音出して", "声出して"]
OFF_KEYWORDS = ["終わった", "終わり", "音声止めて", "音止めて", "声止めて"]
MAIN_ON_KEYWORDS  = ["音声だけで", "音声メインで", "表示しないで", "表示なしで", "音声メインモード"]
MAIN_OFF_KEYWORDS = ["表示して", "通常モードで", "テキスト表示して", "音声メインオフ"]

def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")
    except Exception:
        prompt = ""

    # 音声メインモード
    if any(k in prompt for k in MAIN_ON_KEYWORDS):
        open(VOICE_MAIN_MODE, "w").close()
        open(VOICE_ENABLED, "w").close()
    elif any(k in prompt for k in MAIN_OFF_KEYWORDS):
        for f in [VOICE_MAIN_MODE]:
            if os.path.exists(f):
                os.remove(f)

    # 通常音声 ON/OFF
    if any(k in prompt for k in ON_KEYWORDS):
        open(VOICE_ENABLED, "w").close()
    elif any(k in prompt for k in OFF_KEYWORDS):
        for f in [VOICE_ENABLED, VOICE_MAIN_MODE]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    main()
