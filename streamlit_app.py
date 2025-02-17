import streamlit as st
from sql_utils import generate_sql, execute_sql  # Import functions
TOGETHER_AI_API_KEY = st.secrets["TOGETHER_AI_API_KEY"]

# 🎨 **Insurance Industry Theme**
st.set_page_config(
    page_title="Insurance Data Query Assistant",
    page_icon="💼",
    layout="wide",
)

# 🖌 **Custom CSS Styling**
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #1e3a8a !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: bold;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            margin: 5px;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #153063 !important;
        }
        .sample-container {
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎯 **Page Header**
st.markdown("<h1 class='title'>💼 Insurance Data Query Assistant</h1>", unsafe_allow_html=True)
st.write("📊 Quickly analyze your **insurance policies, claims, and customer data** with AI-driven insights.")

# 🎭 **Sidebar with Themed Sections**
st.sidebar.header("🔍 Explore Insights")
st.sidebar.write("""
- **Policies & Renewals**
- **Customer Analytics**
- **Claims Processing**
- **Premium Revenue**
""")

st.sidebar.write("---")
st.sidebar.info("💡 **Tip:** Use **simple, direct questions** for better results.")

# 📝 **User Query Input**
st.markdown("### ✨ Enter Your Query")

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

user_input = st.text_input("🔍 Ask a question about insurance data:", st.session_state.query_input)

# 📌 **Sample Prompts**
st.markdown("#### 📌 Try these sample queries:")
sample_queries = [
    "How many policies are currently active?",
    "What is the total premium amount for all active policies?",
    "How many active policies does each customer have?",
    "List all customers with upcoming renewals.",
]

col1, col2 = st.columns(2)
for i, query in enumerate(sample_queries):
    if col1.button(query, key=f"query_{i}"):
        st.session_state.query_input = query  # Store selected query
        st.rerun()  # ✅ Refresh UI to auto-fill

# 🚀 **Submit Button**
if st.button("📊 Get Insights"):
    if user_input:
        st.session_state.query_input = user_input  # Save input for re-use
        with st.spinner("⏳ Generating SQL query..."):
            sql_query = generate_sql(user_input)
        
        st.markdown(f"📝 **Generated SQL Query:** `{sql_query}`")

        if sql_query.strip().lower().startswith("select"):
            with st.spinner("⏳ Fetching data..."):
                df = execute_sql(sql_query)

            if isinstance(df, str):
                st.error(df)  # Show SQL error messages
            else:
                st.success("✅ Data retrieved successfully!")
                st.markdown("### 📌 **Query Results**")
                st.dataframe(df)
        else:
            st.error("⚠️ Generated SQL query is invalid. Please check your input.")
    else:
        st.warning("⚠️ Please enter a query before submitting.")

# 🔄 **Reset Button to Clear Query**
if st.button("🔄 Reset Query"):
    st.session_state.query_input = ""  # Clear the input field
    st.rerun()  # Refresh UI

# 📌 Footer
st.markdown("---")
st.markdown("<p class='footer'>🚀 Built by Mahesh with ❤️ using Mistral 7-B Instruct(Hosted at TogetherAI)| Powered by AI & Streamlit | February 2025</p>", unsafe_allow_html=True)
