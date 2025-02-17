import streamlit as st
from sql_utils import generate_sql, execute_sql  # Import functions
TOGETHER_AI_API_KEY = st.secrets["TOGETHER_AI_API_KEY"]

# 🎨 Custom Page Style
st.set_page_config(
    page_title="AI-Powered Insurance Data Query Assistant",
    page_icon="🤖",
    layout="wide",
)

# 🔹 Custom CSS for better UI
st.markdown(
    """
    <style>
        body {
            background-color: #f7f7f7;
        }
        .stTextInput>div>div>input {
            font-size: 18px !important;
            padding: 10px !important;
        }
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 8px !important;
            padding: 12px 20px !important;
        }
        .stButton>button:hover {
            background-color: #45a049 !important;
        }
        .stMarkdown {
            font-size: 18px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎭 Sidebar with Instructions
st.sidebar.header("📝 How to Use")
st.sidebar.write("""
- Enter a **natural language** question in the text box.
- Click **Submit** to generate an SQL query.
- The AI will run the query and show results.
- Example Queries:
  - "How many active policies do we have?"
  - "Show total premium amount for active policies by each policy type."
  - "List all customers with upcoming renewals."
""")
st.sidebar.write("---")
st.sidebar.info("💡 Tip: Use clear, simple sentences for better results.")

# 🎯 **App Title**
st.title("🤖 AI-Powered Insurance Data Query Assistant")

# 📝 **User Query Input**
user_input = st.text_input("🔍 Enter your query:", "")

# 🚀 **Submit Button**
if st.button("Submit Query"):
    if user_input:
        with st.spinner("⏳ Generating SQL query..."):
            sql_query = generate_sql(user_input)
        
        st.write(f"📝 **Generated SQL Query:** `{sql_query}`")

        if sql_query.strip().lower().startswith("select"):
            with st.spinner("⏳ Fetching results..."):
                df = execute_sql(sql_query)

            if isinstance(df, str):
                st.error(df)  # Show SQL error messages in Streamlit
            else:
                st.success("✅ Query executed successfully!")
                st.write("### 📊 Query Results:")
                st.dataframe(df)
        else:
            st.error("⚠️ Generated SQL query is invalid. Please check your input.")
    else:
        st.warning("⚠️ Please enter a query before submitting.")

# 📌 Footer
st.write("---")
st.write("🚀 Built by Mahesh with ❤️ using Mistral 7-B Instruct(Hosted at TogetherAI & Streamlit")
