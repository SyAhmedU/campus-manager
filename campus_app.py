import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. APPLE CONFIGURATION ---
st.set_page_config(
    page_title="CampusOne",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed" # Apple likes clean full screens
)

# --- 2. THE "CUPERTINO" CSS ENGINE ---
st.markdown("""
    <style>
    /* 1. APPLE SYSTEM FONTS & BACKGROUND */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        color: #1D1D1F;
    }
    
    .stApp {
        background-color: #F5F5F7; /* The famous Apple Light Grey */
    }

    /* 2. SIDEBAR (macOS Settings Style) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #D2D2D7;
    }
    
    /* 3. THE "BENTO" CARD SYSTEM */
    .bento-card {
        background-color: #FFFFFF;
        border-radius: 24px; /* Large Apple Curves */
        padding: 35px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04); /* Subtle shadow */
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .bento-card:hover {
        transform: scale(1.01); /* Slight "Lift" on hover like iPadOS */
    }

    /* 4. TYPOGRAPHY */
    h1 {
        font-weight: 700;
        letter-spacing: -0.02em;
        font-size: 48px;
    }
    .hero-text {
        font-size: 56px;
        font-weight: 700;
        background: -webkit-linear-gradient(#1D1D1F, #424245);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 24px;
        font-weight: 600;
        color: #1D1D1F;
        margin-bottom: 5px;
    }
    .card-subtitle {
        font-size: 15px;
        color: #86868B; /* Apple Grey Text */
        font-weight: 400;
        margin-bottom: 20px;
    }

    /* 5. BADGES & ALERTS */
    .apple-badge {
        display: inline-block;
        padding: 4px 10px;
        background-color: #0071E3; /* Apple Blue */
        color: white;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    .alert-text {
        color: #FF3B30; /* Apple Red */
        font-weight: 600;
    }
    
    /* Hide Streamlit Boilerplate */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CONNECTION ---
try:
    key_dict = st.secrets["service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    sheet_id = "1LXnSQ55CfsGBgGYFNrqI6MhXTnsFQhkuPpYe2QPlBEE"
    sheet = client.open_by_key(sheet_id)
    ws_tasks = sheet.worksheet("Tasks")
except:
    st.error("Connection Error. Check Secrets.")
    st.stop()

# --- 4. NAVIGATION (Simple & Clean) ---
# We use a sidebar that mimics the macOS "Settings" list
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/814px-Apple_logo_black.svg.png", width=30)
    st.write("## CampusOne")
    st.write("---")
    
    module = st.radio("Menu", [
        "Dashboard",
        "Stakeholders", 
        "Mentors",
        "Teaching",
        "Logistics"
    ], label_visibility="collapsed")

# --- 5. DASHBOARD LOGIC ---
if module == "Dashboard":
    
    # FETCH DATA
    data = ws_tasks.get_all_records()
    df = pd.DataFrame(data)

    # --- HERO SECTION (Like the iPhone 15 Landing Page) ---
    st.markdown('<p class="hero-text">Control Center.</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size: 20px; color: #86868B;">Overview for {datetime.now().strftime("%A, %B %d")}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- BENTO GRID LAYOUT ---
    
    # ROW 1: THE BIG ALERT (Full Width)
    continuous_tasks = df[df['Category'] == 'Continuous']
    if not continuous_tasks.empty:
        # Check if there are active alerts
        st.markdown(f"""
        <div class="bento-card" style="border: 1px solid #FF3B30;">
            <div style="display:flex; justify-content:space-between;">
                <div>
                    <p class="card-title" style="color:#FF3B30;">Active Attention Required</p>
                    <p class="card-subtitle">Continuous supervision items.</p>
                </div>
                <span style="font-size:24px;">⚠️</span>
            </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, (index, row) in enumerate(continuous_tasks.iterrows()):
             with cols[i%3]:
                 st.markdown(f"**{row['Task']}**<br><span style='color:#86868B; font-size:13px'>{row['Notes']}</span>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 2: SPLIT VIEW (Daily & Weekly)
    col_left, col_right = st.columns([1,1])

    with col_left:
        # DAILY CARD
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">Today</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Daily priorities.</p>', unsafe_allow_html=True)
        
        daily = df[df['Frequency'] == 'Daily']
        if not daily.empty:
            for i, row in daily.iterrows():
                is_done = row['Status'] == 'Done'
                st.checkbox(row['Task'], value=is_done, key=f"d_{i}")
        else:
            st.write("No daily tasks.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # WEEKLY CARD
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">This Week</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Teaching & Prep.</p>', unsafe_allow_html=True)
        
        weekly = df[df['Frequency'] == 'Weekly']
        if not weekly.empty:
            for i, row in weekly.iterrows():
                st.checkbox(row['Task'], value=(row['Status']=='Done'), key=f"w_{i}")
        else:
            st.write("No weekly tasks.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ROW 3: STRATEGIC (Full Width Dark Mode)
    st.markdown("""
    <div class="bento-card" style="background-color: #1D1D1F; color: white;">
        <p class="card-title" style="color:white;">Strategic Vision</p>
        <p class="card-subtitle" style="color:#86868B;">Long-term horizon.</p>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("📅 **Monthly Compliance**")
        monthly = df[df['Frequency'] == 'Monthly']
        if not monthly.empty:
            st.dataframe(monthly[['Task', 'Status']], use_container_width=True, hide_index=True)
    with col_s2:
        st.write("🔭 **Yearly Goals**")
        yearly = df[df['Frequency'] == 'Yearly']
        if not yearly.empty:
            for i, row in yearly.iterrows():
                st.markdown(f"- {row['Task']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.title(module)
    st.info("Coming soon.")
