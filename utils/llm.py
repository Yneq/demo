
import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_llm(prompt: str, model: str = "anthropic/claude-3.5-sonnet") -> Optional[str]:
    """
    Call OpenRouter LLM to convert text to SQL.
    
    Args:
        prompt: The prompt containing the question
        model: Model to use (default: Claude 3.5 Sonnet)
    
    Returns:
        Generated SQL query or None if error
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,  # Low temperature for more deterministic SQL
            "max_tokens": 500
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        
        result = response.json()
        sql_query = result["choices"][0]["message"]["content"].strip()
        
        # Clean up the SQL query (remove markdown code blocks if present)
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        
        return sql_query
        
    except requests.exceptions.Timeout:
        print("Error: LLM request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing LLM response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None