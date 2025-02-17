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
        /* Full-Width Page */
        .block-container {
            padding: 2rem;
        }

        /* Customizing Input Box */
        .stTextInput>div>div>input {
            font-size: 18px !important;
            padding: 12px !important;
            border-radius: 10px !important;
            border: 2px solid #1e3a8a !important;
            background-color: #f9fafb !important;
        }

        /* Enhancing Submit Button */
        .stButton>button {
            background-color: #1e3a8a !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold;
            border-radius: 8px !important;
            padding: 12px 20px !important;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #153063 !important;
        }

        /* Table & Results Styling */
        .stDataFrame {
            background-color: white !important;
            border-radius: 10px !important;
        }

        /* Header & Text */
        .stMarkdown {
            font-size: 18px !important;
            color: #1e293b !important;
        }

        /* Sidebar */
        .stSidebar {
            background-color: #f1f5f9 !important;
            padding: 1rem !important;
        }

        /* Title */
        .title {
            font-size: 36px !important;
            font-weight: bold;
            color: #1e3a8a !important;
        }

        /* Footer */
        .footer {
            font-size: 14px !important;
            text-align: center;
            color: #4b5563 !important;
            margin-top: 20px;
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
user_input = st.text_input("🔍 Ask a question about insurance data:", "")

# 🚀 **Submit Button**
if st.button("📊 Get Insights"):
    if user_input:
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

# 📌 Footer
st.markdown("---")
st.markdown("<p class='footer'>🚀 Built by Mahesh with ❤️ using Mistral 7-B Instruct(Hosted at TogetherAI)| Powered by AI & Streamlit | February 2025</p>", unsafe_allow_html=True)
