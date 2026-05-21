# app.py
# Personal Expense & Income Tracker System
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Expense Tracker System",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #125d91;
    color: white;
}

.metric-card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

h1, h2, h3 {
    color: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FILE HANDLING
# -----------------------------
FILE_NAME = "finance_data.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Date",
        "Type",
        "Category",
        "Amount",
        "Description"
    ])
    df.to_csv(FILE_NAME, index=False)

df = pd.read_csv(FILE_NAME)

# -----------------------------
# SIDEBAR MENU
# -----------------------------
st.sidebar.title("💼 Finance Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Transaction",
        "Statistics",
        "View Records"
    ]
)

st.sidebar.markdown("---")

# -----------------------------
# CATEGORY LISTS
# -----------------------------
expense_categories = [
    "Groceries",
    "Outfits / Clothing",
    "Stationary",
    "Vehicle Maintenance",
    "Fuel",
    "Business Investment",
    "Restaurant",
    "Cinema",
    "Friends & Social",
    "Bills",
    "Mobile Recharge",
    "Internet",
    "Healthcare",
    "Education",
    "Travel",
    "Entertainment",
    "Rent",
    "Savings",
    "Other"
]

income_categories = [
    "Salary",
    "Business Profit",
    "Freelancing",
    "Investment Return",
    "Gift",
    "Other Income"
]

# -----------------------------
# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":

    st.title("💰 Personal Expense Tracker")

    st.write("""
    Welcome to your professional finance management system.
    Track your income, monitor expenses, and analyze your spending habits efficiently.
    """)

    # ==============================
    # CLEAR DASHBOARD BUTTON
    # ==============================
    col_clear, col_space = st.columns([1, 5])

    with col_clear:
        if st.button("🗑 Clear Dashboard"):

            empty_df = pd.DataFrame(columns=[
                "Date",
                "Type",
                "Category",
                "Amount",
                "Payment Method",
                "Description"
            ])

            empty_df.to_csv(FILE_NAME, index=False)

            st.success("Dashboard Cleared Successfully ✅")
            st.rerun()

    if not df.empty:

        total_income = df[df["Type"] == "Income"]["Amount"].sum()

        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

        balance = total_income - total_expense

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Income", f"Rs. {total_income:,.2f}")

        with col2:
            st.metric("Total Expenses", f"Rs. {total_expense:,.2f}")

        with col3:
            st.metric("Current Balance", f"Rs. {balance:,.2f}")

        st.markdown("---")

        expense_df = df[df["Type"] == "Expense"]

        if not expense_df.empty:

            category_sum = expense_df.groupby(
                "Category"
            )["Amount"].sum().reset_index()

            fig = px.pie(
                category_sum,
                names="Category",
                values="Amount",
                title="Expense Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No financial data available.")

# -----------------------------
# -----------------------------
# -----------------------------
# -----------------------------
# -----------------------------
# ADD TRANSACTION
# -----------------------------
elif menu == "Add Transaction":

    st.title("➕ Add New Transaction")

    # =====================================
    # TRANSACTION TYPE
    # =====================================
    transaction_type = st.selectbox(
        "Transaction Type",
        ["Expense", "Income"]
    )

    st.markdown("---")

    # =====================================
    # EXPENSE SECTION
    # =====================================
    if transaction_type == "Expense":

        category = st.selectbox(
            "Expense Category",
            [
                "Groceries",
                "Outfits / Clothing",
                "Stationary",
                "Vehicle Maintenance",
                "Fuel",
                "Business Investment",
                "Restaurant",
                "Cinema",
                "Friends & Social",
                "Bills",
                "Internet",
                "Healthcare",
                "Education",
                "Travel",
                "Entertainment",
                "Self Investment",
                "Rent",
                "Other"
            ]
        )

        amount = st.number_input(
            "Amount Spent (Rs.)",
            min_value=0.0,
            format="%.2f"
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "Bank Transfer",
                "Debit Card",
                "Credit Card",
                "JazzCash",
                "EasyPaisa"
            ]
        )

        transaction_date = st.date_input(
            "Expense Date",
            datetime.today()
        )

        description = st.text_area(
            "Description / Notes",
            placeholder="Example: Grocery shopping for home"
        )

    # =====================================
    # INCOME SECTION
    # =====================================
    else:

        category = st.selectbox(
            "Income Source",
            [
                "Salary",
                "Freelancing",
                "Business Profit",
                "Investment Return",
                "Gift",
                "Rental Income",
                "Other Income"
            ]
        )

        amount = st.number_input(
            "Income Amount (Rs.)",
            min_value=0.0,
            format="%.2f"
        )

        received_from = st.text_input(
            "Received From",
            placeholder="Example: Company or Client Name"
        )

        payment_method = st.selectbox(
            "Received Via",
            [
                "Cash",
                "Bank Transfer",
                "JazzCash",
                "EasyPaisa",
                "Cheque"
            ]
        )

        transaction_date = st.date_input(
            "Income Date",
            datetime.today()
        )

        description = st.text_area(
            "Short Note",
            placeholder="Example: Monthly salary payment"
        )

    st.markdown("---")

    # =====================================
    # SAVE BUTTON
    # =====================================
    if st.button("Save Transaction"):

        new_data = {
            "Date": transaction_date,
            "Type": transaction_type,
            "Category": category,
            "Amount": amount,
            "Payment Method": payment_method,
            "Description": description
        }

        # Extra field only for income
        if transaction_type == "Income":
            new_data["Received From"] = received_from

        new_df = pd.DataFrame([new_data])

        updated_df = pd.concat([df, new_df], ignore_index=True)

        updated_df.to_csv(FILE_NAME, index=False)

        st.success("Transaction Added Successfully ✅")
