"""
Test the three required queries.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.prompt import create_text_to_sql_prompt
from utils.llm import call_llm
from utils.database import execute_query


def test_query(question: str, query_name: str):
    """Test a single query."""
    print(f"\n{'='*60}")
    print(f"Testing: {query_name}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    try:
        # Generate SQL
        prompt = create_text_to_sql_prompt(question)
        sql_query = call_llm(prompt)
        
        if not sql_query:
            print("❌ Failed to generate SQL")
            return False
        
        print(f"\n📝 Generated SQL:\n{sql_query}\n")
        
        # Execute query
        results = execute_query(sql_query)
        
        if results is None:
            print("❌ Failed to execute query")
            return False
        
        if results.empty:
            print("⚠️  Query returned no results")
            return False
        
        print(f"✅ Success! Found {len(results)} results\n")
        print("First 5 rows:")
        print(results.head())
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all test queries."""
    
    queries = [
        ("Which countries in Asia have an LPI score above 3.0?", "Query 1 - Asia LPI > 3.0"),
        ("What's the average LPI score by region?", "Query 2 - Average by Region"),
        ("Show me the top 5 countries by logistics performance", "Query 3 - Top 5")
    ]
    
    results = []
    
    for question, name in queries:
        success = test_query(question, name)
        results.append((name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {passed}/{len(results)} passed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()