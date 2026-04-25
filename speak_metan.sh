#!/bin/bash
# speak_metan.sh - VOICEVOX四国めたんで読み上げ
# 使用法: echo "テキスト" | ./speak_metan.sh
#        または: ./speak_metan.sh "テキスト"

# 設定
VOICEVOX_HOST="http://localhost:50021"
SPEAKER_ID=2  # 四国めたん ノーマル
TMP_WAV="/tmp/metan_$$.wav"

# 引数 or 標準入力からテキスト取得
if [ -n "$1" ]; then
    TEXT="$1"
else
    TEXT=$(cat)
fi

# 空ならスキップ
if [ -z "$TEXT" ]; then
    exit 0
fi

# 絵文字・マークダウン記号・時刻表示を削除（読み上げをシンプルに）
CLEAN_TEXT=$(echo "$TEXT" | sed -E '
    s/【🕐[^】]*】//g;
    s/[🎯🎧✅❌⏸▶📋💰⚠️💡❓🆓🤖💳⏱️🟢🟡🔴📝🎙️🎵🔧🌟]//g;
    s/`[^`]*`//g;
    s/\*\*([^*]+)\*\*/\1/g;
    s/\*([^*]+)\*/\1/g;
    s/#+\s*//g;
    s/^\s*-\s*//g;
    s/https?:\/\/[^ ]*//g;
    s/\|[^|]*\|/ /g;
' | tr -s '\n' ' ')

# VOICEVOXエンジンが起動しているか確認
if ! curl -s --max-time 2 "${VOICEVOX_HOST}/version" > /dev/null; then
    exit 0
fi

# 長文を文単位で分割してチャンク化（1チャンク最大400文字）
CHUNKS=$(echo "$CLEAN_TEXT" | python3 -c "
import sys, re
text = sys.stdin.read().strip()
if not text:
    sys.exit(0)
# 句点・感嘆・疑問で分割
sentences = re.split(r'(?<=[。！？\.])', text)
chunks = []
current = ''
MAX = 400
for s in sentences:
    if len(current) + len(s) > MAX and current:
        chunks.append(current)
        current = s
    else:
        current += s
if current.strip():
    chunks.append(current)
for c in chunks:
    c = c.strip()
    if c:
        print(c)
")

# 各チャンクを順次合成・再生
IFS=$'\n'
for CHUNK in $CHUNKS; do
    [ -z "$CHUNK" ] && continue

    # audio_query
    QUERY=$(curl -s -X POST \
        "${VOICEVOX_HOST}/audio_query?speaker=${SPEAKER_ID}" \
        --get --data-urlencode "text=${CHUNK}" \
        --max-time 10)
    [ -z "$QUERY" ] && continue

    # パラメータ調整
    QUERY=$(echo "$QUERY" | python3 -c "
import sys, json
q = json.load(sys.stdin)
q['speedScale'] = 1.0
q['intonationScale'] = 0.7
q['pitchScale'] = -0.05
q['volumeScale'] = 1.0
print(json.dumps(q, ensure_ascii=False))
")

    # synthesis
    CHUNK_WAV="/tmp/metan_$$_$(date +%N).wav"
    curl -s -X POST \
        "${VOICEVOX_HOST}/synthesis?speaker=${SPEAKER_ID}" \
        -H "Content-Type: application/json" \
        -d "${QUERY}" \
        --max-time 60 \
        --output "${CHUNK_WAV}"

    # 再生（フォアグラウンドで完了待ち）
    if [ -f "${CHUNK_WAV}" ] && [ -s "${CHUNK_WAV}" ]; then
        afplay "${CHUNK_WAV}" 2>/dev/null
        rm -f "${CHUNK_WAV}"
    fi
done
