import streamlit as st
import requests
from bs4 import BeautifulSoup

# ==============================
# CONFIG
# ==============================
INTRANET_URL = "http://10.207.195.198/dynparm_187.htm"

st.set_page_config(page_title="ONGC Live Pressure", layout="centered")

st.title("ONGC – Live Pressure Monitor")

# ==============================
# FUNCTION TO FETCH PRESSURE
# ==============================
def fetch_pressure():
    try:
        r = requests.get(INTRANET_URL, timeout=3)
        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.find(class_="gross")

        if tag:
            value = float(tag.get_text(strip=True).replace(",", ""))
            return value, "LIVE"
        else:
            return None, "TAG NOT FOUND"

    except:
        return None, "INTRANET NOT REACHABLE"


# ==============================
# SESSION STATE FOR LAST VALUE
# ==============================
if "last_pressure" not in st.session_state:
    st.session_state.last_pressure = None

# ==============================
# AUTO REFRESH
# ==============================
auto = st.checkbox("Enable Auto Refresh", value=True)

if auto:
    import time
    time.sleep(5)  # refresh every 5 seconds
    st.rerun()

# ==============================
# FETCH DATA
# ==============================
pressure, status = fetch_pressure()

# ==============================
# DISPLAY LOGIC
# ==============================
if pressure is not None:
    st.session_state.last_pressure = pressure
    st.success("✅ LIVE DATA FROM DCS")

elif st.session_state.last_pressure is not None:
    pressure = st.session_state.last_pressure
    st.warning("⚠️ Showing LAST AVAILABLE VALUE")

else:
    pressure = st.number_input("Enter Manual Pressure", value=0.0)
    st.warning("⚠️ Manual Mode")

# ==============================
# KPI DISPLAY
# ==============================
st.metric("Pressure", f"{pressure}")


st.caption(f"Status: {status}")

