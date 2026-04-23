---
name: gmail-archive-starred
description: Gmail週次自動整理（月曜9:17）：ヤマト配達・Amazon通知（1週間超）削除、スター付き3ヶ月→重要保管、1年以上前の請求・3年以上前のAmex削除
---

Gmailの月次自動整理タスク。毎月1日に実行して以下の処理を行う：

## 処理1：スター付き3ヶ月経過 → 重要保管ラベルへ移動
1. Chromeで `https://mail.google.com/mail/u/0/#search/is%3Astarred+older_than%3A3m+-label%3A%E9%87%8D%E8%A6%81%E4%BF%9D%E7%AE%A1` を開く
2. 該当メールがあれば：全選択 → ラベル付け「重要保管」→ アーカイブ

## 処理2：1週間以上前の配達・発送通知を削除
- `from:"ヤマト運輸" older_than:7d -is:starred`
- `from:"auto-confirm@amazon.co.jp" older_than:7d -is:starred`
- `from:"shipment-tracking@amazon.co.jp" older_than:7d -is:starred`

## 処理3：3ヶ月以上前の自動通知を削除
- `from:"SBI証券" older_than:3m -is:starred`
- `from:"住信SBIネット銀行" older_than:3m -is:starred`
- `from:"JRE BANK" older_than:3m -is:starred`
- `from:"no-reply@accounts.google.com" older_than:3m -is:starred`
- `from:"1Password" older_than:3m -is:starred`
- `from:"Steam" older_than:3m -is:starred`

## 処理4：1年以上前の請求書類を削除
- `from:"アットユーネット" older_than:1y -is:starred`
- `from:"@nifty" older_than:1y -is:starred`
- `from:"楽天銀行" older_than:1y -is:starred`
- `from:"セゾンカード" older_than:1y -is:starred`
- `from:"SAISON ID" older_than:1y -is:starred`

## 処理5：3年以上前のAmerican Express請求を削除
- `from:"American Express" older_than:3y -is:starred`

## 処理6：宣伝・広告系は即削除
- `from:"リベシティ運営" subject:"未読通知"`
- `from:"Gusto Japan"`
- `from:"povo"`
- `from:"Qoo10"`
- `from:"Amazon Marketplace"`
- `from:"Amazon定期おトク便"`
- `from:"マネーフォワードクラウド"`
- `from:"株式会社ビューカード" -subject:"【重要】" -subject:"利用明細"`
- `from:"出光カード" -subject:"ご利用明細"`
- `from:"ETCマイレージ"`

## 実行方法
各検索URLをChromeで開き、以下のJavaScriptで一括削除：
```javascript
function rc(el){const r=el.getBoundingClientRect();['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(new MouseEvent(t,{view:window,bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5,button:0})));}
async function run(){
  const cb=document.querySelectorAll('div[role="main"] span[role="checkbox"]')[0];
  if(!cb)return'empty';
  rc(cb); await new Promise(r=>setTimeout(r,1200));
  const tb=Array.from(document.querySelectorAll('div[role="button"]')).find(b=>(b.getAttribute('data-tooltip')||'')==='削除');
  rc(tb); await new Promise(r=>setTimeout(r,3000));
  return document.querySelectorAll('div[role="main"] tr.zA').length;
}
```
emptyになるまで繰り返す。座標クリック代替：チェックボックス(234,117) → 削除ボタン(350,117)

## 注意事項
- **スター付きは絶対に削除しない**（すべての検索に `-is:starred` を含める）
- 削除はすべて「ゴミ箱へ移動」（30日以内は復元可）
- 処理後にマスターに件数レポートを提出