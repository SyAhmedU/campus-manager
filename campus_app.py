import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. PAGE CONFIGURATION (Browser Tab) ---
st.set_page_config(
    page_title="CampusOne | Executive Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CSS (The "High-End" Look) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F4F6F9;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1A202C;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    /* Card Styling (Shadow Boxes) */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
    }
    
    /* Custom Headers */
    .erp-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: #1A202C;
        margin-bottom: 0px;
    }
    .erp-subheader {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        font-size: 18px;
        color: #4A5568;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Alert Box Design */
    .alert-card {
        background-color: #FFF5F5;
        border-left: 5px solid #E53E3E;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: #742A2A;
    }
    
    /* Strategic Box Design */
    .strategy-card {
        background-color: #F0FFF4;
        border-left: 5px solid #38A169;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: #22543D;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONNECTION SETUP ---
try:
    key_dict = st.secrets["service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    
    # YOUR ACTUAL SHEET ID
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE"
    sheet = client.open_by_key(sheet_id)
    
    # LOAD TABS (With Error Handling)
    try:
        ws_tasks = sheet.worksheet("Tasks")
    except:
        st.error("⚠️ System Halted: Tab 'Tasks' missing in Google Sheet.")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Connection Failed: {e}")
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 🏢 **CAMPUS ONE**")
    st.markdown("### *Executive Control*")
    st.markdown("---")
    
    selected_module = st.radio("OPERATIONS MODULES", [
        "1. ⏱️ Time-Horizon",
        "2. 🤝 Stakeholder Matrix", 
        "3. 👥 Mentor Team",
        "4. 🍎 Teaching Hub",
        "5. 📦 Logistics & Projects"
    ])
    
    st.markdown("---")
    st.markdown(f"**System Status:** 🟢 Online\n\n**Date:** {datetime.now().strftime('%d %b %Y')}")

# --- 5. MODULE 1: TIME-HORIZON DASHBOARD ---
if selected_module == "1. ⏱️ Time-Horizon":
    
    # -- HEADER SECTION --
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<p class="erp-header">Executive Overview</p>', unsafe_allow_html=True)
        st.markdown(f"Welcome back. Here is your operational landscape for **{datetime.now().strftime('%A')}**.")
    with c2:
        # Quick KPI Cards
        st.metric("Pending Actions", "12", "-2")
    
    st.markdown("---")

    # Fetch Data
    data = ws_tasks.get_all_records()
    df = pd.DataFrame(data)

    # -- ROW 1: THE "CONTINUOUS ATTENTION" ZONE (RED ALERTS) --
    st.markdown('<p class="erp-subheader">🔥 Continuous Attention Zone (Active Risks)</p>', unsafe_allow_html=True)
    
    if not df.empty:
        continuous = df[df['Category'] == 'Continuous']
        if not continuous.empty:
            cols = st.columns(3) # Display alerts in a grid of 3
            for i, (index, row) in enumerate(continuous.iterrows()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="alert-card">
                        <b>⚠️ {row['Task']}</b><br>
                        <span style="font-size:12px">{row['Notes']}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("✅ No critical continuous issues active.")
    
    # -- ROW 2: OPERATIONAL GRID (DAILY & WEEKLY) --
    st.markdown('<br>', unsafe_allow_html=True)
    col_daily, col_weekly = st.columns(2)
    
    with col_daily:
        # styled container
        st.markdown('<div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd;">', unsafe_allow_html=True)
        st.markdown('<p class="erp-subheader" style="margin-top:0;">✅ Daily Action List</p>', unsafe_allow_html=True)
        
        if not df.empty:
            daily = df[df['Frequency'] == 'Daily']
            for i, row in daily.iterrows():
                is_done = row['Status'] == 'Done'
                if st.checkbox(f"**{row['Task']}**", value=is_done, key=f"d_{i}"):
                    if not is_done: st.toast(f"Completing: {row['Task']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_weekly:
        st.markdown('<div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd;">', unsafe_allow_html=True)
        st.markdown('<p class="erp-subheader" style="margin-top:0;">📅 Weekly Targets</p>', unsafe_allow_html=True)
        
        if not df.empty:
            weekly = df[df['Frequency'] == 'Weekly']
            for i, row in weekly.iterrows():
                st.checkbox(f"{row['Task']}", value=(row['Status']=='Done'), key=f"w_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

    # -- ROW 3: STRATEGIC HORIZON (LONG TERM) --
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<p class="erp-subheader">🔭 Strategic Horizon (Vision & Compliance)</p>', unsafe_allow_html=True)
    
    s1, s2 = st.columns(2)
    with s1:
        st.info("Monthly Compliance Reports")
        if not df.empty:
            monthly = df[df['Frequency'] == 'Monthly']
            st.table(monthly[['Task', 'Status']])
            
    with s2:
        if not df.empty:
            yearly = df[df['Frequency'] == 'Yearly']
            for i, row in yearly.iterrows():
                st.markdown(f"""
                <div class="strategy-card">
                    <b>🏆 {row['Task']}</b><br>
                    <span style="font-size:12px">{row['Notes']}</span>
                </div>
                """, unsafe_allow_html=True)

# --- OTHER MODULES (PLACEHOLDERS) ---
else:
    st.title(f"{selected_module}")
    st.info("This ERP module is currently under development. Please return to the Dashboard.")
