import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.title("🔧 Connection Diagnostic Tool")

try:
    # STEP 1: READ SECRETS
    st.write("1. Reading Secrets...")
    if "service_account" not in st.secrets:
        st.error("❌ Secrets are missing in Streamlit Settings!")
        st.stop()
    
    key_dict = json.loads(st.secrets["service_account"])
    email = key_dict['client_email']
    st.success(f"✅ Secrets loaded! Robot Email is: {email}")
    st.info("👉 PLEASE CHECK: Did you share your Google Sheet with this email address?")

    # STEP 2: AUTHENTICATE
    st.write("2. Authenticating with Google...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    st.success("✅ Authenticated successfully.")

    # STEP 3: FIND SHEET
    st.write("3. Looking for Spreadsheet named 'FPC Campus Data'...")
    try:
        sheet = client.open("FPC Campus Data")
        st.success("✅ Found Spreadsheet!")
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ ERROR: Could not find 'FPC Campus Data'. Check spelling or Share permissions.")
        st.stop()

    # STEP 4: CHECK TABS
    st.write("4. Checking for 'Logs' tab...")
    worksheets = sheet.worksheets()
    tab_names = [ws.title for ws in worksheets]
    st.info(f"Current Tabs in your sheet: {tab_names}")

    if "Logs" in tab_names:
        st.success("✅ 'Logs' tab found!")
        
        # STEP 5: WRITE TEST
        st.write("5. Writing a test row...")
        sheet.worksheet("Logs").append_row(["TEST", "CONNECTION", "SUCCESS", "IF YOU SEE THIS", "IT WORKS"])
        st.balloons()
        st.success("🎉 SUCCESS! Check your Google Sheet now. You should see a new row.")
    else:
        st.error("❌ ERROR: 'Logs' tab is missing. Please rename your tab in Google Sheets.")

except Exception as e:
    st.error(f"❌ UNEXPECTED ERROR: {e}")
