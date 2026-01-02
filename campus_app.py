import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="FPC-AMET Campus Manager", layout="wide")

# --- 1. SETUP CONNECTION ---
try:
    # UPDATED: Read directly from TOML secrets (No JSON parsing needed)
    # This matches the new format we just saved
    key_dict = st.secrets["service_account"]
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    # Using your ID (The fail-safe method)
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE" # <--- REPLACE THIS WITH YOUR SHEET ID AGAIN
    
    sheet = client.open_by_key(sheet_id)
    sheet_logs = sheet.worksheet("Logs")
    sheet_students = sheet.worksheet("Students")
    
    st.sidebar.success("🟢 System Online")

except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

# --- 2. APP INTERFACE ---
st.title("Campus Manager")

menu = st.sidebar.radio("Menu", ["Dashboard", "Mentor Log", "Student List"])

if menu == "Dashboard":
    st.metric("Total Logs", len(sheet_logs.get_all_values()) - 1)

elif menu == "Mentor Log":
    with st.form("log"):
        mentor = st.selectbox("Mentor", ["Mentor 1", "Mentor 2", "Mentor 3"])
        issue = st.text_input("Issue Description")
        if st.form_submit_button("Submit Log"):
            sheet_logs.append_row([str(datetime.now()), mentor, issue])
            st.success("Log Saved to Google Sheets!")

elif menu == "Student List":
    data = sheet_students.get_all_records()
    st.dataframe(pd.DataFrame(data))
