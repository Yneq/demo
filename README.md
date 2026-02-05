# TradeXchange AI Assessment / TradeXchange AI 評估作業

Build a web UI where users ask natural language questions about trade data, an LLM converts them to SQL, and results display.

建立一個網頁介面，讓使用者用自然語言詢問貿易數據問題，由 LLM 轉換成 SQL 查詢，並顯示結果。

## Database / 資料庫

Supabase (read-only / 唯讀):
- URL: `https://bqyrjnpwiwldppbkeafk.supabase.co`
- Anon key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxeXJqbnB3aXdsZHBwYmtlYWZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAyMzI0MDcsImV4cCI6MjA4NTgwODQwN30.JmzMN1xU_yhGzW4Ki_d6PpJqkTpVjDHA7dkyen4w6Rg`
- Table / 資料表: `countries_lpi` (id, country, region, lpi_score, year)

Note: The data contains some quality issues. / 注意：資料中包含一些品質問題。

## AI

OpenRouter key (shared, rate-limited / 共用，有額度限制): `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`

Use any model. Be efficient.

可使用任何模型，請節約使用。

## Requirements / 需求

Make these three queries work / 讓以下三個查詢能正常運作：

1. "Which countries in Asia have an LPI score above 3.0?" / 「亞洲有哪些國家的 LPI 分數高於 3.0？」
2. "What's the average LPI score by region?" / 「各區域的平均 LPI 分數是多少？」
3. "Show me the top 5 countries by logistics performance" / 「顯示物流表現前五名的國家」

## Submit / 繳交方式

- Fork this repo, build your solution / Fork 此 repo，建立你的解決方案
- Include a ~2 min screen recording demo (Loom, QuickTime, OBS, or any tool) / 附上約 2 分鐘的螢幕錄影示範（Loom、QuickTime、OBS 或任何工具皆可）
- Send your repo link + video to us on 104 within 48 hours of receiving this assignment / 收到此作業後 48 小時內，將 repo 連結與影片寄至 104

Any stack is fine. We're looking at: correctness, error handling, code clarity.

可使用任何技術棧。評估重點：正確性、錯誤處理、程式碼清晰度。

## Questions? / 有問題嗎？

If anything is unclear or you run into issues, reach out on 104. The OpenRouter key is shared across candidates — if it stops working, let us know.

如有任何不清楚或遇到問題，請聯繫 104。OpenRouter key 為所有應徵者共用，若無法使用請告知我們。
