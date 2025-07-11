import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import openai

# OPTIONAL: Set your OpenAI key here if you want to enable AI insights
# openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI Personal Finance Dashboard", layout="wide")

# Title
st.title("💸 AI-Powered Personal Finance Dashboard")
st.markdown("Upload your expense data and get smart financial insights.")

# Sidebar upload
uploaded_file = st.sidebar.file_uploader("Upload your expense CSV", type=["csv"])

# Sample Data Format Reminder
with st.sidebar.expander("📄 Sample CSV Format"):
    st.markdown("""
    ```
    Date,Category,Amount,Description
    2025-06-01,Food,250,Pizza Hut
    2025-06-03,Transport,120,Uber
    2025-06-05,Rent,15000,Monthly Rent
    ```
    """)

# Load and process CSV
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period("M").astype(str)

    # KPIs
    total_spent = df['Amount'].sum()
    top_category = df.groupby('Category')['Amount'].sum().idxmax()
    avg_monthly = df.groupby('Month')['Amount'].sum().mean()

    st.subheader("📊 Expense Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₹{total_spent:,.0f}")
    col2.metric("Top Spending Category", top_category)
    col3.metric("Avg. Monthly Spend", f"₹{avg_monthly:,.0f}")

    # Charts
    st.subheader("📌 Category-wise Spend")
    category_chart = px.pie(df, values='Amount', names='Category', title='Spend by Category')
    st.plotly_chart(category_chart, use_container_width=True)

    st.subheader("📈 Monthly Trend")
    monthly_chart = px.line(df.groupby('Month')['Amount'].sum().reset_index(),
                            x='Month', y='Amount', markers=True,
                            title='Monthly Expense Trend')
    st.plotly_chart(monthly_chart, use_container_width=True)

    # AI Suggestions (mock or real)
    st.subheader("🤖 AI Saving Suggestions")
    if "openai.api_key" in globals() and openai.api_key:
        # Send recent expense data to GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial advisor."},
                {"role": "user", "content": f"Analyze this expense data and suggest 3 ways to save money:\n{df.tail(20).to_string(index=False)}"}
            ]
        )
        advice = response['choices'][0]['message']['content']
        st.markdown(f"💡 {advice}")
    else:
        # Dummy Suggestions
        st.info("Add your OpenAI API key in the code to enable real-time suggestions.")
        st.markdown("""
        - Consider reducing eating-out expenses, which seem high.
        - Track monthly subscriptions—cancel unused ones.
        - Set category-wise budgets to prevent overspending.
        """)

else:
    st.warning("📤 Please upload a CSV file to get started.")


