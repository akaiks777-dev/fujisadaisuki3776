#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# スターシア 音声読み上げスクリプト（voice_script.txt から読み上げ）
# 使い方: python3 ~/.claude/speak_last_response.py

import urllib.request
import json
import subprocess
import os

VOICE_SCRIPT_PATH = os.path.expanduser("~/.claude/voice_script.txt")

def speak_file():
    if not os.path.exists(VOICE_SCRIPT_PATH):
        print("voice_script.txt が見つかりません")
        return

    with open(VOICE_SCRIPT_PATH, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("読み上げるテキストがありません")
        return

    speaker = 20  # もち子さん（ノーマル）

    req = urllib.request.Request(
        "http://localhost:50021/audio_query?text=" + urllib.request.quote(text) + "&speaker=" + str(speaker),
        method="POST"
    )
    with urllib.request.urlopen(req) as res:
        query = json.loads(res.read())

    # 確定パラメーター
    query["pitchScale"] = 0.01
    query["speedScale"] = 1.1
    query["intonationScale"] = 0.5

    for ap in query["accent_phrases"]:
        if ap.get("pause_mora"):
            ap["pause_mora"]["vowel_length"] = 0.8

    req2 = urllib.request.Request(
        "http://localhost:50021/synthesis?speaker=" + str(speaker),
        data=json.dumps(query).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req2) as res:
        wav_data = res.read()

    with open("/tmp/starsia_speak.wav", "wb") as f:
        f.write(wav_data)

    subprocess.run(["afplay", "/tmp/starsia_speak.wav"])

if __name__ == "__main__":
    speak_file()
