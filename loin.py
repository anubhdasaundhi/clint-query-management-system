import streamlit as st
import mysql.connector
import pandas as pan
import hashlib
## importing libraries

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()\
    

#creating the connection wiith DB
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="bankONE",
        password="0701",
        database="P1"
    )

#authenticating the username and password
#encoding the provided password to check if its matching with the one in the DB
# creating the authentication factor.
#  
def authenticate_user(username : str, password: str):
    hashed_pwd=hash_password(password)
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        query = """SELECT * from user WHERE username = %s and hashed_password = %s"""
        cursor.execute(query, (username, hashed_pwd))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


## creating loging form
st.title ("Client Query Management System")
username = st.text_input("USERNAME")
password = st.text_input("PASSWORD", type= "password" )
role = st.selectbox("ROLE",["Client", "Support"])


## condition processing to switch the pages to registration form, client query and support dashboard.
 
if st.button("REGISTER"):
    st.switch_page("pages/registrartion.py")
elif st.button("LOGIN"):
    if not username or not password:
        st.warning("Please enter USER NAME and PASSWORD!")
    
    else:
        user = authenticate_user(username, password)
        if user:
            if user["role"] != role:
                st.error(f"Role Mismatch: your account role is {user['role']}.")

            else:
                st.success(f"Login Successfull as {role}!")

                st.query_params["user"] = username  


                if role.lower() == "client":
                    st.switch_page("pages/clint.py")
                elif role.lower() == "support":
                    st.switch_page("pages/dashboard.py")

        else:
            st.error("Invalid User Name or Password")
    