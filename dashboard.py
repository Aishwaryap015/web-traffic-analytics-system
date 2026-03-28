import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from auth import login_user

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(layout="wide", page_title="Analytics Dashboard ~ AP")

# ---------------------------
# CUSTOM CSS (SAAS UI 🔥)
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Cards */
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

/* Titles */
h1, h2, h3 {
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Buttons */
.stDownloadButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOGIN SYSTEM
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login_user(username, password)

        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------------------
# LOAD DATA
# ---------------------------
conn = sqlite3.connect("data/web_traffic.db")
df = pd.read_sql_query("SELECT * FROM web_traffic", conn)

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.markdown("### 👤 User")
st.sidebar.write(st.session_state.username)
st.sidebar.write(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# FILTERS
source = st.sidebar.selectbox("Traffic Source", ["All"] + list(df["source"].unique()))

min_date = df["timestamp"].min().date()
max_date = df["timestamp"].max().date()

start_date, end_date = st.sidebar.date_input("Date Range", [min_date, max_date])

df = df[
    (df["timestamp"].dt.date >= start_date) &
    (df["timestamp"].dt.date <= end_date)
]

if source != "All":
    df = df[df["source"] == source]

# EXPORT
csv = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("Download CSV", csv, "data.csv")

# ---------------------------
# HEADER
# ---------------------------
st.title("📊 Web Traffic Analytics Dashboard ~ AP")

# ---------------------------
# KPI CARDS 🔥
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'><h3>Total Records</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><h3>Users</h3><h2>{df['user_id'].nunique()}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><h3>Sessions</h3><h2>{df['session_id'].nunique()}</h2></div>", unsafe_allow_html=True)

# ---------------------------
# AI INSIGHTS 🤖
# ---------------------------
st.subheader("🤖 Smart Insights ~ AP")

insights = []

if len(df) > 20000:
    insights.append("High traffic spike detected")
elif len(df) < 1000:
    insights.append("Traffic is low")

top_source = df["source"].value_counts().idxmax()
insights.append(f"Top source: {top_source}")

top_page = df["page"].value_counts().idxmax()
insights.append(f"Most visited page: {top_page}")

for i in insights:
    st.success(i)

# ---------------------------
# TRAFFIC DISTRIBUTION
# ---------------------------
col1, col2 = st.columns(2)

source_counts = df["source"].value_counts().reset_index()
source_counts.columns = ["Source", "Count"]

with col1:
    fig = px.pie(source_counts, names="Source", values="Count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Insights")
    for _, row in source_counts.iterrows():
        percent = (row["Count"]/len(df))*100
        st.write(f"{row['Source']} → {percent:.1f}%")

# ---------------------------
# DAILY TREND
# ---------------------------
daily = df.groupby(df["timestamp"].dt.date).size().reset_index()
daily.columns = ["Date", "Visits"]

st.plotly_chart(px.line(daily, x="Date", y="Visits"), use_container_width=True)

# ---------------------------
# FUNNEL
# ---------------------------
funnel = pd.DataFrame({
    "Stage": ["Views", "Clicks", "Logins", "Checkout"],
    "Count": [
        len(df[df["action"]=="view"]),
        len(df[df["action"]=="click"]),
        len(df[df["action"]=="login"]),
        len(df[df["page"]=="Checkout"])
    ]
})

st.plotly_chart(px.bar(funnel, x="Stage", y="Count"), use_container_width=True)

# ---------------------------
# ROLE BASED
# ---------------------------
if st.session_state.role == "admin":
    st.subheader("Admin Panel")
    st.dataframe(df)

else:
    st.subheader("User View")
    st.dataframe(df.head(50))