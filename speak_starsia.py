#!/usr/bin/env python3
# スターシア（メイド長）音声スクリプト
# VOICEVOX 波音リツ（ノーマル）speaker=9
# 確定パラメーター: 2026-04-19
#
# 使い方:
#   python3 ~/.claude/speak_starsia.py
#   python3 ~/.claude/speak_starsia.py "任意のテキスト"

import urllib.request
import json
import subprocess
import sys

def speak(text=None):
    if text is None:
        text = "いらっしゃいませ。ようこそいらっしゃいました。"

    speaker = 9  # 波音リツ（ノーマル）

    req = urllib.request.Request(
        "http://localhost:50021/audio_query?text=" + urllib.request.quote(text) + "&speaker=" + str(speaker),
        method="POST"
    )
    with urllib.request.urlopen(req) as res:
        query = json.loads(res.read())

    # 確定パラメーター
    query["pitchScale"] = 0.01
    query["speedScale"] = 0.96
    query["intonationScale"] = 0.5

    # pause_mora（句読点ポーズ）を長めに
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
    text = sys.argv[1] if len(sys.argv) > 1 else None
    speak(text)
