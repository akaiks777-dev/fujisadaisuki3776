#!/usr/bin/env python3
"""
UserPromptSubmitフック: 「はい」と入力した時にタッチID認証を要求する
認証成功 → そのまま「はい」を送信
認証失敗 → 入力をブロック（空文字に置換）
"""
import json
import sys
import subprocess
import hashlib
import getpass

# PINコードのハッシュ（SHA-256）
PIN_HASH = "5a87600a0203232f5296c4ab504c690fc55770f3908e881fd03a543fb7883199"

# タッチID認証が必要なキーワード（スペースのみ・空文字含む）
CONFIRM_WORDS = {"はい", "yes", "Yes", "YES", "ok", "OK", "Ok", "y", "Y", "3"}

def verify_pin():
    """PINコード入力による認証（回数制限なし）"""
    while True:
        try:
            pin = getpass.getpass("PIN(8桁)を入力: ")
            pin_hash = hashlib.sha256(pin.encode()).hexdigest()
            if pin_hash == PIN_HASH:
                return True
            print("PINが違います。", file=sys.stderr)
        except (EOFError, KeyboardInterrupt):
            return False

def main():
    try:
        hook_data = json.loads(sys.stdin.read())
    except Exception:
        return

    prompt = hook_data.get("prompt", "").strip()

    # 確認キーワードでなければスキップ
    if prompt not in CONFIRM_WORDS:
        return

    authenticated = False

    # 1. タッチID認証を試行
    try:
        result = subprocess.run(
            ["/Users/shigesan/.claude/touchid_auth"],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            authenticated = True
    except Exception:
        pass

    # 2. タッチID失敗時はPINコードでフォールバック
    if not authenticated:
        print("Touch IDが使えません。PINコードで認証します。", file=sys.stderr)
        authenticated = verify_pin()

    if not authenticated:
        # 認証失敗 → 入力をブロック
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "rejectPrompt": True,
                "additionalContext": "認証に失敗しました。マスター本人のみ操作可能です。"
            }
        }
        print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
