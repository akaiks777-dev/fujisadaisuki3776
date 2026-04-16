#!/usr/bin/env python3
"""
Claude Code PreToolUse フック: セキュリティ重要ツールにタッチID認証を要求する
タッチID失敗時はPINコード（8桁）でフォールバック
認証成功 → allow / 認証失敗 → deny
"""
import json
import sys
import subprocess
import hashlib
import getpass

# PINコードのハッシュ（SHA-256）
PIN_HASH = "5a87600a0203232f5296c4ab504c690fc55770f3908e881fd03a543fb7883199"

# タッチID認証が必要なツール（denyリストに相当）
PROTECTED_TOOLS = {
    "mcp__computer-use__type",
    "mcp__computer-use__key",
    "mcp__computer-use__left_click",
    "mcp__computer-use__double_click",
    "mcp__computer-use__triple_click",
    "mcp__computer-use__right_click",
    "mcp__computer-use__middle_click",
    "mcp__computer-use__left_click_drag",
    "mcp__computer-use__left_mouse_down",
    "mcp__computer-use__left_mouse_up",
    "mcp__computer-use__mouse_move",
    "mcp__computer-use__scroll",
    "mcp__computer-use__computer_batch",
    "mcp__computer-use__hold_key",
    "mcp__computer-use__request_access",
    "mcp__computer-use__open_application",
}

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

    tool_name = hook_data.get("tool_name", "")

    # 保護対象ツールでなければスキップ（通常の許可フローへ）
    if tool_name not in PROTECTED_TOOLS:
        return

    authenticated = False

    # 1. まずタッチID認証を試行
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

    if authenticated:
        output = {
            "decision": "allow"
        }
    else:
        output = {
            "decision": "deny",
            "reason": "認証に失敗しました。マスター本人のみ操作可能です。"
        }

    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
