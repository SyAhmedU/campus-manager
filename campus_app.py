import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="FPC Campus", page_icon="🎓", layout="wide")

# --- CUSTOM CSS (THE "GLOW UP") ---
st.markdown("""
    <style>
    .big-font { font-size: 20px !important; }
    div.stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNECTION SETUP ---
try:
    key_dict = st.secrets["service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    # YOUR ACTUAL SHEET ID IS NOW HARDCODED HERE
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE"
    
    sheet = client.open_by_key(sheet_id)
    sheet_logs = sheet.worksheet("Logs")
    sheet_students = sheet.worksheet("Students")

except Exception as e:
    st.error("⚠️ Connection Error. Please check your Sheet ID in the code.")
    st.stop()

# --- HEADER ---
st.title("🎓 FPC Campus Operations")
st.markdown("---")

# --- MAIN NAVIGATION (TABS) ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Log Issue", "👥 Student Database"])

# --- TAB 1: DASHBOARD ---
with tab1:
    # Fetch Data
    logs = sheet_logs.get_all_records()
    df_logs = pd.DataFrame(logs)
    
    # Calculate Stats
    total_issues = len(df_logs)
    # Check if 'Status' column exists, otherwise assume all are Open
    if 'Status' in df_logs.columns:
        open_issues = len(df_logs[df_logs['Status'] == 'Open'])
    else:
        open_issues = total_issues 

    # Display Metrics in Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logs", total_issues, "All time")
    col2.metric("Open Issues", open_issues, "Needs Attention", delta_color="inverse")
    col3.metric("System Status", "Online", "🟢 Connected")

    st.subheader("Recent Activity")
    if not df_logs.empty:
        st.dataframe(df_logs.tail(5), use_container_width=True)
    else:
        st.info("No logs found yet.")

# --- TAB 2: LOG ISSUE ---
with tab2:
    st.write("### 🚩 Report a Student Issue")
    
    with st.form("clean_log_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            mentor = st.selectbox("Reporting Mentor", ["Mentor 1", "Mentor 2", "Mentor 3", "Mentor 4"])
            batch = st.selectbox("Batch", ["Year I", "Year II"])
        with c2:
            s_id = st.text_input("Student ID (e.g., Y1-004)")
            issue_type = st.selectbox("Issue Type", ["Discipline", "Late Arrival", "Academic", "Health"])
            
        details = st.text_area("Detailed Description")
        
        submitted = st.form_submit_button("🚀 Submit Report")
        
        if submitted:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            # Save: Date | Mentor | Student_ID | Issue | Status
            sheet_logs.append_row([timestamp, mentor, s_id, f"[{issue_type}] {details}", "Open"])
            st.toast("✅ Report Submitted Successfully!")

# --- TAB 3: DATABASE ---
with tab3:
    st.write("### 📂 Complete Student List")
    
    # Search Bar
    search = st.text_input("🔍 Search by Name or ID", "")
    
    # Load Data
    students = sheet_students.get_all_records()
    df_students = pd.DataFrame(students)
    
    if search:
        # Filter data (Case insensitive)
        mask = df_students.apply(lambda x: x.astype(str).str.contains(search, case=False).any(), axis=1)
        df_filtered = df_students[mask]
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.dataframe(df_students, use_container_width=True)
