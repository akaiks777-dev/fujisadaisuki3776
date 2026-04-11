---
name: moneyforward-monthly-report
description: 毎月5日にマネーフォワード家計簿データを整理・分析レポートを更新する
---

毎月5日の定期タスクです。以下の手順でマネーフォワード家計簿データを整理・分析してください。

## 手順

### 1. 先月のCSVダウンロードを促す通知
ユーザーに以下のメッセージを表示してください：

「📊 【毎月5日の家計簿整理タスク】

先月分のマネーフォワードCSVをダウンロードして ~/Downloads/マネーフォワード家計簿データ/ に保存してください。

手順：
1. https://ssnb.x.moneyforward.com/cf を開く
2. 「収支内訳」タブ → 先月を選択
3. ページ下部「ダウンロード」ボタン
4. 保存先：~/Downloads/マネーフォワード家計簿データ/

ダウンロードが完了したら「完了」と入力してください。」

### 2. ユーザーが完了と入力したら
~/Downloads/マネーフォワード家計簿データ/ フォルダ内の全CSVファイルを読み込んで、以下のPythonスクリプトを実行して家計簿分析レポートを更新してください：

```python
import os, csv, glob
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

data_dir = os.path.expanduser("~/Downloads/マネーフォワード家計簿データ")
pattern = os.path.join(data_dir, "収入・支出詳細_????-??-??_????-??-??.csv")
files = sorted(glob.glob(pattern))

monthly = defaultdict(lambda: {'income': 0, 'expense': 0, 'categories': defaultdict(float)})
seen = set()

for f in files:
    base = os.path.basename(f)
    key = base[:25]
    if key in seen:
        continue
    seen.add(key)
    for enc in ['shift_jis', 'cp932', 'utf-8']:
        try:
            with open(f, encoding=enc) as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    if row.get('計算対象') != '1':
                        continue
                    try:
                        amount = float(row['金額（円）'])
                        month = row['日付'][:7].replace('/', '-')
                        category = row.get('大項目', 'その他') or 'その他'
                        if amount > 0:
                            monthly[month]['income'] += amount
                        else:
                            monthly[month]['expense'] += abs(amount)
                            monthly[month]['categories'][category] += abs(amount)
                    except:
                        pass
            break
        except:
            continue

months = sorted(monthly.keys())
yearly = defaultdict(lambda: {'income': 0, 'expense': 0})
for m in months:
    y = m[:4]
    yearly[y]['income'] += monthly[m]['income']
    yearly[y]['expense'] += monthly[m]['expense']

cat_totals = defaultdict(float)
for m in months:
    for cat, amt in monthly[m]['categories'].items():
        cat_totals[cat] += amt
cat_sorted = sorted(cat_totals.items(), key=lambda x: -x[1])

# Excelファイル作成（省略 - 既存のスクリプトと同じ）
print(f"✅ {len(months)}ヶ月分のデータを処理しました")
print(f"期間: {months[0]} ～ {months[-1]}")
```

### 3. 完了報告
分析レポートを ~/Downloads/マネーフォワード家計簿データ/家計簿分析レポート.xlsx に更新して、以下を報告してください：
- 処理した月数
- 最新月の収入・支出・収支
- 前月比較
- 今年の年間収支（現時点）
