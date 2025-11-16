import streamlit as st
import pandas as pd
import mysql.connector
import hashlib
from datetime import datetime
import pandas as pd
import time

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="bankONE",
        password="0701",
        database="P1"
    )
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
        
            


st.header ('Client Query Management System') 


#st.button ('Register')

form=st.title("Registration Page")


with st.form(key="registration_form"):
    username = st.text_input("USER_NAME")
    name = st.text_input("NAME")
    email = st.text_input("EMAIL")
    number = st.text_input("MOBILE NUMBER")
    password = st.text_input("PASSWORD", type="password")
    role = st.selectbox("ROLE",["Client", "Support"])
    submit = st.form_submit_button(label="SUBMIT")
    
    # The submit button must be inside the form
   # submit_button = st.form_submit_button(label="Register")

# You can handle form submission here
if submit:
    if not username or not name or not email or not number or not password:
        st.error("⚠️ Please fill in all fields before submitting.")
    elif not number.isdigit():
        st.error("📱 Please enter a valid mobile number (numbers only).")
    else:
        try:
            # Connect to the DB here
            mydb = create_connection()
            if mydb.is_connected():
                st.success("Connected to MySQL database.")
            else:
                st.error("Failed to connect to MySQL database.")
            
            cursor = mydb.cursor()

            # Check if username/email exists
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error("🚫 Username or Email already exists. Please choose another.")
            else:
                # Hash password
                hashed_pw = hash_password(password)

                # Insert user
                query = """
                    INSERT INTO user (username, email, name, phone_number, hashed_password, role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (username, email, name, number, hashed_pw, role)
                cursor.execute(query, values)
                mydb.commit()

                st.success("✅ Registration Successful!")

                # Display entered data
                reg_data = {
                    "Username": username,
                    "Name": name,
                    "Email": email,
                    "Phone": number,
                    "Role": role
                }
                st.write("### Your Information:")
                st.table(pd.DataFrame([reg_data]))

        except mysql.connector.Error as e:
            st.error(f"❌ Database Error: {e}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'mydb' in locals() and mydb.is_connected():
                mydb.close()
else:
    st.info("ℹ️ Please provide the requested information and click **Submit**.")
st.balloons()
#displayy the data as table
st.write("here is the details")
#st.table(df)


