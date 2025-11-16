import streamlit as st
from datetime import datetime
import mysql.connector

# ---------------------------------------
# creating Database Connection
# ---------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="bankONE",
        password="0701",
        database="P1"
    )

# ---------------------------------------
# saving Query into database
# ---------------------------------------
def insert_query(mailid,mobileno,queryheading, querydiscription, status,
query_created_time,query_closed_time):
    conn = get_connection()
    cursor = conn.cursor()
    

    sql = """
        INSERT INTO query1 
        (mailid,mobileno,queryheading, querydiscription, status,
query_created_time,query_closed_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (mailid,mobileno,queryheading, querydiscription, status,
query_created_time,query_closed_time)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()


# ---------------------------------------
# creating Streamlit UI
# ---------------------------------------
st.title(" Submit a New Query")

with st.form("query_form"):
    email = st.text_input("Email ID")
    mobile = st.text_input("Mobile Number")
    heading = st.text_input("Query Heading")
    description = st.text_area("querydiscription", height=150)

    submit = st.form_submit_button("Submit Query")

if submit:
    
    query_created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Open"
    query_closed_time = None  # NULL in MySQL

    try:
        insert_query(email, mobile, heading, description, status,query_created_time, query_closed_time)

        st.success(" Query Submitted Successfully!")
        st.info(f"Created Time: {query_created_time}")
        st.warning("Status: Open")

    except Exception as e:
        st.error(f"Error inserting query: {e}")
