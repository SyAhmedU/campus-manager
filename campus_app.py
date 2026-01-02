import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

st.set_page_config(page_title="FPC-AMET Campus Manager", layout="wide")

# --- 1. SETUP CONNECTION ---
try:
    key_dict = json.loads(st.secrets["service_account"])
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    # *** CRITICAL CHANGE: USING ID INSTEAD OF NAME ***
    # REPLACE THE TEXT BELOW WITH YOUR LONG CODE FROM STEP 1
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE" 
    
    sheet = client.open_by_key(sheet_id)
    sheet_logs = sheet.worksheet("Logs")
    sheet_students = sheet.worksheet("Students")
    
    st.sidebar.success("🟢 Connected via ID")

except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.info("Check: 1. Did you paste the Sheet ID in the code? 2. Is the Sheet shared with the campus-bot email?")
    st.stop()

# --- 2. APP INTERFACE ---
st.title("Campus Manager")

menu = st.sidebar.radio("Menu", ["Dashboard", "Mentor Log", "Student List"])

if menu == "Dashboard":
    st.metric("Total Logs", len(sheet_logs.get_all_values()) - 1)
    st.write("System is Online.")

elif menu == "Mentor Log":
    with st.form("log"):
        st.write("Log an Issue")
        mentor = st.selectbox("Mentor", ["Mentor 1", "Mentor 2"])
        issue = st.text_input("Issue")
        if st.form_submit_button("Submit"):
            sheet_logs.append_row([str(datetime.now()), mentor, issue])
            st.success("Saved!")

elif menu == "Student List":
    data = sheet_students.get_all_records()
    st.dataframe(pd.DataFrame(data))