# -----------------------------
# -----------------------------
# STATISTICS
# -----------------------------
elif menu == "Statistics":

    st.title("📊 Financial Statistics")

    # ==============================
    # CLEAR STATISTICS BUTTON
    # ==============================
    col_clear, col_space = st.columns([1, 5])

    with col_clear:
        if st.button("🗑 Clear Statistics"):

            empty_df = pd.DataFrame(columns=df.columns)

            empty_df.to_csv(FILE_NAME, index=False)

            st.success("Statistics Cleared Successfully ✅")
            st.rerun()

    if df.empty:
        st.warning("No records available.")

    else:

        df["Date"] = pd.to_datetime(df["Date"])

        time_filter = st.selectbox(
            "Select Time Period",
            [
                "One Day",
                "One Week",
                "One Month",
                "One Year",
                "All Time"
            ]
        )

        today = pd.Timestamp.today()

        if time_filter == "One Day":
            filtered_df = df[df["Date"] >= today - pd.Timedelta(days=1)]

        elif time_filter == "One Week":
            filtered_df = df[df["Date"] >= today - pd.Timedelta(days=7)]

        elif time_filter == "One Month":
            filtered_df = df[df["Date"] >= today - pd.Timedelta(days=30)]

        elif time_filter == "One Year":
            filtered_df = df[df["Date"] >= today - pd.Timedelta(days=365)]

        else:
            filtered_df = df

        income = filtered_df[
            filtered_df["Type"] == "Income"
        ]["Amount"].sum()

        expense = filtered_df[
            filtered_df["Type"] == "Expense"
        ]["Amount"].sum()

        savings = income - expense

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Income", f"Rs. {income:,.2f}")

        with col2:
            st.metric("Expenses", f"Rs. {expense:,.2f}")

        with col3:
            st.metric("Savings", f"Rs. {savings:,.2f}")

        st.markdown("---")

        daily_summary = filtered_df.groupby(
            ["Date", "Type"]
        )["Amount"].sum().reset_index()

        fig = px.line(
            daily_summary,
            x="Date",
            y="Amount",
            color="Type",
            markers=True,
            title="Income vs Expenses Trend"
        )
        # ==============================
        # CATEGORY-WISE EXPENSE BAR CHART
        # ==============================

        expense_only = filtered_df[
            filtered_df["Type"] == "Expense"
            ]

        if not expense_only.empty:

            category_data = expense_only.groupby(
                "Category"
            )["Amount"].sum().reset_index()

            fig2 = px.bar(
                category_data,
                x="Category",
                y="Amount",
                title="Category-wise Expenses",
                text_auto=True
            )

            fig2.update_layout(
                xaxis_title="Expense Category",
                yaxis_title="Amount (Rs.)"
            )

            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("No expense data available for bar chart.")

        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# -----------------------------
# VIEW RECORDS
# -----------------------------
elif menu == "View Records":

    st.title("📁 Transaction Records")

    if df.empty:
        st.info("No transaction records found.")

    else:

        search = st.text_input("Search Category")

        filtered = df

        if search:
            filtered = df[
                df["Category"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            filtered.sort_values(
                by="Date",
                ascending=False
            ),
            use_container_width=True
        )

        st.markdown("---")

        # ==============================
        # DELETE SINGLE RECORD
        # ==============================
        st.subheader("🗑 Delete Individual Record")

        record_index = st.number_input(
            "Enter Record Index to Delete",
            min_value=0,
            max_value=len(df) - 1,
            step=1
        )

        if st.button("Delete Selected Record"):

            df = df.drop(record_index)

            df.to_csv(FILE_NAME, index=False)

            st.success("Record Deleted Successfully ✅")
            st.rerun()

        st.markdown("---")

        # ==============================
        # CLEAR ALL RECORDS
        # ==============================
        if st.button("⚠ Clear All Records"):

            empty_df = pd.DataFrame(columns=df.columns)

            empty_df.to_csv(FILE_NAME, index=False)

            st.success("All Records Cleared Successfully ✅")
            st.rerun()

        st.download_button(
            label="⬇ Download Records as CSV",
            data=filtered.to_csv(index=False),
            file_name="finance_records.csv",
            mime="text/csv"
        )
# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Personal Finance Management System | Developed with Streamlit")