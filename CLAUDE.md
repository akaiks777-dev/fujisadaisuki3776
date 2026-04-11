# Claude個人設定

## 言語
常に日本語で回答する。
会話のタイトル・要約を生成する際も必ず日本語で記述する。

## リベシティ図書館 自動検索

以下のキーワードや話題が出たときは、**自動的に** `https://library.libecity.com/search?keyword=[キーワード]` を検索して回答に活用する：

- リベシティ / ノウハウ図書館 に関する質問
- Claude Code / Claude Cowork の使い方・活用事例
- ITリテラシー・AI活用に関する質問
- 副業・投資・家計管理などの実践ノウハウ
- 「どうやって使うか」「活用事例」「便利な使い方」などの質問

### 検索URL形式
[https://library.libecity.com/search?keyword=検索キーワード](https://library.libecity.com/search?keyword=検索キーワード)

### 自動検索の手順
1. ユーザーの質問からキーワードを抽出
2. 上記URLで検索
3. 上位の記事タイトルと内容を参考に回答
4. 参照した記事があれば回答末尾にURLを記載

## ユーザー情報
- 使用機器: Mac mini M4 Pro (48GB RAM / 1TB SSD)
- モニター: Dell U2723QX × 2台（4K）
- 外付けHDD: Buffalo 4TB（バックアップハードディスク1TB / Drive_Rest 1TB / 動画2TB）
- ブラウザ: Google Chrome

## テキスト表示ルール
回答中に以下のものを記載する際は、指定の形式で表示する：

- URL（クリッカブルなMarkdownリンク形式：`[URL](URL)` ）→ クリックしてブラウザで開けるようにする
- ファイル名・ファイルパス（インラインコード `）
- コマンド・コード（インラインコード `）
- アルファベットの技術用語・固有名詞（インラインコード `）
- 数字のみの値・バージョン番号など（インラインコード `）

例：
[https://example.com](https://example.com)
ファイル名：`CLAUDE.md`　コマンド：`npm install`　バージョン：`v1.2.3`

## 注意事項
- リベシティのノウハウ図書館はログインが必要なため、WebFetchでは本文が取得できない場合がある
- その場合はChrome経由で検索結果を案内する

## 「はる」スクリーンショット機能（重要・削除禁止）

ユーザーが `はる` とだけ入力すると、自動でスクリーンショットを撮影してClaudeに見せる機能。

### 仕組み
- `settings.json` の `UserPromptSubmit` フックで `~/.claude/kuro_screenshot.py` を実行
- `kuro_screenshot.py` がプロンプトを監視し、`はる` の場合に `screencapture` でスクリーンショットを `/tmp/kuro_screenshot.png` に保存
- フックが `additionalContext` でClaudeに画像読み込みを指示
- ClaudeはReadツールで `/tmp/kuro_screenshot.png` を読み込んで表示する

### 必須ファイル
- `~/.claude/settings.json` — `UserPromptSubmit` フックに `python3 ~/.claude/kuro_screenshot.py` の記述が必要
- `~/.claude/kuro_screenshot.py` — スクリーンショット撮影スクリプト
- `iCloud: ClaudeCode_Sync/settings.json` — 同じ内容をiCloudにも保存

### settings.json が壊れたら
`iCloud Drive/ClaudeCode_Sync/sync_to_local.sh` を実行して復元する。

## 「同期」コマンド（重要・削除禁止）

### 「同期」= アップロード（Mac mini → iCloud → MacBook Air）
ユーザーが `同期` とだけ入力したら、**確認なしで即座に**実行する。
```
bash "$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeCode_Sync/sync_from_local.sh"
```

### 「同期下」= ダウンロード（MacBook Air → iCloud → Mac mini）
ユーザーが `同期下` と入力したら、**確認なしで即座に**実行する。
```
bash "$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeCode_Sync/sync_to_local.sh"
```

### 仕組み
- `同期`：`Mac mini` → `iCloud` → `MacBook Air`（Mac miniの内容をアップロード）
- `同期下`：`MacBook Air` → `iCloud` → `Mac mini`（MacBook Airで変更した内容をMac miniに取り込む）
- 同期対象：`CLAUDE.md`、`settings.json`、`kuro_screenshot.py`、`plugins/`、`scheduled-tasks/`、`projects/`（チャット履歴）、`history.jsonl`、`Espanso`設定、同期スクリプト、`LaunchAgents`

### 目的
- `Mac mini` と `MacBook Air` の間で `Claude Code` / `Claude Cowork` のチャット履歴・設定・セッションをすべて共有する
- 新しいセッションが増えても自動的に同期対象に含まれる

### スクリプトの場所
- アップロード（`Mac mini` → `iCloud`）：`iCloud Drive/ClaudeCode_Sync/sync_from_local.sh`
- ダウンロード（`iCloud` → `Mac mini`）：`iCloud Drive/ClaudeCode_Sync/sync_to_local.sh`

## 引き継ぎメモ（2026-04-10）

### 完了済み
1. **Apple ID の表示確認・修正済み** — `Mac mini` のApple ID表示を確認し、ファイル修正完了
2. **Stopフック拡張** — `settings.json` のStopフックを更新。セッション終了時にデスクトップの `.png` ファイルすべて（`Claude Cowork` でコピペした画像含む）をゴミ箱に移動 + `/tmp/kuro_screenshot.png` もクリーンアップ
3. **`CLAUDE.md` の同期コマンド表記修正**（4/9）— 矢印表記を `Mac mini` → `iCloud` → `MacBook Air` に統一
4. **同期済み** — 上記変更を `iCloud` にアップロード完了
5. **セッションタイトル日本語化（4/10）** — `Claude Code` のサイドバーに表示されるセッションタイトルが英語になる問題を解決
   - 原因：セッションの `summary` フィールドが未設定の場合、`Claude Code` が英語でタイトルを自動生成していた
   - 対策①：`~/.claude/add_japanese_summaries.py` を作成。既存28件のセッションに日本語タイトルを一括追加済み
   - 対策②：`settings.json` のStopフックに `add_japanese_summaries.py` を追加。今後は**セッション終了のたびに自動で日本語タイトルが付く**
   - タイトルの内容：最初のユーザーメッセージ先頭25文字を使用
