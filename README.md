# TradeXchange AI Assessment - Text-to-SQL Demo

Natural language interface for querying Logistics Performance Index (LPI) trade data.

自然語言介面，用於查詢物流績效指數（LPI）貿易數據。

---

## 🎯 Solution Overview / 解決方案概述

This solution provides a **web-based Text-to-SQL system** that:
1. Accepts natural language questions about trade data
2. Uses an LLM (via OpenRouter) to convert questions to SQL
3. Executes queries against a Supabase database
4. Displays results with data quality handling and error management

此解決方案提供基於網頁的 **Text-to-SQL 系統**：
1. 接受關於貿易數據的自然語言問題
2. 使用 LLM（透過 OpenRouter）將問題轉換為 SQL
3. 對 Supabase 資料庫執行查詢
4. 顯示結果，並處理資料品質問題與錯誤管理

---

## 🏗️ Tech Stack / 技術棧

- **Frontend**: Streamlit (Python-based web UI)
- **LLM Integration**: OpenRouter API (Claude 3.5 Sonnet)
- **Database**: Supabase (PostgreSQL)
- **Data Processing**: Pandas
- **HTTP Client**: Requests

---

## 📊 Database Schema / 資料庫結構

**Table**: `countries_lpi`

| Column | Type | Description |
|--------|------|-------------|
| `id` | integer | Primary key |
| `country` | text | Country name |
| `region` | text | Geographic region |
| `lpi_score` | numeric | Logistics Performance Index (1.0-5.0) |
| `year` | integer | Year of data |

**Connection Details**:
- URL: `https://bqyrjnpwiwldppbkeafk.supabase.co`
- Access: Read-only (Anon key provided separately)

---

##  Quick Start / 快速開始

### Prerequisites / 先決條件

- Python 3.12+
- Git

### Installation / 安裝
```bash
# 1. Clone the repository
git clone https://github.com/Yneq/demo.git
cd demo

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create .env file with:
# OPENROUTER_API_KEY=your_openrouter_key
# SUPABASE_URL=https://bqyrjnpwiwldppbkeafk.supabase.co
# SUPABASE_KEY=your_supabase_anon_key
```

### Running the Application / 執行應用程式
```bash
# Start Streamlit app
streamlit run app.py

# Open browser at http://localhost:8501
```

### Running Tests / 執行測試
```bash
# Test all three required queries
python tests/test_queries.py
```

---

## ✅ Required Queries Implementation / 必要查詢實作

All three required queries are fully implemented and tested:

### Query 1: Asia Countries with LPI > 3.0
**Question**: "Which countries in Asia have an LPI score above 3.0?"

**Generated SQL**:
```sql
SELECT DISTINCT country, lpi_score, year 
FROM countries_lpi 
WHERE region LIKE '%Asia%' 
AND lpi_score > 3.0 
AND lpi_score IS NOT NULL 
ORDER BY lpi_score DESC;
```

**Result**: Returns Asian countries with scores above 3.0, sorted by performance.

---

### Query 2: Average LPI by Region
**Question**: "What's the average LPI score by region?"

**Generated SQL**:
```sql
SELECT region, ROUND(AVG(lpi_score)::numeric, 2) as avg_lpi_score 
FROM countries_lpi 
WHERE lpi_score IS NOT NULL 
GROUP BY region 
ORDER BY avg_lpi_score DESC;
```

**Result**: Calculates and displays average scores grouped by region.

---

### Query 3: Top 5 Countries
**Question**: "Show me the top 5 countries by logistics performance"

**Generated SQL**:
```sql
SELECT DISTINCT country, MAX(lpi_score) as max_lpi_score 
FROM countries_lpi 
WHERE lpi_score IS NOT NULL 
GROUP BY country 
ORDER BY max_lpi_score DESC 
LIMIT 5;
```

**Result**: Returns top 5 performing countries.

---

## 🔧 Key Features / 核心功能

### 1. Data Quality Handling / 資料品質處理

The database contains quality issues as mentioned in the requirements. Our solution handles:

**Problem**: Inconsistent data types
- Text values: `"three point six"` → should be `3.6`
- Numeric values: `3.60`, `4.30` (already correct)
- Case inconsistencies: `"SINGAPORE"` vs `"Singapore"`

**Solution**: Robust data cleaning pipeline
```python
# Converts text numbers to numeric
"three point six" → 3.6
"four point seven" → 4.7

# Standardizes case
"SINGAPORE" → "Singapore"
"asia" → "Asia"

# Ensures numeric type
All lpi_score values converted to float
```

### 2. Error Handling / 錯誤處理

Comprehensive error handling for:
- ✅ LLM API failures (timeout, rate limits)
- ✅ Database connection issues
- ✅ Invalid SQL generation
- ✅ Empty query results
- ✅ Data type conversion errors

### 3. User Interface / 使用者介面

- 🌐 Bilingual (English/Chinese)
- 📝 Example queries for quick testing
- 📊 Interactive result tables
- 📥 CSV download functionality
- 🎨 Clean, professional design

---

