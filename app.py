import streamlit as st
import sqlite3
import pandas as pd
import time

# DB connection
conn = sqlite3.connect("data/web_traffic.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------------
# LOGIN FUNCTION
# ------------------------
def login(username, password):
    query = "SELECT * FROM auth_users WHERE username=? AND password=?"
    result = cursor.execute(query, (username, password)).fetchone()
    return result

# ------------------------
# SESSION STATE
# ------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------------
# LOGIN PAGE
# ------------------------
if not st.session_state.logged_in:

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ------------------------
# DASHBOARD
# ------------------------
else:

    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("Web Traffic Dashboard")

    df = pd.read_sql_query("SELECT * FROM web_traffic", conn)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df.dropna(subset=["timestamp"])

    # KPIs
    st.subheader("Metrics")

    col1, col2 = st.columns(2)
    col1.metric("Total Records", len(df))
    col2.metric("Users", df["user_id"].nunique())

    # Role-based view
    if st.session_state.role == "admin":
        st.subheader("Admin Insights")
        st.dataframe(df.head(20))

    elif st.session_state.role == "analyst":
        st.subheader("Traffic Analysis")
        st.line_chart(df.groupby(df["timestamp"].dt.date).size())

    # Auto refresh
    time.sleep(3)
    st.rerun()