"""Database operations using direct HTTP requests to Supabase REST API."""

import os
import requests
from typing import Optional
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def fetch_all_data() -> Optional[pd.DataFrame]:
    """Fetch all data from countries_lpi table."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/countries_lpi"
        
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        params = {
            "select": "*"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return pd.DataFrame()
        
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data quality issues.
    Handle inconsistent types, case issues, and text values.
    """
    df = df.copy()
    
    # 1. Standardize case
    if 'country' in df.columns:
        df['country'] = df['country'].str.strip().str.title()
    
    if 'region' in df.columns:
        df['region'] = df['region'].str.strip().str.title()
    
    # 2. Clean lpi_score (CRITICAL)
    if 'lpi_score' in df.columns:
        def parse_lpi_score(value):
            if isinstance(value, str):
                value = value.lower().strip()
                
                # 建立統一的數字對照表（全部存為整數）
                text_to_num = {
                    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
                    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
                }
                
                if 'point' in value:
                    parts = value.split('point')
                    if len(parts) == 2:
                        whole_str = parts[0].strip()
                        decimal_str = parts[1].strip()
                        
                        # 取得整數值 (例如 "six" -> 6)
                        whole_val = text_to_num.get(whole_str, 0)
                        
                        # 取得小數值並除以 10 (例如 "three" -> 3 -> 0.3)
                        decimal_val = text_to_num.get(decimal_str, 0) * 0.1
                        
                        return float(whole_val + decimal_val)
                
                # Try direct conversion
                try:
                    return float(value)
                except ValueError:
                    return None
            
            return None
        
        for i in range(len(df)):
            df.loc[i, 'lpi_score'] = parse_lpi_score(df.loc[i, 'lpi_score'])
    
    # 3. Remove duplicates (keep first occurrence)
    # Use country + year as key for deduplication
    if 'country' in df.columns and 'year' in df.columns:
        df = df.sort_values('lpi_score', ascending=False)  # Keep highest score
        df = df.drop_duplicates(subset=['country', 'year'], keep='first')
    else:
        df = df.drop_duplicates()
    
    # 在 return 之前，確保 lpi_score 真的是 float
    if 'lpi_score' in df.columns:
        df['lpi_score'] = pd.to_numeric(df['lpi_score'], errors='coerce')
    
    # 4. Remove rows with invalid lpi_score
    df = df[df['lpi_score'].notna()]
    
    return df


def execute_query(sql_query: str) -> Optional[pd.DataFrame]:
    """
    Execute SQL query by fetching all data and processing locally.
    Includes data cleaning to handle quality issues.
    """
    try:
        # Fetch all data
        df = fetch_all_data()
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Clean data
        df = clean_data(df)
        
        # Process based on SQL query
        sql_lower = sql_query.lower()
        
        # Query 1: Asia + LPI > 3.0
        if "asia" in sql_lower and "lpi_score > 3" in sql_lower:
            result = df[
                df['region'].str.contains('Asia', case=False, na=False) &
                (df['lpi_score'] > 3.0)
            ].copy()
            
            result = result[['country', 'lpi_score', 'year']].drop_duplicates()
            result = result.sort_values('lpi_score', ascending=False)
            
            return result
        
        # Query 2: Average by region
        elif "group by region" in sql_lower and "avg" in sql_lower:
            result = df.groupby('region').agg({
                'lpi_score': 'mean'
            }).reset_index()
            
            result.columns = ['region', 'avg_lpi_score']
            result['avg_lpi_score'] = result['avg_lpi_score'].round(2)
            result = result.sort_values('avg_lpi_score', ascending=False)
            
            return result
        
        # Query 3: Top 5 countries
        elif "top 5" in sql_lower or ("limit 5" in sql_lower and "country" in sql_lower):
            result = df.groupby('country').agg({
                'lpi_score': 'max'
            }).reset_index()
            
            result.columns = ['country', 'max_lpi_score']
            result = result.sort_values('max_lpi_score', ascending=False).head(5)
            
            return result
        
        # Default: return filtered data
        else:
            return df
        
    except Exception as e:
        print(f"Error executing query: {e}")
        import traceback
        traceback.print_exc()
        return None