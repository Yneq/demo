"""
TradeXchange AI Assessment - Text-to-SQL Demo
Natural language interface for querying trade data.
"""

import streamlit as st
import pandas as pd
from utils.prompt import create_text_to_sql_prompt
from utils.llm import call_llm
from utils.database import execute_query

# Page config
st.set_page_config(
    page_title="TradeXchange AI - Text-to-SQL",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 TradeXchange AI - Text-to-SQL Demo")
st.markdown("""
Ask questions about **Logistics Performance Index (LPI)** data in natural language.
The AI will convert your question to SQL and display the results.

詢問關於**物流績效指數（LPI）**資料的問題，AI 會將您的問題轉換為 SQL 並顯示結果。
""")

# Sidebar with example queries
st.sidebar.header("📝 Example Queries / 範例查詢")
st.sidebar.markdown("""
1. Which countries in Asia have an LPI score above 3.0?
2. What's the average LPI score by region?
3. Show me the top 5 countries by logistics performance

**Database Schema / 資料庫結構：**
- Table: `countries_lpi`
- Columns: `id`, `country`, `region`, `lpi_score`, `year`
""")

# Example queries for quick testing
example_queries = {
    "Query 1 - Asia LPI > 3.0": "Which countries in Asia have an LPI score above 3.0?",
    "Query 2 - Average by Region": "What's the average LPI score by region?",
    "Query 3 - Top 5 Countries": "Show me the top 5 countries by logistics performance"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Test / 快速測試")
selected_example = st.sidebar.selectbox(
    "Select an example / 選擇範例：",
    ["Custom Query"] + list(example_queries.keys())
)

# Main input area
if selected_example == "Custom Query":
    user_question = st.text_area(
        "Enter your question / 輸入您的問題：",
        placeholder="e.g., Which countries have the highest LPI scores?",
        height=100
    )
else:
    user_question = st.text_area(
        "Enter your question / 輸入您的問題：",
        value=example_queries[selected_example],
        height=100
    )

# Query button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    query_button = st.button("🔍 Query / 查詢", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear / 清除", use_container_width=True)

if clear_button:
    st.rerun()

# Process query
if query_button and user_question:
    with st.spinner("🤖 Converting to SQL... / 正在轉換為 SQL..."):
        try:
            # Step 1: Convert to SQL using LLM
            prompt = create_text_to_sql_prompt(user_question)
            sql_query = call_llm(prompt)
            
            if not sql_query:
                st.error("❌ Failed to generate SQL query. Please try again.")
                st.error("❌ 無法生成 SQL 查詢，請重試。")
                st.stop()
            
            # Display generated SQL
            st.subheader("📝 Generated SQL / 生成的 SQL")
            st.code(sql_query, language="sql")
            
            # Step 2: Execute SQL query
            with st.spinner("⚡ Executing query... / 正在執行查詢..."):
                results = execute_query(sql_query)
                
                if results is None:
                    st.error("❌ Failed to execute query. Please check the SQL.")
                    st.error("❌ 查詢執行失敗，請檢查 SQL。")
                    st.stop()
                
                if results.empty:
                    st.warning("⚠️ Query returned no results.")
                    st.warning("⚠️ 查詢沒有返回結果。")
                else:
                    # Display results
                    st.subheader(f"📊 Results / 結果 ({len(results)} rows)")
                    
                    # Show dataframe
                    st.dataframe(
                        results,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Download button
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV / 下載 CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                    
                    # Success message
                    st.success(f"✅ Query executed successfully! Found {len(results)} results.")
                    st.success(f"✅ 查詢成功執行！找到 {len(results)} 筆結果。")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.error(f"❌ 錯誤：{str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>
    Built with Streamlit + OpenRouter + Supabase<br>
    TradeXchange AI Assessment | Vance
    </small>
</div>
""", unsafe_allow_h