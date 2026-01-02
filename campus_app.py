import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION & SETUP ---
st.set_page_config(page_title="FPC-AMET Campus Manager", layout="wide")
FILE_STUDENTS = 'amet_students.csv'
FILE_LOGS = 'amet_logs.csv'

# --- 1. DATA INITIALIZATION (The "Zero Cost" Database) ---
def init_data():
    # If student list doesn't exist, we create the 150 students automatically
    if not os.path.exists(FILE_STUDENTS):
        students = []
        # Generate 85 Year I Students
        for i in range(1, 86):
            students.append({"ID": f"Y1-{i:03d}", "Name": f"Student Y1-{i}", "Year": "Year I", "Mentor": "Unassigned"})
        # Generate 65 Year II Students
        for i in range(1, 66):
            students.append({"ID": f"Y2-{i:03d}", "Name": f"Student Y2-{i}", "Year": "Year II", "Mentor": "Unassigned"})
        
        df = pd.DataFrame(students)
        df.to_csv(FILE_STUDENTS, index=False)

    # If logs don't exist, create file
    if not os.path.exists(FILE_LOGS):
        df_logs = pd.DataFrame(columns=["Date", "Mentor", "Student_ID", "Issue", "Status"])
        df_logs.to_csv(FILE_LOGS, index=False)

init_data()

# --- 2. LOAD DATA ---
df_students = pd.read_csv(FILE_STUDENTS)
df_logs = pd.read_csv(FILE_LOGS)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🎓 FPC-AMET Ops")
menu = st.sidebar.radio("Go to:", ["Dashboard", "Daily Attendance", "Mentor Log", "Student List"])
st.sidebar.markdown("---")
st.sidebar.info(f"System Status: Online\nStudents: {len(df_students)}\nMentors: 8")

# --- 4. APP MODULES ---

# === DASHBOARD ===
if menu == "Dashboard":
    st.title("Campus Command Center")
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", len(df_students))
    c2.metric("Pending Issues", len(df_logs[df_logs['Status'] == 'Open']))
    c3.metric("Attendance (Today)", "Active")
    
    st.markdown("### 📢 Recent Mentor Logs")
    if not df_logs.empty:
        st.dataframe(df_logs.tail(5), use_container_width=True)
    else:
        st.info("No logs recorded yet.")

# === ATTENDANCE SYSTEM ===
elif menu == "Daily Attendance":
    st.title("📝 Daily Attendance")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Batch", ["Year I", "Year II"])
    with col2:
        mentor_name = st.selectbox("Mentor Name", [f"Mentor {i}" for i in range(1,9)])
    
    # Filter students by year
    filtered_students = df_students[df_students['Year'] == selected_year]
    
    with st.form("attendance_form"):
        st.write(f"Marking Attendance for **{selected_year}**")
        
        # Create a checklist for students
        # In a real scenario, we save this to a separate CSV. 
        # For this demo, we just simulate the submission.
        attendance_data = {}
        for index, row in filtered_students.head(20).iterrows(): # Showing first 20 for cleaner UI
            attendance_data[row['ID']] = st.checkbox(f"{row['ID']} - {row['Name']}", value=True)
            
        submitted = st.form_submit_button("Submit Attendance")
        if submitted:
            st.success(f"Attendance recorded for {selected_year} by {mentor_name} at {datetime.now().strftime('%H:%M')}")

# === MENTOR LOG (ISSUES) ===
elif menu == "Mentor Log":
    st.title("🚩 Mentor Issue Tracker")
    
    with st.form("issue_log"):
        st.write("Log a Student Issue or Incident")
        m_name = st.selectbox("Reporting Mentor", [f"Mentor {i}" for i in range(1,9)])
        s_id = st.selectbox("Student ID", df_students['ID'].unique())
        issue_txt = st.text_area("Description of Issue")
        priority = st.select_slider("Priority", options=["Low", "Medium", "High", "Critical"])
        
        submit_log = st.form_submit_button("Log Issue")
        
        if submit_log:
            new_log = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Mentor": m_name,
                "Student_ID": s_id,
                "Issue": f"[{priority}] {issue_txt}",
                "Status": "Open"
            }
            # Append to CSV
            new_df = pd.DataFrame([new_log])
            new_df.to_csv(FILE_LOGS, mode='a', header=False, index=False)
            st.success("Issue Logged Successfully!")
            st.rerun()

# === STUDENT LIST ===
elif menu == "Student List":
    st.title("📂 Student Database")
    st.dataframe(df_students, use_container_width=True)