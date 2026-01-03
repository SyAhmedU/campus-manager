import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="CampusOne Cloud", page_icon="☁️", layout="wide")

# --- 2. APPLE-STYLE CSS ---
st.markdown("""
    <style>
    /* Global Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    .stApp {
        background-color: #F8FAFC;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    /* Card Containers */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
    }
    
    /* Headers */
    h1 { font-weight: 700 !important; letter-spacing: -0.02em; }
    h3 { font-weight: 600 !important; color: #334155 !important; }

    /* Scheduler Grid Styling */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SHEETS CONNECTION ---
try:
    key_dict = st.secrets["service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE" # Your ID
    sheet = client.open_by_key(sheet_id)
    
    # Load Tabs
    ws_tasks = sheet.worksheet("Tasks")
    ws_schedule = sheet.worksheet("Scheduler")

except Exception as e:
    st.error("⚠️ Connection Error. Please check your Secrets or Sheet ID.")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("CampusOne ☁️")
    st.caption(f"Connected to Google Sheets")
    st.markdown("---")
    
    menu = st.radio("Navigate", [
        "Dashboard",
        "Daily Scheduler",
        "Task Manager"
    ])
    
    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# --- 5. DATA LOADERS ---
def load_schedule():
    data = ws_schedule.get_all_records()
    return pd.DataFrame(data)

def save_schedule_row(date, time, task, link, stake, remarks):
    # Append row to Google Sheets
    ws_schedule.append_row([str(date), time, task, link, stake, remarks])

# --- 6. PAGE: DASHBOARD ---
if menu == "Dashboard":
    st.title(f"Overview: {datetime.now().strftime('%A, %d %B')}")
    
    # Live Stats from Google Sheets
    tasks = ws_tasks.get_all_records()
    df_tasks = pd.DataFrame(tasks)
    
    total = len(df_tasks)
    pending = len(df_tasks[df_tasks['Status'] != 'Done']) if not df_tasks.empty else 0
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card"><h3>Active Tasks</h3><h1>{pending}</h1></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><h3>Total Logged</h3><h1>{total}</h1></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><h3>System Status</h3><h1 style='color:#10B981'>Online</h1></div>""", unsafe_allow_html=True)

# --- 7. PAGE: DAILY SCHEDULER (The New Feature) ---
elif menu == "Daily Scheduler":
    st.title("📅 Daily Scheduler")
    
    # A. Date Selector
    c_date, c_blank = st.columns([1, 3])
    with c_date:
        selected_date = st.date_input("Select Date", datetime.now())
    
    st.info(f"Editing Schedule for: **{selected_date.strftime('%Y-%m-%d')}**")

    # B. The "Time Slices" Template
    time_slots = [
        "08:30 - 09:20", "09:20 - 10:10", "10:20 - 11:10",
        "11:10 - 12:00", "12:00 - 12:45", "12:45 - 01:30",
        "01:30 - 02:15", "02:15 - 03:00", "03:00 - 03:30"
    ]
    
    # C. Fetch Existing Data for this Date
    df_all = load_schedule()
    
    # Filter for selected date
    if not df_all.empty:
        # Ensure date column is string for comparison
        df_all['Date'] = df_all['Date'].astype(str)
        day_data = df_all[df_all['Date'] == str(selected_date)]
    else:
        day_data = pd.DataFrame()

    # D. Prepare Data for the Editor
    # We create a template DataFrame with the fixed time slots
    editor_data = []
    for slot in time_slots:
        # Check if we already have data for this slot
        existing = day_data[day_data['Time_Slot'] == slot] if not day_data.empty else pd.DataFrame()
        
        if not existing.empty:
            row = existing.iloc[0]
            editor_data.append({
                "Time_Slot": slot,
                "Task": row['Task'],
                "Link": row['Link'],
                "Stakeholders": row['Stakeholders'],
                "Remarks": row['Remarks']
            })
        else:
            editor_data.append({
                "Time_Slot": slot,
                "Task": "",
                "Link": "",
                "Stakeholders": "",
                "Remarks": ""
            })
            
    df_editor = pd.DataFrame(editor_data)

    # E. The Magic Grid (Data Editor)
    edited_df = st.data_editor(
        df_editor,
        column_config={
            "Time_Slot": st.column_config.TextColumn("Time", disabled=True), # Lock time
            "Task": st.column_config.TextColumn("Focus Task", width="medium"),
            "Link": st.column_config.LinkColumn("Resource Link"),
            "Stakeholders": st.column_config.TextColumn("People"),
            "Remarks": st.column_config.TextColumn("Notes")
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed"
    )

    # F. Save Button
    if st.button("💾 Save Schedule to Cloud"):
        # 1. Delete old rows for this date (to avoid duplicates)
        # Note: GSpread deletion is tricky, so we usually append. 
        # For simplicity in V1, we will just Append new versions. 
        # (A true database update requires finding row numbers).
        
        # Simple Append Strategy:
        for index, row in edited_df.iterrows():
            # Only save if there is a task written
            if row['Task'].strip() != "":
                save_schedule_row(
                    selected_date, 
                    row['Time_Slot'], 
                    row['Task'], 
                    row['Link'], 
                    row['Stakeholders'], 
                    row['Remarks']
                )
        
        st.success("✅ Schedule synced to Google Sheets!")
        st.cache_data.clear() # Force reload next time

# --- 8. PAGE: TASK MANAGER ---
elif menu == "Task Manager":
    st.title("✅ Task Manager")
    
    # Fetch
    tasks = ws_tasks.get_all_records()
    df = pd.DataFrame(tasks)
    
    # Show
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tasks found.")
        
    # Quick Add
    with st.form("new_task"):
        c1, c2 = st.columns([3, 1])
        with c1:
            new_t = st.text_input("New Task")
        with c2:
            cat = st.selectbox("Category", ["Admin", "Compliance", "Facilities"])
        
        if st.form_submit_button("Add Task"):
            ws_tasks.append_row([new_t, cat, "Daily", "Pending", ""])
            st.success("Added!")
            st.rerun()
