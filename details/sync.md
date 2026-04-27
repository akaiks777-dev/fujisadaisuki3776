# 同期コマンド詳細

## 仕組み（2026-04-23 新設計）
ラッパースクリプトが `hostname` を自動判定し、正しい方向で同期：

| コマンド | 本店で実行 | 支店で実行 |
|---|---|---|
| `本店から支店` | 本店→iCloud（push） | iCloud→支店（pull） |
| `支店から本店` | iCloud→本店（pull） | 支店→iCloud（push） |

## 安全機能（3段階）
1. hostname自動判定
2. push前の新旧チェック
3. 自動スナップショット

## 同期対象
`CLAUDE.md` / `settings.json` / `kuro_screenshot.py` / `relay_notes.md` / `rollback.sh` / `plugins/` / `scheduled-tasks/` / `projects/` / `history.jsonl` / Espanso設定 / 同期スクリプト / LaunchAgents

## スクリプトの場所
- ラッパー（推奨）: `iCloud Drive/ClaudeCode_Sync/sync_honten_to_shiten.sh` / `sync_shiten_to_honten.sh`
- 内部実装（直接使用禁止）: `sync_from_local.sh` / `sync_to_local.sh`

## 2026-04-23 事故の教訓
旧スクリプトは「本店視点」で書かれており、支店で実行すると逆方向に動作→本店成果物を消去する事故が発生。新設計でhostname判定により解決。