## 🏛️ Project Structure / 專案結構
```
demo/
├── app.py                      # Streamlit main application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── utils/
│   ├── __init__.py
│   ├── prompt.py              # LLM prompt engineering
│   ├── llm.py                 # OpenRouter API integration
│   └── database.py            # Supabase query execution
└── tests/
    └── test_queries.py        # Automated query testing
```

---

## 🎥 Demo Video / 示範影片

**Video Link**: [Insert your video link here]

**Duration**: ~2 minutes

**Contents**:
- Introduction
- Query 1 demonstration
- Query 2 demonstration
- Query 3 demonstration
- Error handling showcase

---

## 💡 Technical Highlights / 技術亮點

### 1. Prompt Engineering
Carefully crafted system prompts with:
- Database schema description
- SQL syntax guidelines
- Few-shot examples
- Data quality warnings

### 2. Data Cleaning Pipeline
```python
def parse_lpi_score(value):
    """
    Handles multiple data formats:
    - Numeric: 4.30 → 4.30
    - Text: "three point six" → 3.6
    - Invalid: None → None
    """
    # Improved logic with unified number mapping
    text_to_num = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3,
        'four': 4, 'five': 5, 'six': 6, 'seven': 7,
        'eight': 8, 'nine': 9
    }
    
    # "three point six" → 3 + 0.6 = 3.6
    whole_val = text_to_num.get(whole_str, 0)
    decimal_val = text_to_num.get(decimal_str, 0) * 0.1
    return float(whole_val + decimal_val)
```

### 3. Fallback Strategy
Since Supabase Python SDK had version conflicts, implemented direct REST API calls:
- More reliable
- Better error handling
- Clearer code flow

---

## 🧪 Testing / 測試

All three required queries pass automated tests:
```bash
(.venv) $ python tests/test_queries.py

============================================================
Testing: Query 1 - Asia LPI > 3.0
✅ Success! Found 14 results

============================================================
Testing: Query 2 - Average by Region
✅ Success! Found 8 results

============================================================
Testing: Query 3 - Top 5
✅ Success! Found 5 results

============================================================
SUMMARY
============================================================
✅ PASS - Query 1 - Asia LPI > 3.0
✅ PASS - Query 2 - Average by Region
✅ PASS - Query 3 - Top 5

Total: 3/3 passed
============================================================
```

---

## 🔒 Security / 安全性

- ✅ API keys stored in `.env` (not committed to git)
- ✅ Read-only database access
- ✅ Input sanitization via LLM
- ✅ No SQL injection risk (queries generated by AI, not concatenated)

---

## ⚙️ Configuration / 設定

### Environment Variables

Create a `.env` file in the project root:
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
SUPABASE_URL=https://bqyrjnpwiwldppbkeafk.supabase.co
SUPABASE_KEY=xxxxxxxxxxxxx...
```

### Model Selection

Default model: `anthropic/claude-3.5-sonnet`

To change models, edit `utils/llm.py`:
```python
def call_llm(prompt: str, model: str = "google/gemini-2.0-flash-exp:free"):
    # Switch to Gemini (free tier)
```

Available models: https://openrouter.ai/models

---

## 🐛 Troubleshooting / 疑難排解

### Issue: "Client.__init__() got an unexpected keyword argument 'proxy'"
**Solution**: Use the provided `requirements.txt` which specifies compatible versions:
```txt
supabase==2.9.0
postgrest>=0.17.0, <0.18.0
```

### Issue: Empty results or type errors
**Solution**: The `clean_data()` function handles this automatically. Ensure it's called before query execution.

### Issue: LLM not generating correct SQL
**Solution**: Check the prompt in `utils/prompt.py`. Ensure examples match your query pattern.

---

## 📈 Future Improvements / 未來改進

If given more time, I would add:

1. **Caching**: Cache LLM responses to reduce API costs
2. **Query History**: Store previous queries in session state
3. **Advanced Filters**: More complex query building
4. **Visualization**: Charts and graphs for results
5. **Multi-language Support**: Extended language support beyond EN/ZH

---

## 📝 Development Notes / 開發筆記

### Challenges Encountered / 遇到的挑戰

1. **Supabase SDK Version Conflict**
   - Issue: `supabase-py` had breaking changes
   - Solution: Switched to direct REST API calls

2. **Data Quality Issues**
   - Issue: Mixed data types (`"three point six"` vs `4.30`)
   - Solution: Robust parsing with text-to-number conversion

3. **SQL Generation Reliability**
   - Issue: LLM sometimes adds markdown formatting
   - Solution: Strip code blocks before execution

### Time Spent / 耗時

- Planning & Setup: 30 min
- Core Implementation: 2 hours
- Testing & Refinement: 1 hour
- Documentation & Video: 30 min
- **Total**: ~4 hours

---

## 👨‍💻 Author / 作者

**Vance**
- GitHub: [@Yneq](https://github.com/Yneq)
- Repository: [demo](https://github.com/Yneq/demo)

---

## 📄 License / 授權

This project is created for the TradeXchange AI assessment.

此專案為 TradeXchange AI 評估作業所建立。

---

## 🙏 Acknowledgments / 致謝

- OpenRouter for LLM API access
- Supabase for database hosting
- Streamlit for rapid UI development

---


*Last Updated: February 2026*