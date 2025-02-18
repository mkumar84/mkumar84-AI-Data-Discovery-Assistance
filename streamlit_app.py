import streamlit as st
import matplotlib.pyplot as plt
from sql_utils import generate_sql, execute_sql  # Import functions
TOGETHER_AI_API_KEY = st.secrets["TOGETHER_AI_API_KEY"]

# 🎨 **Insurance Industry Theme**
st.set_page_config(
    page_title="AI-Powered Insurance Data Query Assistant",
    page_icon="💼",
    layout="wide",
)

# 🖌 **Custom CSS Styling**
st.markdown(
    """
    <style>
        .stButton>button {
            font-size: 16px !important;
            font-weight: bold;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            margin: 5px;
            transition: 0.3s ease-in-out;
        }
        /* Insights Button */
        .insights-button > button {
            background-color: #1e3a8a !important;
            color: white !important;
        }
        .insights-button > button:hover {
            background-color: #153063 !important;
        }
        /* Reset Button */
        .reset-button > button {
            background-color: #dc3545 !important;
            color: white !important;
        }
        .reset-button > button:hover {
            background-color: #b02a37 !important;
        }
        /* Sample Queries */
        .sample-container {
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .sample-queries {
            font-size: 14px !important;
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

# 📌 **Sample Prompts with Auto-Submission**
st.markdown("#### 📌 Try these sample queries:", unsafe_allow_html=True)
sample_queries = [
    "How many policies are currently active?",
    "What is the total premium amount for all active policies?",
    "How many active policies does each customer have?",
    "List all customers with upcoming renewals.",
    "How many claims have been processed for each policy type?",
]

col1, col2 = st.columns(2)
for i, query in enumerate(sample_queries):
    if col1.button(query, key=f"query_{i}"):
        st.session_state.query_input = query  # Store selected query
        st.session_state.auto_submit = True  # Flag for auto-submission
        st.rerun()  # ✅ Refresh UI to auto-fill and auto-submit

# 🚀 **Check for Auto-Submission**
if st.session_state.get("auto_submit", False):
    user_input = st.session_state.query_input  # Auto-fill input box
    del st.session_state.auto_submit  # Remove auto-submit flag
    auto_submit_triggered = True  # Flag to execute query

else:
    auto_submit_triggered = False

# 📌 **Buttons Layout**
col_left, col_right = st.columns([1, 1])

# 🔄 **Reset Button**
with col_left:
    if st.button("🔄 Reset Query", key="reset", help="Clear the query and start fresh", use_container_width=True):
        st.session_state.query_input = ""  # Clear the input field
        st.rerun()  # Refresh UI

# 🚀 **Submit Button**
with col_right:
    if st.button("📊 Get Insights", key="submit", help="Generate and execute SQL query", use_container_width=True) or auto_submit_triggered:
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
            else:
                st.error("⚠️ Generated SQL query is invalid. Please check your input.")
        else:
            st.warning("⚠️ Please enter a query before submitting.")

import matplotlib.pyplot as plt

# 🚀 **Move Table Rendering OUTSIDE of Button Layout**
if 'df' in locals() and not isinstance(df, str):
    st.markdown("### 📌 **Query Results**")

    # **Center the Table Properly**
    col_left_space, col_center, col_right_space = st.columns([1, 3, 1])
    with col_center:
        st.dataframe(df, use_container_width=True, height=min(500, len(df) * 35 + 50))  # Dynamically adjust height

    # 🚀 **Dynamically Generate Pie/Donut Chart for Aggregation Queries**
    if len(df.columns) == 2 and df.dtypes[1] in ["int64", "float64"]:
        st.markdown("### 📊 **Visual Breakdown**")

        # **Prepare the Chart Data**
        labels = df[df.columns[0]]  # First column (Categories)
        values = df[df.columns[1]]  # Second column (Counts/Amounts)

        # **Generate the Pie Chart**
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, wedgeprops={"edgecolor": "black"})
        ax.set_title("Data Breakdown")

        # **Display the Chart in Streamlit**
        st.pyplot(fig)

# 📌 Footer
st.markdown("---")
st.markdown("<p class='footer'>🚀 Built by Mahesh with ❤️ using Mistral 7-B Instruct(Hosted at TogetherAI)| Powered by AI & Streamlit | February 2025</p>", unsafe_allow_html=True)
