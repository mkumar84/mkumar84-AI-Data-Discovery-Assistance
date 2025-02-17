import streamlit as st
from sql_utils import generate_sql, execute_sql  # Import functions
TOGETHER_AI_API_KEY = st.secrets["TOGETHER_AI_API_KEY"]


# Streamlit UI
st.title("AI-Powered Insurance Data Query Assistant")

user_input = st.text_input("Enter your query:", "")

if st.button("Submit"):
    if user_input:
        st.write(f"🔍 **User Query:** {user_input}")  # Show user input
        sql_query = generate_sql(user_input)
        st.write(f"📝 **Generated SQL Query:** `{sql_query}`")  # Show generated SQL

        if sql_query.strip().lower().startswith("select"):  # Ensure it's a valid SQL query
            df = execute_sql(sql_query)
            if isinstance(df, str):
                st.error(df)  # Show SQL error messages in Streamlit
            else:
                st.write("### Query Results:")
                st.dataframe(df)
        else:
            st.error("⚠️ Generated SQL query is invalid. Please check your input.")

