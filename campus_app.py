import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="FPC-AMET Campus Manager", layout="wide")

# --- CONNECT TO GOOGLE SHEETS ---
try:
    # 1. Get the secret we just saved
    # We parse the JSON string from the "service_account" variable in secrets
    key_dict = json.loads(st.secrets["service_account"])
    
    # 2. Authenticate
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    # 3. Open the Spreadsheet (Must match your Google Sheet name exactly)
    sheet = client.open("FPC Campus Data")
    sheet_students = sheet.worksheet("Students")
    sheet_logs = sheet.worksheet("Logs")

except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

# --- APP INTERFACE ---
st.sidebar.title("🎓 FPC-AMET Ops")
st.sidebar.success("🟢 Online & Connected")

menu = st.sidebar.radio("Menu", ["Dashboard", "Attendance", "Mentor Log", "Student List"])

if menu == "Dashboard":
    st.title("Campus Command Center")
    
    # Fetch data live
    logs_data = sheet_logs.get_all_records()
    df_logs = pd.DataFrame(logs_data)
    
    c1, c2 = st.columns(2)
    c1.metric("Total Logs", len(df_logs))
    c2.metric("Pending Issues", len(df_logs[df_logs['Status'] == 'Open']) if not df_logs.empty else 0)
    
    st.subheader("Recent Activity")
    if not df_logs.empty:
        st.dataframe(df_logs.tail(5), use_container_width=True)

elif menu == "Attendance":
    st.title("📝 Mark Attendance")
    
    with st.form("attendance_form"):
        mentor = st.selectbox("Reporting Mentor", [f"Mentor {i}" for i in range(1,9)])
        batch = st.selectbox("Batch", ["Year I", "Year II"])
        status = st.radio("Status", ["All Present", "Exceptions"])
        notes = st.text_input("If Exceptions, list Absent IDs (e.g. Y1-002, Y1-009)")
        
        submitted = st.form_submit_button("Submit Attendance")
        
        if submitted:
            # Add row to Google Sheet
            # Format: Date | Mentor | Student_ID | Issue | Status
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = [timestamp, mentor, "BATCH-LOG", f"Attendance: {batch} - {status} ({notes})", "Closed"]
            sheet_logs.append_row(log_entry)
            st.success(f"✅ Attendance saved for {batch}!")

elif menu == "Mentor Log":
    st.title("🚩 Report an Issue")
    
    with st.form("log_form"):
        mentor = st.selectbox("Mentor Name", [f"Mentor {i}" for i in range(1,9)])
        s_id = st.text_input("Student ID (e.g., Y1-005)")
        issue = st.text_area("Description of Issue")
        
        if st.form_submit_button("Save Log"):
            timestamp = datetime.now().strftime("%Y-%m-%d")
            # Format: Date | Mentor | Student_ID | Issue | Status
            new_row = [timestamp, mentor, s_id, issue, "Open"]
            sheet_logs.append_row(new_row)
            st.success("✅ Issue logged in Google Sheet!")

elif menu == "Student List":
    st.title("📂 Student Database")
    # Fetch live data
    data = sheet_students.get_all_records()
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
