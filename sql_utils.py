import requests
import os
import psycopg2
import pandas as pd
import streamlit as st
from metadata import TABLE_COLUMN_MAP  # Import column mapping
import re

# Load API key from secrets
TOGETHER_AI_API_KEY = st.secrets["TOGETHER_AI_API_KEY"]

def map_columns(sql_query):
    """ Replace incorrect columns and make all string comparisons case-insensitive """
    replacements = {
        "policy_customer_policy_claim_payment_id": "policy_id",
        "policy_policy_claim_status": "policy_status",
        "policy_policy_status": "policy_status",
    }

    for incorrect, correct in replacements.items():
        if incorrect in sql_query:
            print(f"🔄 Replacing '{incorrect}' with '{correct}'")  # Debugging print
            sql_query = sql_query.replace(incorrect, correct)

    # ✅ Fix incorrect pattern `policy.TRIM(policy_status) ILIKE`
    sql_query = re.sub(r"policy\.TRIM\(([^)]+)\)", r"TRIM(\1)", sql_query)
    return sql_query
    
    # ✅ Extra Fix: Ensure incorrect hallucinated column names are corrected
    sql_query = sql_query.replace("policy_customer_policy_claim_payment_id", "policy_id")
    sql_query = sql_query.replace("policy_policy_status", "policy_status")  # Another fix
    return sql_query

def clean_sql_output(sql_query):
    """ Remove non-SQL text from AI response """

    # ✅ Remove everything before the first SELECT (ensures SQL-only output)
    sql_query = re.sub(r"(?i)^.*?(SELECT)", r"\1", sql_query).strip()

    # ✅ Remove unnecessary list formatting (e.g., "Customers who are 18 or younger")
    sql_query = re.sub(r"^\d+\.\s*", "", sql_query, flags=re.MULTILINE)
    sql_query = re.sub(r"(?i)customers who are.*", "", sql_query).strip()  # Removes category labels

    # ✅ Remove markdown formatting
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # ✅ Extract only the first SQL query if multiple exist
    sql_query = sql_query.split("User Query:")[0].strip()  # Remove additional AI-generated user queries
    sql_query = sql_query.split("\n\n")[0].strip()  # Keep only the first valid query

    return sql_query

def generate_sql(user_query):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # ✅ Strictly enforce the correct database schema
    schema_info = (
        "**PostgreSQL Schema**:\n"
        "- **customer** (customer_id, customer_name, customer_age, customer_email)\n"
        "- **policy** (policy_id, customer_id, policy_type, policy_status, policy_start_date, policy_end_date, premium_amount)\n"
        "- **claims** (claim_id, policy_id, claim_amount, claim_status, claim_date)\n"
        "- **payments** (payment_id, policy_id, payment_amount, payment_date)\n\n"
        "Use ONLY the column names listed above. Do NOT make up new columns.\n"
        "If a condition requires `customer_age`, always JOIN `policy` and `customer` using `customer.customer_id = policy.customer_id`.\n"
        "STRICT RULES: Ensure `policy_status` uses `ILIKE 'active'` for case-insensitivity.\n"
        "ONLY include `policy_end_date IS NULL` if explicitly asked for policies with NO end date."
        "Do NOT include `policy_end_date IS NULL` unless the user explicitly asks for 'policies with no end date'.\n"
        "ALWAYS use fully qualified column names (e.g., `customer.customer_id` instead of `customer_id`).\n"
         "To find policies expiring within the next 30 days, use:\n"
        "`policy_end_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'`\n"
        "DO NOT use `DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '30 days'` as it gives incorrect results.\n"
        "Do NOT add `policy_end_date IS NULL` unless explicitly requested.\n"
        "ALWAYS use `GROUP BY` when aggregating values (e.g., `SUM(premium_amount) BY policy_type`).\n"
        "DO NOT add unnecessary semicolons (`;`) before `GROUP BY` statements.\n"
        "ALWAYS ensure correct aggregation when using `COUNT()` or `SUM()`.\n"
    )

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": (
            "You are an expert SQL assistant for a PostgreSQL database.\n"
            f"{schema_info}\n"
            "Convert the following natural language request into a valid PostgreSQL SQL query.\n"
            "STRICT RULES: Ensure `policy_status` uses `ILIKE 'active'` for case-insensitivity.\n"
            "Always use `customer.customer_id`, `policy.policy_status`, `policy.policy_end_date`, etc.\n"
            "Do NOT include `policy_end_date IS NULL` unless specifically requested.\n"
            "ALWAYS use fully qualified column names (e.g., `customer.customer_id` instead of `customer_id`).\n"
            "Do NOT include explanations, comments, or markdown formatting (` ``` `).\n\n"
            "To find policies expiring within the next 30 days, use:\n"
            "`policy_end_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'`\n"
            "DO NOT use `DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '30 days'` as it gives incorrect results.\n"
            f"User Query: {user_query}\n\n"
        ),
        "max_tokens": 250
    }
    
    response = requests.post(url, json=data, headers=headers).json()
    
    print("🔹 API Raw Response:", response)  # Debugging print

    if "error" in response:
        print("❌ API Error:", response["error"])
        return "SELECT 'Error: SQL query generation failed.' AS message;"

    sql_query = response.get("choices", [{}])[0].get("text", "").strip()

    print("📝 **Generated SQL Query (Raw):**", sql_query)  # Debugging print

    # ✅ Remove markdown formatting (```sql ... ```)
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # ✅ Clean up the SQL output
    sql_query = clean_sql_output(sql_query)

    # ✅ Map incorrect column names to actual column names
    sql_query = map_columns(sql_query)

    print("📝 **Final SQL Query After Fix:**", sql_query)  # Debugging print

    return sql_query

def execute_sql(query):
    """ Connect to the Render PostgreSQL database and execute queries """
    try:
        conn = psycopg2.connect(
            dbname=st.secrets["PG_DB"],
            user=st.secrets["PG_USER"],
            password=st.secrets["PG_PASSWORD"],
            host=st.secrets["PG_HOST"],
            port=st.secrets["PG_PORT"]
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        conn.close()
        return df
    except Exception as e:
        return f"❌ SQL Execution Error: {str(e)}"
