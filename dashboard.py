import streamlit as st
import mysql.connector
from datetime import datetime
import pandas as pd
import altair as alt

# ----------------------------------------------
# Creating Database Connection
# ----------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="bankONE",
        password="0701",
        database="P1"
    )

# ----------------------------------------------
# Fetching Queries from DB
# ----------------------------------------------
def fetch_queries(status_filter=None, category_filter=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM query1 WHERE 1=1"
    params = []

    if status_filter and status_filter != "All":
        query += " AND status = %s"
        params.append(status_filter)

    if category_filter and category_filter != "All":
        query += " AND category = %s"
        params.append(category_filter)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

# ----------------------------------------------
# Close a Query
# ----------------------------------------------
def close_query(query_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE query1
        SET status = 'Closed',
            query_closed_time = %s
        WHERE query_id = %s
    """

    values = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query_id)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------------------------
# STREAMLIT UI
# ----------------------------------------------
st.title("Query Management Dashboard (Support Team)")

# ----------------------------------------------
# FILTERS
# ----------------------------------------------
st.subheader("Filter Queries")

left, right = st.columns(2)

status_filter = left.selectbox("Filter by status", ["All", "Open", "Closed"])

# ----------------------------------------------
# Fetch & Display Data
# ----------------------------------------------
queries = fetch_queries(status_filter)

if queries:
    df = pd.DataFrame(queries)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No queries found for the selected filters.")

# ----------------------------------------------
# CLOSING the QUERY
# ----------------------------------------------
st.subheader("Close an Open Query")

# Filtering only open queries for closure
open_queries = [q for q in queries if q["status"] == "Open"]

if open_queries:
    selected_query = st.selectbox(
        "Select Query to Close",
        open_queries,
        format_func=lambda x: f"#{x['query_id']} - {x['queryheading']}"
    )

    if st.button("Close Selected Query"):
        close_query(selected_query["query_id"])
        st.success(f"Query #{selected_query['query_id']} has been closed.")
        st.rerun()
else:
    st.info("No open queries available to close.")

# ----------------------------------------------
# ANALYTICS AND VISUALIZATION
# ----------------------------------------------
st.subheader("Query Analytics & Visualization")

if queries:
    df = pd.DataFrame(queries)

    # Ensure date columns are datetime
    df["query_created_time"] = pd.to_datetime(df["query_created_time"], errors="coerce")
    df["query_closed_time"] = pd.to_datetime(df["query_closed_time"], errors="coerce")

    # ------------------------------------------------
    # 1. Queries Created Per Day
    # ------------------------------------------------
    st.write("### 📊 Queries Created Per Day")

    created_per_day = (
        df.groupby(df["query_created_time"].dt.date)
          .size()
          .reset_index(name="count")
          .rename(columns={"query_created_time": "date"})
    )

    chart_created = (
        alt.Chart(created_per_day)
        .mark_bar(color="#4C72B0")
        .encode(
            x="date:T",
            y="count:Q",
            tooltip=["date:T", "count:Q"]
        )
    )

    st.altair_chart(chart_created, use_container_width=True)

    # ------------------------------------------------
    # 2. Open vs Closed Queries (Status Pie Chart)
    # ------------------------------------------------
    st.write("### 🥧 Query Status Distribution")

    status_count = df["status"].value_counts().reset_index()
    status_count.columns = ["status", "count"]

    pie_chart = (
        alt.Chart(status_count)
        .mark_arc()
        .encode(
            theta="count:Q",
            color="status:N",
            tooltip=["status:N", "count:Q"]
        )
    )

    st.altair_chart(pie_chart, use_container_width=True)

    # ------------------------------------------------
    # 3. Queries Closed Per Day
    # ------------------------------------------------
    st.write("### 📉 Queries Closed Per Day")

    closed_df = df.dropna(subset=["query_closed_time"])

    if not closed_df.empty:
        closed_per_day = (
            closed_df.groupby(closed_df["query_closed_time"].dt.date)
                     .size()
                     .reset_index(name="count")
                     .rename(columns={"query_closed_time": "date"})
        )

        chart_closed = (
            alt.Chart(closed_per_day)
            .mark_bar(color="#DD8452")
            .encode(
                x="date:T",
                y="count:Q",
                tooltip=["date:T", "count:Q"]
            )
        )

        st.altair_chart(chart_closed, use_container_width=True)
    else:
        st.info("No closed queries available to visualize.")
else:
    st.warning("No data available for visualization.")

