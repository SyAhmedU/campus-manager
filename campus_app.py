import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import webbrowser

# --- 1. PAGE SETUP (Must be first) ---
st.set_page_config(page_title="CampusOne", page_icon="", layout="wide")

# --- 2. THE DESIGNER CSS (The "Apple" Skin) ---
st.markdown("""
    <style>
    /* 1. Global Reset to Apple Style */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1D1D1F;
        background-color: #F5F5F7; /* Apple Light Grey */
    }
    
    /* Main Background Override */
    .stApp {
        background-color: #F5F5F7;
    }

    /* 2. Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #D2D2D7;
    }
    [data-testid="stSidebar"] h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* 3. Card Styling (The "Bento" Box) */
    .css-card {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.02);
    }
    
    /* 4. Time Slot Card */
    .time-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 4px solid #0071E3; /* Apple Blue Accent */
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    
    /* 5. Custom Buttons */
    .stButton > button {
        background-color: #0071E3;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #0077ED;
        transform: scale(1.01);
    }
    
    /* 6. Clean Inputs */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #D2D2D7;
        padding: 10px;
        background-color: #FFFFFF;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0071E3;
        box-shadow: 0 0 0 1px #0071E3;
    }
    
    /* Hide Streamlit Cruft */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CLOUD CONNECTION ---
try:
    key_dict = st.secrets["service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    # YOUR SHEET ID
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE" 
    sheet = client.open_by_key(sheet_id)
    ws_schedule = sheet.worksheet("Scheduler")

except Exception as e:
    st.error("⚠️ Cloud Sync Error. Check Secrets.")
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/814px-Apple_logo_black.svg.png", width=25)
    st.markdown("### **CampusOne**")
    st.markdown("---")
    
    menu = st.radio("Menu", ["Overview", "Daily Scheduler", "Settings"], label_visibility="collapsed")
    
    st.markdown("---")
    st.caption(f"📅 Today: {datetime.now().strftime('%b %d')}")

# --- 5. SCHEDULER LOGIC ---
if menu == "Daily Scheduler":
    
    # -- HEADER --
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("# Daily Focus")
        st.markdown(f"**{datetime.now().strftime('%A, %B %d, %Y')}**")
    with c2:
        if st.button("💾 Sync to Cloud"):
            # This triggers the save logic below
            st.toast("Syncing...", icon="☁️")

    # -- DATE PICKER --
    selected_date = st.date_input("Filter Date", datetime.now(), label_visibility="collapsed")
    st.markdown("---")

    # -- LOAD DATA --
    df_all = pd.DataFrame(ws_schedule.get_all_records())
    
    # Filter for selected date
    if not df_all.empty:
        df_all['Date'] = df_all['Date'].astype(str)
        day_data = df_all[df_all['Date'] == str(selected_date)]
    else:
        day_data = pd.DataFrame()

    # -- THE TIME SLOTS --
    time_slots = [
        "08:30 - 09:20", "09:20 - 10:10", "10:20 - 11:10",
        "11:10 - 12:00", "12:00 - 12:45", "12:45 - 01:30",
        "01:30 - 02:15", "02:15 - 03:00", "03:00 - 03:30"
    ]

    # -- RENDER TIME CARDS --
    # We use a form so the user can edit everything and hit Save once
    with st.form("scheduler_form"):
        
        # List to hold new data to save
        new_data_rows = []

        for slot in time_slots:
            # Find existing data for this slot
            existing = day_data[day_data['Time_Slot'] == slot] if not day_data.empty else pd.DataFrame()
            
            # Get current values or empty strings
            val_task = existing.iloc[0]['Task'] if not existing.empty else ""
            val_link = existing.iloc[0]['Link'] if not existing.empty else ""
            val_stake = existing.iloc[0]['Stakeholders'] if not existing.empty else ""
            val_remark = existing.iloc[0]['Remarks'] if not existing.empty else ""

            # -- THE UI CARD --
            st.markdown(f"""<div class="time-card">
                <div style="color:#0071E3; font-weight:700; font-size:14px; margin-bottom:8px;">{slot}</div>
            </div>""", unsafe_allow_html=True)
            
            c_task, c_link, c_who, c_note = st.columns([3, 2, 2, 2])
            
            with c_task:
                new_task = st.text_input(f"Task {slot}", value=val_task, placeholder="Focus Task...", label_visibility="collapsed")
            with c_link:
                new_link = st.text_input(f"Link {slot}", value=val_link, placeholder="URL", label_visibility="collapsed")
            with c_who:
                new_stake = st.text_input(f"Who {slot}", value=val_stake, placeholder="Stakeholders", label_visibility="collapsed")
            with c_note:
                new_remark = st.text_input(f"Note {slot}", value=val_remark, placeholder="Remarks", label_visibility="collapsed")

            # Collect data for saving
            if new_task: # Only save if there's a task
                new_data_rows.append([str(selected_date), slot, new_task, new_link, new_stake, new_remark])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # -- SAVE BUTTON --
        submitted = st.form_submit_button("✅ Update Schedule")
        
        if submitted:
            # 1. Clear old data for this date (Simple append strategy for V1, ideal is update)
            # For this version, we will just Append. 
            # In a production app, we would delete old rows for this date first.
            
            for row in new_data_rows:
                ws_schedule.append_row(row)
                
            st.success("Schedule Saved to Google Sheets!")
            st.rerun()

# --- 6. OVERVIEW PAGE (Placeholder) ---
elif menu == "Overview":
    st.title("Campus Overview")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="css-card">
            <h3>📅 Today's Focus</h3>
            <p style='color:#86868B'>Check the Daily Scheduler tab to manage your time blocks.</p>
        </div>""", unsafe_allow_html=True)
        
    with c2:
        st.markdown("""<div class="css-card">
            <h3>☁️ Cloud Status</h3>
            <p style='color:#10B981; font-weight:600'>Connected to Google Sheets</p>
        </div>""", unsafe_allow_html=True)

# --- 7. SETTINGS (Placeholder) ---
elif menu == "Settings":
    st.title("Settings")
    st.markdown("Configure your Gemini API Key here in the next update.")
